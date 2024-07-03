from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import pyautogui
import os
import time
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.chrome.options import Options
import subprocess


switch_button = (1097, 920)  # Coordinates of the button to click full window in selenium and firefox
pyautogui.PAUSE = 0  # maximize the clicking speed
def start_browser(chrome):
    if chrome:
        #user_data_dir = '/home/leonardo/Desktop/New Folder 1'
        #user_data_dir = '/home/leonardo/.config/google-chrome/'
        #profile = 'Default'
        # Set up Chrome options
        chrome_options = Options()
        #chrome_options.add_argument(f'user-data-dir={user_data_dir}')  # I use my profile only for blocking the advertisement with ublock plugin
        #chrome_options.add_argument(f'--profile-directory={profile}')
        chrome_options.add_argument("--user-data-dir=/home/leonardo/Desktop/user_chrome")
        chrome_options.add_argument("--disable-cache")
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
        # Additional Chrome options to force QUIC
        chrome_options.add_argument('--enable-quic')
        #chrome_options.add_argument('--origin-to-force-quic-on='+video_link+':443')

        chrome_options.headless = False
        driver = webdriver.Chrome(options=chrome_options)
    else:
        # Set up Firefox options
        user_data_dir = '/home/leonardo/snap/firefox/common/.mozilla/firefox/'
        profile = 'pk38y8cg.default-1703190718502'
        profile_path = f'{user_data_dir}{profile}'
        options = FFOptions()
        service = FFService(executable_path="/snap/bin/geckodriver")
        options.add_argument("-profile")
        options.add_argument(profile_path)
        os.environ['SSLKEYLOGFILE'] = '/home/leonardo/Desktop/sslkeylogfile.log'  # Replace with your desired file path
        # Set Firefox preferences to disable cache
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.cache.disk.enable", False)
        firefox_profile.set_preference("browser.cache.memory.enable", False)
        firefox_profile.set_preference("browser.cache.offline.enable", False)
        firefox_profile.set_preference("network.http.use-cache", False)
        # browser = webdriver.Firefox(executable_path=geckodriver_path, options=options)
        driver = webdriver.Firefox(options=options, service=service)
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
def click_during_stall_real(frequency):
    global clicks
    while not stop_thread_event.is_set():
        pyautogui.click(switch_button)
        pyautogui.click(switch_button)
        pyautogui.click(switch_button)
        #pyautogui.click(switch_button)
        clicks.append(time.time())
        time.sleep(frequency)
def click_during_stall_theoretical(frequency):
    global clicks
    while not stop_thread_event.is_set():
        # pyautogui.click(switch_button)
        # pyautogui.click(switch_button)
        # pyautogui.click(switch_button)
        # pyautogui.click(switch_button)
        #Put time necessary to click 4 times in a row
        #time.sleep(0.005182421207427979) 4 clicks
        time.sleep(0.004062247276306152) #3 clicks
        clicks.append(time.time())
        time.sleep(frequency)
def run_fixed_network_tcconfig(interface, Network_id, global_state, start):
    while True:
        if start:
            subprocess.run(['sudo', '/home/leonardo/Desktop/venv_310/bin/tcset', interface, '--rate', Network_id, '--direction','incoming'], check=True)
            print('Network limit set to: ' + Network_id)
            start=False
        if global_state['stop_signal']:
            print("Bandwidth emulation stopped.")
            # remove_bandwidth(interface)
            subprocess.run(['sudo', '/home/leonardo/Desktop/venv_310/bin/tcdel', interface, '--all'], check=True)
            break
def save_cliks_and_clear(folder_path):
    global clicks
    with open(folder_path + 'Clicks.txt', 'a') as f_clicks:
        for click in clicks:
            f_clicks.write(str(click)+'\n')
    clicks.clear()

if __name__ == "__main__":
    clicks = []
    # Get parameter passed to script
    #if len(sys.argv) > 4:
    # Network_id = sys.argv[1]
    # Video_link = sys.argv[2]
    # length_individual_exp = int(sys.argv[3])
    # click_frequency = float(sys.argv[4])
    nr_session = 2
    Network_id = '1000Kbps'
    Video_link = 'https://www.youtube.com/watch?v=EOrJ-NxukTo'#'https://www.youtube.com/watch?v=mzdfGCdNSHQ'#'https://www.youtube.com/watch?v=-hK3py6FlDU'#https://www.youtube.com/watch?v=bZ3O-8pQLd0'
    length_individual_exp = 1000
    click_frequency = 0.5
    conta_stalls = 0
    nr_stall_limit = 10
    chrome = True
    print("Network received by script 1:", Network_id)
    print('Video link received by script 1:', Video_link)
    print("Length received by script 1:", length_individual_exp)
    print("Click frequency received by script 1:", click_frequency)

    interface = 'wlo1'
    global_state = {'stop_signal': False}
    subprocess.run(['sudo', '/home/leonardo/Desktop/venv_310/bin/tcdel', interface, '--all'], check=True)
    driver = start_browser(chrome)
    # Select the monitor to open Browser
    driver.set_window_position(0, 0)
    # Maximize the window
    driver.maximize_window()
    driver.get(Video_link)
    time.sleep(3)
    #close the chat
    print('close chat')
    pyautogui.click(1776, 248)
    video_id = Video_link.split('=')[-1]
    folder_path = 'Results/'# + video_id + '_' + Network_id + '/'+'Session_'+str(nr_session)+'/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #wait before setting the network
    time.sleep(20)

    #set bandwidth limit
    #Network_path = '/home/leonardo/Desktop/ISP_user_collaboration/Traces/formatted_norway_aggregated_nohttp2/bus.ljansbakken-oslo/report.2010-09-29_1628CEST.log_formatted'
    #Network_path = '/home/leonardo/Desktop/ISP_user_collaboration/Traces/formatted_norway_aggregated_nohttp2/metro.kalbakken-jernbanetorget/report.2010-09-14_1038CEST.log_formatted'
    #network_thread = threading.Thread(target=run_network_tcconfig, args=(Network_path, 'wlo1', global_state,))
    network_thread = threading.Thread(target=run_fixed_network_tcconfig, args=('wlo1', Network_id, global_state, True,))
    #network_thread.start()


    stop_thread_event = threading.Event()
    thread = None
    stall_length = 0
    stall_time = 0
    if os.path.exists(folder_path+'Real_stalls.txt'):
        os.remove(folder_path+'Real_stalls.txt')
    if os.path.exists(folder_path+'Clicks.txt'):
        os.remove(folder_path+'Clicks.txt')


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

            time.sleep(0.05)

        #Deal with the stall that happens at the end of the experiment
        if stall_time != 0:
            stall_end_time = time.time()
            stop_thread_event.set()  #Stop the clicking thread
            stall_length = stall_end_time - stall_time
            f_stalls.write('E-'+str(stall_end_time) + '\n')
            print('------FINAL STALL ', stall_length)
            save_cliks_and_clear(folder_path)
            conta_stalls += 1

    # Stop the network emulation
    global_state['stop_signal'] = True
    #network_thread.join()
    driver.quit()
