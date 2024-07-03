import os
from PIL import ImageGrab, Image, ImageChops
import time
import numpy as np
import sys
from collections import deque
import pyautogui
import threading
import copy


switch_button = (1097, 920)  # Coordinates of the button to click full window in selenium and firefox
pyautogui.PAUSE = 0  # maximize the clicking speed
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
def thumbnail_difference(bbox,threshold=300):
    # Check if the difference forms the contour of a rectangle
    x1, y1, x2, y2 = bbox
    #width = x2 - x1
    height = y2 - y1
    is_thumbnail = height < threshold
    return is_thumbnail
def create_external_screenshot(screenshot, central_square_bbox):
    """Creates an external screenshot by filling the central square with black."""
    external_screenshot = Image.new('RGB', screenshot.size)
    external_screenshot.paste(screenshot, (0, 0))
    external_screenshot.paste((0, 0, 0), central_square_bbox)  # Fill the central square with black
    return external_screenshot
def create_external_screenshot_alternative(screenshot, central_square_bbox):
    """Creates an external screenshot by filling the central square with black."""
    # Convert the screenshot to a NumPy array for faster processing
    screenshot_array = np.array(screenshot)

    # Create an external screenshot array initialized with zeros
    external_screenshot_array = np.zeros_like(screenshot_array)

    # Fill the entire external screenshot array with the original screenshot
    external_screenshot_array[:] = screenshot_array

    # Get the coordinates of the central square
    x1, y1, x2, y2 = central_square_bbox

    # Fill the central square region with black
    external_screenshot_array[y1:y2, x1:x2] = [0, 0, 0]

    # Convert the NumPy array back to an image
    external_screenshot = Image.fromarray(external_screenshot_array)

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
            return True, external_screenshot, internal_screenshot, ''
        if not external_equal:
            if thumbnail_difference(thumbnail_box): #if difference is a thumbnail: height difference less than 300
                #print('thumbnail detected')
                ### metti condizioni per dire se ancora stall o no
                return True, external_screenshot, internal_screenshot, 'thumb'
    return False, external_screenshot, internal_screenshot, ''
def click_during_stall_real(frequency):
    global detected_clicks
    while not stop_thread_event.is_set():
        pyautogui.click(switch_button)
        pyautogui.click(switch_button)
        pyautogui.click(switch_button)
        detected_clicks.append(time.time())
        time.sleep(frequency)
def save_cliks_and_clear(folder_path):
    global detected_clicks
    global interval_screenshot
    with open(folder_path + 'Detected_clicks_'+str(interval_screenshot)+'.txt', 'a') as f_clicks:
        for click in detected_clicks:
            f_clicks.write(str(click) + '\n')
    detected_clicks.clear()
def save_stalls_and_clear(folder_path):
    global save_stalls_time
    global interval_screenshot
    with open(folder_path + 'Detected_stalls.'+str(interval_screenshot)+'txt', 'a') as f_stalls:
        for stall in save_stalls_time:
            f_stalls.write(str(stall) + '\n')
    save_stalls_time.clear()




if __name__ == "__main__":
    # Get parameter passed to script
    if len(sys.argv) > 1:
        # Network_id = sys.argv[1]
        # Video_link = sys.argv[2]
        # length_individual_exp = int(sys.argv[3])
        interval_screenshot = float(sys.argv[1])
        # click_frequency = float(sys.argv[5])
    nr_session = 1
    Network_id = '1000Kbps'
    Video_link = 'https://www.youtube.com/watch?v=mzdfGCdNSHQ'#'https://www.youtube.com/watch?v=-hK3py6FlDU'#https://www.youtube.com/watch?v=bZ3O-8pQLd0'
    length_individual_exp = 1000
    click_frequency = 0.5
    #interval_screenshot = 0.2

    print("Parameter received by script 2:", Network_id)
    print('Video link received by script 2:', Video_link)
    print("Length received by script 2:", length_individual_exp)
    print("Interval_screenshot received by script 2:", interval_screenshot)
    print("Click frequency received by script 2:", click_frequency)
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
    folder_path = 'Results/' + video_id + '_' + Network_id + '/'+'Session_'+str(nr_session)+'/'

    if os.path.exists(folder_path + 'Detected_stalls.'+str(interval_screenshot)+'txt'):
        os.remove(folder_path + 'Detected_stalls.'+str(interval_screenshot)+'txt')
    if os.path.exists(folder_path + 'Detected_stalls.'+str(interval_screenshot)+'txt'):
        os.remove(folder_path + 'Detected_stalls.'+str(interval_screenshot)+'txt')

    ## Check if video element is present and get its size
    #video_elem = driver.find_element(By.CLASS_NAME, "html5-main-video")
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
    space_top_selenium = 50 #20 #50 with selenium and chrome, 0 without selenium 20firefox
    screen_bbox = (100, 170+space_top_selenium, width+100, 853)#height+160)

    ## Capture screenshots
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
            stall_detected, external_screenshot, internal_screenshot, thumb = take_screenshot(previous_screenshots,bbox,screen_bbox)
            now=time.time()
            #print('!!stall detected: '+str(stall_detected)+' previous_stall_detected: '+str(previous_stall_detected)+ ' time diff: '+str(now-previous_time))
            previous_time = now
            # Update the previous screenshots for the next iteration
            previous_screenshots[0] = external_screenshot
            previous_screenshots[1] = internal_screenshot
            #logic for calculating the stalls
            if stall_detected and previous_stall_detected: # stall continues
                if thumb!='thumb': ########NB in theory there should be the if!!!!
                    sum_time += interval # questionable round for excess
                    print('stall continues')
                    save_last_three_outcomes.append('stall continues')
                #else if not thumb I don't count the sum time, because it is true and true because of the disappear of the thumbnail
            elif stall_detected and not previous_stall_detected: # new stall
                if thumb != 'thumb':
                    sum_time += interval # questionable round for excess
                    stall_start_time = time.time()
                    print('new stall')
                    save_stalls_time.append('S-'+str(stall_start_time))
                    ###here I should start the clicks thread
                    # Start the click thread
                    stop_thread_event.clear()  # Ensure the event is cleared before starting the thread
                    thread = threading.Thread(target=click_during_stall_real, args=(click_frequency,))
                    thread.start()
                    save_last_three_outcomes.append('new stall')
                else:
                    print('no stall')
                    ####if condition to distinguish when stall detected because of thumbnail as stall after nothing and when in middle of stall
                    if sum_time==0:
                        stall_detected = False
                    else:
                        sum_time += interval  # questionable round for excess
                    save_last_three_outcomes.append('no stall')
            elif not stall_detected and previous_stall_detected: # end of stall
                if sum_time!=0:
                    stall_detected_time = time.time()
                    sum_time += interval  ##### controversial, not necessarily right, check it out later
                    print('end of stall')
                    print('Stall_duration: '+ str(stall_detected_time-stall_start_time))
                    save_last_three_outcomes.append('end of stall')
                    save_stalls_time.append('E-'+str(stall_detected_time))
                    #here I should stop the clicks thread
                    stop_thread_event.set()  # Signal the thread to stop
                    thread.join()  # Wait for the thread to finish
                    #move away the pointer
                    #pyautogui.moveTo(1107, 945)
                    thread = None  # Clean up the thread object
                    detected_clicks.append('----------')
                    save_cliks_and_clear(folder_path)
                    save_stalls_and_clear(folder_path)

                    if sum_time==0.1 and save_last_three_outcomes[0]!='no stall': #I've noticed that often the detector detect new stall of 0.1 after a previous stall that actually belong to the previous stall
                        print('super short stall belonging to the previous')
                        save_stalls[-1] += 0.1
                    else:
                        #save the stall info
                        save_stalls.append(sum_time)
                        # with open(folder_path+video_id+'_'+Network_id+'_detected.txt', 'a') as f:
                        #     f.write(str(sum_time) + '\n')
                    sum_time = 0
            else: # no stall
                print('no stall')
                save_last_three_outcomes.append('no stall')

            previous_stall_detected = copy.copy(stall_detected)
            next_capture_time += interval
            # Dynamically adjust sleep to maintain the interval
            time_to_next_capture = max(0, next_capture_time - time.time())
            time.sleep(time_to_next_capture)







