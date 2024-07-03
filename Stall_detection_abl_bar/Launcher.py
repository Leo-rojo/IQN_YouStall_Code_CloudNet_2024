import subprocess
import os
import time
import random

def select_random_files(main_directory, num_folders=3, num_files_per_folder=1, seed=None):
    # Optionally set the seed for reproducibility
    if seed is not None:
        random.seed(seed)
    # List all folders in the main directory
    folders = [f.path for f in os.scandir(main_directory) if f.is_dir()]

    # Check if there are enough folders to select from
    if len(folders) < num_folders:
        raise ValueError("Not enough folders to select from.")

    # Randomly select the specified number of folders
    selected_folders = random.sample(folders, num_folders)

    # Select random files from each selected folder
    selected_files = []
    for folder in selected_folders:
        files = [f.path for f in os.scandir(folder) if f.is_file()]
        if len(files) < num_files_per_folder:
            raise ValueError(f"Not enough files in folder {folder} to select {num_files_per_folder}.")
        selected_files.extend(random.sample(files, num_files_per_folder))

    return selected_folders, selected_files
def select_random_video_links(video_links_all, num_links=3, seed=None):
    if seed is not None:
        random.seed(seed)
    # Select random video links
    return random.sample(video_links_all, num_links)
def get_pid(window_title):
    # Command to get the PID of the window with the specified title
    command = f"pgrep -f '{window_title}'"
    # Execute the command and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Extract and return the PID from the output
    return int(result.stdout.split('\n')[0])
def send_sudo_password(password):
    # Command to echo the sudo password and pipe it to sudo
    sudo_command = f"echo {password} | sudo -S echo ''"
    # Execute the sudo command
    subprocess.run(sudo_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":

    interval_screenshot_values = [0.1, 0.2, 0.5, 1, 2]
    processes = []

    for i, interval in enumerate(interval_screenshot_values, start=1):
        #if i==1:
        terminal_command = f"x-terminal-emulator -T 'Script {i}' -e bash -c 'python Stalls_detector_par_01_simplified.py {interval}'"
        # else:
        #     terminal_command = f"x-terminal-emulator -T 'Script {i}' -e bash -c 'python Stalls_detector_par.py {interval}'"
        process = subprocess.Popen(terminal_command, shell=True)
        processes.append(process)
        print(f"Script {i} started with interval {interval}.")

    # Wait for all processes to finish
    for i, process in enumerate(processes, start=1):
        return_code = process.wait()
        print(f"Script {i} finished with return code: {return_code}")
    # if not os.path.exists('Results'):
    #     os.makedirs('Results')
    # interval_screenshot = 0.1
    # terminal_command = f"x-terminal-emulator -T 'Script 1' -e bash -c 'python Stalls_detector_par_01_over.py'"
    # process1 = subprocess.Popen(terminal_command, shell=True)
    # print("Script 1 started.")
    # interval_screenshot = 0.2
    # terminal_command = f"x-terminal-emulator -T 'Script 2' -e bash -c 'python Stalls_detector_par.py{interval_screenshot}'"
    # process2 = subprocess.Popen(terminal_command, shell=True)
    # print("Script 2 started.")
    # interval_screenshot = 0.3
    # terminal_command = f"x-terminal-emulator -T 'Script 3' -e bash -c 'python Stalls_detector_par.py{interval_screenshot}'"
    # process3 = subprocess.Popen(terminal_command, shell=True)
    # print("Script 3 started.")
    # interval_screenshot = 0.4
    # terminal_command = f"x-terminal-emulator -T 'Script 4' -e bash -c 'python Stalls_detector_par.py{interval_screenshot}'"
    # process4 = subprocess.Popen(terminal_command, shell=True)
    # print("Script 4 started.")
    # interval_screenshot = 0.5
    # terminal_command = f"x-terminal-emulator -T 'Script 5' -e bash -c 'python Stalls_detector_par.py{interval_screenshot}'"
    # process5 = subprocess.Popen(terminal_command, shell=True)
    # print("Script 5 started.")
    #
    #
    # process5_return_code = process5.wait()
    # print(f"Script 1 finished with return code: {process5_return_code}")

