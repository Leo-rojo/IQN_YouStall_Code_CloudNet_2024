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

folder_path='/home/leonardo/Desktop/ISP_user_collaboration/End-to-end_reconstruction/Results_endtoend/mzdfGCdNSHQ_1000Kbps/p_0.2 w_0.1/'
def parse_stalls(stall_lines):
    stalls = []
    for i in range(0, len(stall_lines), 2):
        start_time = float(stall_lines[i].strip()[2:])
        end_time = float(stall_lines[i + 1].strip()[2:])
        stalls.append((start_time, end_time))
    return stalls
def read_stalls_from_lines(lines):
    stalls = []
    for i in range(0, len(lines), 2):
        start_time = float(lines[i].strip().split('-')[1])
        end_time = float(lines[i + 1].strip().split('-')[1])
        stalls.append((start_time, end_time))
    return stalls



# with open(folder_path+'time_diff_orig.txt', 'r') as f:
#     time_diff = f.readlines()
# time_diff_clean = [float(time.strip()) for time in time_diff]
with open(folder_path+'timestamp_of_candidate.txt', 'r') as f:
    time_candidate = f.readlines()
time_candidate_clean = [float(time.strip()) for time in time_candidate]





pkt_array=[]
stall_finder=[]
DETECTION_TIME_WINDOW = 0.3
NR_OF_CLICKS = 4
memory='no stall'
stall_nostall = []
for actual_time_pkt in time_candidate_clean:
    pkt_array.append(actual_time_pkt)
    # Remove packets that are outside the sliding window
    pkt_array = [pkt for pkt in pkt_array if actual_time_pkt - pkt <= DETECTION_TIME_WINDOW]
    #print(pkt_array)
    # Check for stall detection
    if len(pkt_array) >= NR_OF_CLICKS:
        print("stall")
        memory='stall'
        DETECTION_TIME_WINDOW = 0.8
        stall_nostall.append('r')
        #reset_pattern_array()
    elif len(pkt_array)==1:
        print("no stall")
        memory='no stall'
        DETECTION_TIME_WINDOW = 0.3
        stall_nostall.append('b')
    else:
        print(memory)
        if memory == 'stall':
            DETECTION_TIME_WINDOW = 0.8
            stall_nostall.append('r')
        else:
            DETECTION_TIME_WINDOW = 0.3
            stall_nostall.append('b')
    print(pkt_array)


# Sort the timestamps
time_candidate_clean.sort()

# Create cumulative occurrence arrays
cumulative_time_candidates = np.arange(1, len(time_candidate_clean) + 1)

# Plot the cumulative occurrences
fig = plt.figure(figsize=(20, 10),dpi=100)
# Plotting cumulative time candidates
#plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, label='Candidate packets', marker='o')
# Plotting cumulative time candidates with colored points
plt.scatter([t - time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, c=stall_nostall, cmap='coolwarm', label='Candidate packets', marker='o')
# Adding labels and title
plt.xlabel('Time in sec respect first candidate packet')
plt.ylabel('Cumulative Occurrence')
plt.legend()
plt.grid(True)
plt.savefig('cumulative_stalldet.pdf',bbox_inches='tight')
plt.savefig('cumulative_stalldet.png',bbox_inches='tight')


# Initialize lists to store change timestamps
b_to_r_timestamps = []
r_to_b_timestamps = []

# Iterate through the stall_nostall array to detect changes
for i in range(1, len(stall_nostall)):
    if stall_nostall[i] != stall_nostall[i-1]:
        # Change detected
        if stall_nostall[i-1] == 'b' and stall_nostall[i] == 'r':
            b_to_r_timestamps.append(time_candidate_clean[i]) #even i-1 can be
        elif stall_nostall[i-1] == 'r' and stall_nostall[i] == 'b':
            r_to_b_timestamps.append(time_candidate_clean[i-1])

if stall_nostall[-1] == 'r':
    r_to_b_timestamps.append(time_candidate_clean[-1])

stall_lengths=[]
stall_lengths_stoe=[]
for i in range(len(b_to_r_timestamps)):
    stall_lengths_stoe.append((b_to_r_timestamps[i],r_to_b_timestamps[i]))
    stall_lengths.append(r_to_b_timestamps[i]-b_to_r_timestamps[i])

with open(folder_path + 'Real_stalls.txt', 'r') as f:
    real_stalls_lines = f.readlines()
real_stalls = read_stalls_from_lines(real_stalls_lines)
real_stalls_length = [(end-start) for start, end in real_stalls] #*1000

#calculate rmse and mae between detected and real stalls
from sklearn.metrics import mean_squared_error, mean_absolute_error
rmse = mean_squared_error(real_stalls_length, stall_lengths, squared=False)
mae = mean_absolute_error(real_stalls_length, stall_lengths)
print(rmse)
print(mae)

# # Combine and sort all change timestamps
# change_timestamps = sorted(b_to_r_timestamps + r_to_b_timestamps)
#
# # Calculate distances between consecutive change timestamps
# time_diffs = np.diff(change_timestamps)
#
# # Print the results
# print("Timestamps where 'b' became 'r':", b_to_r_timestamps)
# print("Timestamps where 'r' became 'b':", r_to_b_timestamps)
# print("All change timestamps:", change_timestamps)
# print("Time differences between consecutive changes:", time_diffs)



















#
#
# #calculate moving average for n=4 packets
# n=4
# time_diff_avg = []
# for i in range(n, len(time_diff_clean)):
#     time_diff_avg.append(np.mean(time_diff_clean[i-n:i]))
#
# #plot the moving average against cumulative points
# # Convert timestamps from string to float
# with open(folder_path+'Detected_clicks.txt', 'r') as f:
#     detected_clicks = f.readlines()
# with open(folder_path+'timestamp_of_candidate.txt', 'r') as f:
#     time_candidate = f.readlines()
# clicks_clean = [click.strip() for click in detected_clicks if click != '----------\n']
# time_candidate_clean = [time.strip() for time in time_candidate]
# clicks_clean = list(map(float, clicks_clean))
# time_candidate_clean = list(map(float, time_candidate_clean))
#
# # Sort the timestamps
# clicks_clean.sort()
# time_candidate_clean.sort()
#
# # Create cumulative occurrence arrays
# cumulative_clicks = np.arange(1, len(clicks_clean) + 1)
# cumulative_time_candidates = np.arange(1, len(time_candidate_clean) + 1)
#
#
# fig = plt.figure(figsize=(20, 10),dpi=100)
# # Plotting cumulative clicks
# plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, label='Candidate packets', marker='o')
# # Plotting moving average
# plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean[n+1:]], time_diff_avg, label='Moving average', marker='o')
# # Adding vertical dashed lines where moving average is greater than 1
# for i in range(len(time_diff_avg)):
#     if time_diff_avg[i] > 0.3:
#         plt.axvline(x=time_candidate_clean[i+ n + 1]  - time_candidate_clean[0], color='r', linestyle='--')  # Adjust x position as needed
#
# # Adding labels and title
# plt.xlabel('Time in sec respect first candidate packet')
# plt.ylabel('Cumulative Occurrence')
# plt.legend()
# plt.grid(True)
#
# plt.savefig('cumulative_movave.pdf',bbox_inches='tight')
# plt.close()
#
#
#
# #calculate exponential moving average for n=4 packets
# n=4
# alpha = 0.8
# # Calculate Exponential Moving Average (EMA) for every n packets
# ema = []
# for i in range(n, len(time_diff_clean) + 1):
#     if i == n:
#         ema.append(np.mean(time_diff_clean[:n]))  # First EMA calculation
#     else:
#         ema.append(ema[-1] + alpha * (time_diff_clean[i - 1] - ema[-1]))  # Subsequent EMA calculations
# # Adding vertical dashed lines where moving average is greater than 1
# for i in range(len(ema)):
#     if ema[i] > 1:
#         plt.axvline(x=time_candidate_clean[i+ n + 1]  - time_candidate_clean[0], color='r', linestyle='--')  # Adjust x position as needed
#
#
# fig = plt.figure(figsize=(20, 10),dpi=100)
# # Plotting cumulative clicks
# plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, label='Candidate packets', marker='o')
# # Plotting exponential moving average
# plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean[n:]], ema, label='Exponential moving average', marker='o')
#
#
# # Adding vertical dashed lines where moving average is greater than 1
# for i in range(len(time_diff_avg)):
#     if time_diff_avg[i] > 0.3:
#         plt.axvline(x=time_candidate_clean[i+ n ]  - time_candidate_clean[0], color='r', linestyle='--')  # Adjust x position as needed
#
# # Adding labels and title
# plt.xlabel('Time in sec respect first candidate packet')
# plt.ylabel('Cumulative Occurrence')
# plt.legend()
# plt.grid(True)
#
# plt.savefig('cumulative_movexpave.pdf',bbox_inches='tight')
#
