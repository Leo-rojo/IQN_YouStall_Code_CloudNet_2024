from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time
from selenium.webdriver.chrome.options import Options
import subprocess

switch_button = (1099,918) #Put the position of the 'autoplay' button on your monitor
pyautogui.PAUSE = 0  #maximize the clicking speed
def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/your/path/user_chrome")
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
    conta_stalls = 0
    click_frequency = 0.200
    Network_id = '1000Kbps'
    Video_link = ''# put the link of the live youtube video you want to test, e.g. 'https://www.youtube.com/watch?v=NqRP08sCG_w'
    nr_stall_limit = 10 # number of stalls to be detected before ending the experiment
    interface = 'wlo1'  # put the name of your interface
    subprocess.run(['sudo', '/your/path/tcdel', interface, '--all'], check=True)# clear all the traffic control rules
    driver = start_browser()
    driver.set_window_position(0, 0)  # Select the monitor to open Browser
    driver.maximize_window()  # Maximize the window
    driver.get(Video_link)
    time.sleep(3)

    print('close chat')
    pyautogui.click(1776, 248)
    video_id = Video_link.split('=')[-1]

    #wait before setting the network
    time.sleep(20)
    stall_length = 0
    stall_time = 0
    start_time = time.time()
    while conta_stalls < nr_stall_limit:
        if check_buffering(driver):
            if stall_time == 0:  # Stall starts
                stall_start_time = time.time()
                stall_time = stall_start_time
        else:
            if stall_time != 0:  # Stall ends
                stall_end_time = time.time()
                stall_length = stall_end_time - stall_time
                print('------STALL ', stall_length)
                stall_time = 0  # Reset for next stall
                stall_length = 0  # Reset the stall length
                conta_stalls += 1

    #Deal with the stall that happens at the end of the experiment
    if stall_time != 0:
        stall_end_time = time.time()
        stall_length = stall_end_time - stall_time
        print('------FINAL STALL ', stall_length)
        conta_stalls += 1
    driver.quit()
