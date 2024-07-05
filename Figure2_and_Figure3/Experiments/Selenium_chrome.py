from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import os
import time
from selenium.webdriver.chrome.options import Options
import subprocess

switch_button = (1099,918) #Put the position of the 'autoplay' button on your monitor
pyautogui.PAUSE = 0  #maximize the clicking speed
def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/your/path/user_chrome") #To keep the user logged in, use your own path
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument('--enable-quic')
    chrome_options.headless = False
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def check_buffering(driver):
    try:
        spinner = driver.find_element(By.CLASS_NAME, "ytp-spinner")
        if "display: none;" in spinner.get_attribute("style"):
            return False
        else:
            return True
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    Video_link = 'https://www.youtube.com/watch?v=XJVXN7xi02k'  # put the link of the video you want to test
    kind = 'sport'  # put the kind of video you are testing: news, music, sport
    clicks = []
    conta_stalls = 0
    Network_id = '1000Kbps'
    nr_stall_limit = 100 #number of stalls to be detected before ending the experiment
    interface = 'wlo1' #put the name of your interface
    subprocess.run(['sudo', '/your/path/tcdel', interface, '--all'], check=True) #clear all the traffic control rules
    driver = start_browser()
    driver.set_window_position(0, 0) # Select the monitor to open Browser
    driver.maximize_window() # Maximize the window
    driver.get(Video_link)
    time.sleep(3)

    #close the chat
    print('close chat')
    pyautogui.click(1776, 248)

    video_id = Video_link.split('=')[-1]
    folder_path = 'Results_'+kind+'/' + video_id + '_' + Network_id+'/p_0.2' #put the path where you want to save the results
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #wait before setting the network
    time.sleep(20)

    stall_length = 0
    stall_time = 0
    with open(folder_path+'/Real_stalls.txt', 'a') as f_stalls:
        while conta_stalls < nr_stall_limit:
            if check_buffering(driver):
                if stall_time == 0:  # Stall starts
                    stall_start_time = time.time()
                    stall_time = stall_start_time
                    f_stalls.write('S-' + str(stall_start_time) + '\n')
            else:
                if stall_time != 0:  # Stall ends
                    stall_end_time = time.time()
                    stall_length = stall_end_time - stall_time
                    f_stalls.write('E-'+str(stall_end_time) + '\n')
                    print('------STALL ', stall_length)
                    stall_time = 0  # Reset for next stall
                    stall_length = 0  # Reset the stall length
                    clicks.append('----------')
                    conta_stalls += 1

        #Deal with the stall that happens at the end of the experiment
        if stall_time != 0:
            stall_end_time = time.time()
            stall_length = stall_end_time - stall_time
            f_stalls.write('E-'+str(stall_end_time) + '\n')
            print('------FINAL STALL ', stall_length)
            conta_stalls += 1

    driver.quit()
