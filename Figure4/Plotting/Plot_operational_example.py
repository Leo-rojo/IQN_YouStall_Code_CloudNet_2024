import matplotlib.pyplot as plt
import numpy as np
font_axes_titles = {'family': 'sans-serif', 'color': 'black', 'size': 60}
font_title = {'family': 'sans-serif', 'color': 'black', 'size': 60}
font_general = {'family': 'sans-serif', 'size': 60}
plt.rc('font', **font_general)
def ecdf(data):
    """Compute ECDF"""
    n = len(data)
    x = np.sort(data)
    y = np.arange(1, n + 1) / n
    return x, y
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

folder_path = '../Results/Operational_example/'
with open(folder_path+'timestamp_of_candidate.txt', 'r') as f:
    time_candidate = f.readlines()
time_candidate_clean = [float(time.strip()) for time in time_candidate]
pkt_array=[]
stall_finder=[]
p=0.2
DETECTION_TIME_WINDOW = 0.3 #3/2*p
NR_OF_CLICKS = 4
memory='out of stall'
stall_nostall = []

#Detection algorithm of ISP agent
for actual_time_pkt in time_candidate_clean:
    pkt_array.append(actual_time_pkt)
    # Remove packets that are outside the sliding window
    pkt_array = [pkt for pkt in pkt_array if actual_time_pkt - pkt <= DETECTION_TIME_WINDOW]
    if len(pkt_array) >= NR_OF_CLICKS:
        memory='in stall'
        DETECTION_TIME_WINDOW = 0.8 #4*p
        stall_nostall.append('r')
    else:
        if memory == 'in stall':
            memory='no stall'
            DETECTION_TIME_WINDOW = 0.3
            stall_nostall.append('b')
        else:
            DETECTION_TIME_WINDOW = 0.3
            stall_nostall.append('b')

with open(folder_path + 'Real_stalls.txt', 'r') as f:
    real_stalls_lines = f.readlines()
real_stalls = read_stalls_from_lines(real_stalls_lines)

# Sort the timestamps
time_candidate_clean.sort()

# Initialize lists to store change timestamps
b_to_r_timestamps = []
r_to_b_timestamps = []

# Iterate through the stall_nostall array to detect changes
for i in range(1, len(stall_nostall)):
    if stall_nostall[i] != stall_nostall[i - 1]:
        # Change detected
        if stall_nostall[i - 1] == 'b' and stall_nostall[i] == 'r':
            b_to_r_timestamps.append(time_candidate_clean[i])  # even i-1 can be
        elif stall_nostall[i - 1] == 'r' and stall_nostall[i] == 'b':
            r_to_b_timestamps.append(time_candidate_clean[i - 1])

if stall_nostall[-1] == 'r':
    r_to_b_timestamps.append(time_candidate_clean[-1])

stall_lengths = []
stall_stoe = []
stall_detected_sel = []
for i in range(len(b_to_r_timestamps)):
    stall_stoe.append((b_to_r_timestamps[i], r_to_b_timestamps[i]))
    stall_lengths.append(r_to_b_timestamps[i] - b_to_r_timestamps[i])
    stall_detected_sel.append(
        (b_to_r_timestamps[i], r_to_b_timestamps[i], r_to_b_timestamps[i] - b_to_r_timestamps[i]))

# Create cumulative occurrence arrays
cumulative_time_candidates = np.arange(1, len(time_candidate_clean) + 1)
limit=4200
# Plot the cumulative occurrences
fig = plt.figure(figsize=(20, 10),dpi=100)
y_position_top = max(cumulative_time_candidates[:limit]) + 500  # Y position for the top line
y_position_bottom = -500  # Y position for the bottom line
plt.plot([10,14.5], [y_position_top, y_position_top], color='m', linewidth=11, label='actual stall')
plt.plot([19.3, 20], [y_position_top, y_position_top], color='m', linewidth=11)  # , label=label)
plt.plot([21.5, 23], [y_position_top, y_position_top], color='m', linewidth=11)  # , label=label)
plt.plot([27, 29], [y_position_top, y_position_top], color='m', linewidth=11)  # , label=label)
plt.plot([35, 38], [y_position_top, y_position_top], color='m', linewidth=11)  # , label=label)
plt.scatter([t - time_candidate_clean[0] for t in time_candidate_clean[:limit]], cumulative_time_candidates[:limit],color='black', label='candidate packet', marker='o', s=100)  # c=stall_nostall[:limit],
plt.plot([10, 14.5], [y_position_bottom, y_position_bottom], color='orange', linewidth=9, label='inferred stall')
plt.plot([19.3, 20], [y_position_bottom, y_position_bottom], color='orange', linewidth=9)  # , label=label)
plt.plot([21.5, 23], [y_position_bottom, y_position_bottom], color='orange', linewidth=9)  # , label=label)
plt.plot([27, 29], [y_position_bottom, y_position_bottom], color='orange', linewidth=9)  # , label=label)
plt.plot([35, 38], [y_position_bottom, y_position_bottom], color='orange', linewidth=9)  # , label=label)
plt.xlabel('Time, s')
plt.yticks([])
plt.ylim(y_position_bottom - 1100, y_position_top + 1100)  # Adjust the padding as needed
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
plt.tick_params(axis='x', which='major', width=7, length=24)
plt.tick_params(axis='y', which='major', width=7, length=24, pad=20)
text_x = 15
text_y = -1600
plt.text(text_x, text_y, 'inferred stalls', ha='left', va='bottom', fontsize=60,)
text_x = 15
text_y = 4800
plt.text(text_x, text_y, 'actual stalls', ha='left', va='bottom', fontsize=60, )
text_x = -0.6
text_y = 2300
plt.text(text_x, text_y, 'candidate packets', ha='left', va='bottom', fontsize=60, )
plt.savefig('operation_example.pdf',bbox_inches='tight')
plt.savefig('operation_example.png',bbox_inches='tight')