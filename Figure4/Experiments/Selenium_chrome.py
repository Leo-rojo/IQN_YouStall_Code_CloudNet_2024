from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import pyautogui
import os
import time
from selenium.webdriver.chrome.options import Options
import subprocess

switch_button = (1099,918) #Put the position of the 'autoplay' button on your monitor
pyautogui.PAUSE = 0  #maximize the clicking speed
def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/home/leonardo/Desktop/user_chrome")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument('--enable-quic')
    chrome_options.headless = False
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def click_during_stall_theoretical(frequency):
    global clicks
    while not stop_thread_event.is_set():
        time.sleep(0.021857500076293945) #average time of 4 clicks
        clicks.append(time.time())
        time.sleep(frequency)
def check_buffering(driver):
    try:
        spinner = driver.find_element(By.CLASS_NAME, "ytp-spinner")
        if "display: none;" in spinner.get_attribute("style"):
            return False
        else:
            return True
    except Exception as e:
        print("Error:", e)
def save_cliks_and_clear(folder_path):
    global clicks
    with open(folder_path + 'Clicks.txt', 'a') as f_clicks:
        for click in clicks:
            f_clicks.write(str(click)+'\n')
    clicks.clear()

if __name__ == "__main__":
    clicks = []
    conta_stalls = 0
    click_frequency = 0.200
    Network_id = '1000Kbps'
    Video_link = 'https://www.youtube.com/watch?v=znN1GoKbPf4' # put the link of the video you want to test
    nr_stall_limit = 100 # number of stalls to be detected before ending the experiment
    interface = 'wlo1'  # put the name of your interface
    subprocess.run(['sudo', '/home/leonardo/Desktop/venv_310/bin/tcdel', interface, '--all'], check=True)# clear all the traffic control rules
    driver = start_browser()
    driver.set_window_position(0, 0)  # Select the monitor to open Browser
    driver.maximize_window()  # Maximize the window
    driver.get(Video_link)
    time.sleep(3)

    print('close chat')
    pyautogui.click(1776, 248)
    video_id = Video_link.split('=')[-1]
    folder_path = 'Results/' + video_id + '_' + Network_id + '/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    #wait before setting the network
    time.sleep(20)
    stop_thread_event = threading.Event()
    thread = None
    stall_length = 0
    stall_time = 0
    start_time = time.time()
    with open(folder_path+'Real_stalls.txt', 'a') as f_stalls:
        while conta_stalls < nr_stall_limit:
            if check_buffering(driver):
                if stall_time == 0:  # Stall starts
                    stall_start_time = time.time()
                    stall_time = stall_start_time
                    stop_thread_event.clear()  # Ensure the event is cleared before starting the thread
                    thread = threading.Thread(target=click_during_stall_theoretical, args=(click_frequency,))
                    thread.start()
                    f_stalls.write('S-' + str(stall_start_time) + '\n')
            else:
                if stall_time != 0:  # Stall ends
                    stall_end_time = time.time()
                    # Stop the click thread
                    stop_thread_event.set()  #Stop the clicking thread
                    thread.join()  # Wait for the thread to finish
                    thread = None  # Clean up the thread object

                    stall_length = stall_end_time - stall_time
                    f_stalls.write('E-'+str(stall_end_time) + '\n')
                    print('------STALL ', stall_length)
                    stall_time = 0  # Reset for next stall
                    stall_length = 0  # Reset the stall length
                    clicks.append('----------')
                    save_cliks_and_clear(folder_path)
                    conta_stalls += 1

        #Deal with the stall that happens at the end of the experiment
        if stall_time != 0:
            stall_end_time = time.time()
            stop_thread_event.set()  #Stop the clicking thread
            stall_length = stall_end_time - stall_time
            f_stalls.write('E-'+str(stall_end_time) + '\n')
            print('------FINAL STALL ', stall_length)
            save_cliks_and_clear(folder_path)
            conta_stalls += 1
    driver.quit()
