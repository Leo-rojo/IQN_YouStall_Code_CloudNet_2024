import matplotlib.pyplot as plt
import numpy as np
font_axes_titles = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 30,
                        }
font_title = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 30,
                        }
font_general = {'family' : 'sans-serif',
                        #'weight' : 'bold',
                        'size'   : 30}
plt.rc('font', **font_general)

folder_path='/home/leonardo/Desktop/ISP_user_collaboration/cumulative_packets_click_experiment/Results_cumul/mzdfGCdNSHQ_1000Kbps/p_0.2 w_0.1/'
def parse_stalls(stall_lines):
    stalls = []
    for i in range(0, len(stall_lines), 2):
        start_time = float(stall_lines[i].strip()[2:])
        end_time = float(stall_lines[i + 1].strip()[2:])
        stalls.append((start_time, end_time))
    return stalls
with open(folder_path+'Detected_clicks.txt', 'r') as f:
    detected_clicks = f.readlines()
with open(folder_path+'timestamp_of_candidate.txt', 'r') as f:
    time_candidate = f.readlines()
with open(folder_path + 'Real_stalls.txt', 'r') as f:
    real_stalls = f.readlines()
clicks_clean = [click.strip() for click in detected_clicks if click != '----------\n']
time_candidate_clean = [time.strip() for time in time_candidate]
real_stalls_cleaned = [stall.strip() for stall in real_stalls]
real_stalls_parsed = parse_stalls(real_stalls)
real_stalls_length = [(end-start)*1000 for start, end in real_stalls_parsed]
# Convert timestamps from string to float
clicks_clean = list(map(float, clicks_clean))
time_candidate_clean = list(map(float, time_candidate_clean))
# Sort the timestamps
clicks_clean.sort()
time_candidate_clean.sort()

time_diff_orig = []
for i in range(1, len(time_candidate_clean)):
    time_diff_orig.append(time_candidate_clean[i] - time_candidate_clean[i-1])
#save time diff in file
with open(folder_path+'time_diff_orig.txt', 'w') as f:
    for time in time_diff_orig:
        f.write(f"{time}\n")



# Step 1: Create a combined list with distinguishing marks
combined = [(time, 'C') for time in clicks_clean] + [(time, '') for time in time_candidate_clean]

# Step 2: Sort the combined list
combined.sort()

# Step 3: Calculate time differences ignoring 'C' timestamps
time_diff = []
last_time = None

for time, suffix in combined:
    if suffix != 'C':
        if last_time is not None:
            time_diff.append(round(time - last_time,3))
        last_time = time
    else:
        time_diff.append(f"{time}C")
#save time diff in file
with open(folder_path+'time_diff.txt', 'w') as f:
    for time in time_diff:
        f.write(f"{time}\n")

