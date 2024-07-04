import os
from PIL import ImageGrab, Image, ImageChops
import time
import numpy as np
import sys
from collections import deque
import pyautogui
import threading
import copy


switch_button = (1099,918) #Put the position of the 'autoplay' button on your monitor
pyautogui.PAUSE = 0  #maximize the clicking speed
def compare_images(image1, image2):
    """Compares two images and returns True if they are identical, False otherwise."""
    diff = ImageChops.difference(image1, image2)
    box = diff.getbbox()
    return not box, box
def compare_images_excluding_right_up_corner(image1, image2):
    """
    Compares two images and returns a tuple (are_identical, bbox, diff).
    are_identical is True if the images are identical, False otherwise.
    bbox is the bounding box of the difference if the images are not identical.
    diff is the image showing differences.
    """
    # Calculate the difference image
    diff = ImageChops.difference(image1, image2)

    # Define the region to exclude (right upper square section)
    exclude_box = (1200, 10, 1280, 50)

    # Exclude the specified region from the difference image
    exclude_region_from_diff(diff, exclude_box)

    # Calculate the bounding box of the differences
    bbox = diff.getbbox()


    # Return the result
    return not bbox, bbox
def exclude_region_from_diff(diff, exclude_box):
    """
    Excludes a specified region from the given difference image.
    """
    if exclude_box:
        x1, y1, x2, y2 = exclude_box
        pixels = diff.load()
        for x in range(x1, x2):
            for y in range(y1, y2):
                pixels[x, y] = (0, 0, 0) if diff.mode == 'RGB' else 0
def create_external_screenshot(screenshot, central_square_bbox):
    """Creates an external screenshot by filling the central square with black."""
    external_screenshot = Image.new('RGB', screenshot.size)
    external_screenshot.paste(screenshot, (0, 0))
    external_screenshot.paste((0, 0, 0), central_square_bbox)  # Fill the central square with black
    return external_screenshot
def take_screenshot(previous_screenshots,bbox,screen_bbox):
    screenshot = ImageGrab.grab(bbox=screen_bbox)
    external_screenshot = create_external_screenshot(screenshot, bbox)  # Example central square bbox, adjust according to your needs
    internal_screenshot = screenshot.crop(bbox)  # Example crop, adjust according to your needs
    # Compare with previous screenshots
    if not (previous_screenshots[0] is None or previous_screenshots[1] is None):
        external_equal,thumbnail_box= compare_images_excluding_right_up_corner(external_screenshot, previous_screenshots[0])
        #print('external_difference: '+str(thumbnail_box))
        internal_equal,_= compare_images(internal_screenshot, previous_screenshots[1])
        if (not internal_equal) and (external_equal):
            return True, external_screenshot, internal_screenshot
    return False, external_screenshot, internal_screenshot
def save_cliks_and_clear(folder_path,click_frequency):
    global detected_clicks
    with open(folder_path + 'Detected_clicks_'+str(click_frequency)+'.txt', 'a') as f_clicks:
        if detected_clicks:
            for click in detected_clicks:
                f_clicks.write(str(click) + '\n')
            detected_clicks.clear()
def save_stalls_and_clear(folder_path,click_frequency):
    global save_stalls_time
    with open(folder_path + 'Detected_stalls_'+str(click_frequency)+'.txt', 'a') as f_stalls:
        for stall in save_stalls_time:
            f_stalls.write(str(stall) + '\n')
    save_stalls_time.clear()


if __name__ == "__main__":
    interval_screenshot = 0.2
    Network_id = '1000Kbps'
    Video_link = 'https://www.youtube.com/watch?v=znN1GoKbPf4'
    length_individual_exp = 3000
    click_frequency = interval_screenshot
    video_id = Video_link.split('=')[-1]

    save_stalls = []
    save_stalls_time = []
    save_start_end_stalls = []
    detected_clicks = []
    save_last_three_outcomes = deque(maxlen=3)
    sum_time = 0
    stop_thread_event = threading.Event()
    thread = None
    interval = interval_screenshot
    duration = length_individual_exp
    folder_path = 'Results/' + video_id + '_' + Network_id + '/'

    # Create all directories in the folder path
    os.makedirs(folder_path, exist_ok=True)

    if os.path.exists(folder_path + 'Detected_stalls_'+str(click_frequency)+'.txt'):
        os.remove(folder_path + 'Detected_stalls_'+str(click_frequency)+'.txt')
    if os.path.exists(folder_path + 'Detected_clicks_'+str(click_frequency)+'.txt'):
        os.remove(folder_path + 'Detected_clicks_'+str(click_frequency)+'.txt')

    width = 1280 #video_elem.size["width"]
    height = 720 # video_elem.size["height"]
    print(f"Assumed video size: {height} x {width}")

    ## Calculate the coordinates for the bounding box
    radius = 60
    white_space_on_top = 0 #165 if I go manually, 200 if I go with selenium which add a white space on top
    white_space_left = 0
    top_left_x = (width / 2 - radius) + white_space_left
    top_left_y = (height / 2 - radius) + white_space_on_top
    bottom_right_x = (width / 2 + radius) + white_space_left
    bottom_right_y = (height / 2 + radius) + white_space_on_top
    bbox = (int(top_left_x), int(top_left_y), int(bottom_right_x), int(bottom_right_y))
    print(bbox)

    ## Define the screen bounding box to capture the entire screen
    space_top_selenium = 50 #I'm removing portion of screen that can interfere with the comparison, like commands/search bar
    screen_bbox = (100, 170+space_top_selenium, width+100, 853)

    start_time = time.time()
    next_capture_time = start_time + interval
    index = 0
    previous_screenshots = [None, None]  # Use a list to hold a mutable reference to the previous screenshot
    previous_stall_detected = False
    sum_time = 0

    previous_time=0
    while time.time() - start_time < duration:
        current_time = time.time()
        if current_time >= next_capture_time:
            index += 1
            start_screenshot=time.time()
            # stall detected can be True, False, 'control'
            stall_detected, external_screenshot, internal_screenshot = take_screenshot(previous_screenshots,bbox,screen_bbox)
            if stall_detected:
                print('stall detected')
                pyautogui.click(switch_button)
                pyautogui.click(switch_button)
                pyautogui.click(switch_button)
                pyautogui.click(switch_button)
                detected_clicks.append('S-' + str(time.time()))
            else:
                print('stall not detected')
                detected_clicks.append('N-' + str(time.time()))

            now=time.time()
            previous_time = now
            previous_screenshots[0] = external_screenshot
            previous_screenshots[1] = internal_screenshot
            #save every 10 index so to don't bottlneck the I/O
            if index%10==0:
                save_cliks_and_clear(folder_path,click_frequency)

            previous_stall_detected = copy.copy(stall_detected)
            next_capture_time += interval

            # Dynamically adjust sleep to maintain the interval
            time_to_next_capture = max(0, next_capture_time - time.time())
            time.sleep(time_to_next_capture)







