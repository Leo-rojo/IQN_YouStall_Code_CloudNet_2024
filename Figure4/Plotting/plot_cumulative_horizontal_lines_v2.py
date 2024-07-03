import matplotlib.pyplot as plt
import numpy as np
font_axes_titles = {'family': 'sans-serif', 'color': 'black', 'size': 60}
font_title = {'family': 'sans-serif', 'color': 'black', 'size': 60}
font_general = {'family': 'sans-serif', 'size': 60}
plt.rc('font', **font_general)
# music='/home/leonardo/Desktop/ISP_user_collaboration/Figure4/100_stalls_music_p02_detectorlight/Results_endtoend/cL710l090u0_1000Kbps/p_0.2 w_0.1/'
# news='/home/leonardo/Desktop/ISP_user_collaboration/Figure4/100_stalls_news_p02_detectorlight/Results_endtoend/mzdfGCdNSHQ_1000Kbps/p_0.2 w_0.1/'
# sport='/home/leonardo/Desktop/ISP_user_collaboration/Figure4/100_stalls_sport_p02_detectorlight/Results_endtoend/znN1GoKbPf4_1000Kbps/p_0.2 w_0.1/'
#folder_path='/home/leonardo/Desktop/ISP_user_collaboration/Figure4/Results_endtoend/znN1GoKbPf4_1000Kbps/p_0.2 w_0.1/'
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
folder='/home/leonardo/Desktop/ISP_user_collaboration/cumulative_packets_click_experiment/Results_cumul_decoupled/mzdfGCdNSHQ_1000Kbps/p_0.2 w_0.1/'
for folder_path in [folder]:
    with open(folder_path+'timestamp_of_candidate.txt', 'r') as f:
        time_candidate = f.readlines()
    time_candidate_clean = [float(time.strip()) for time in time_candidate]
    pkt_array=[]
    stall_finder=[]
    p=0.2
    DETECTION_TIME_WINDOW = 0.3
    NR_OF_CLICKS = 4
    memory='out of stall'
    stall_nostall = []
    for actual_time_pkt in time_candidate_clean:
        pkt_array.append(actual_time_pkt)
        # Remove packets that are outside the sliding window
        pkt_array = [pkt for pkt in pkt_array if actual_time_pkt - pkt <= DETECTION_TIME_WINDOW]
        if len(pkt_array) >= NR_OF_CLICKS:
            #print("stall")
            memory='in stall'
            DETECTION_TIME_WINDOW = 0.8
            stall_nostall.append('r')
            #reset_pattern_array()
        # elif len(pkt_array)==1:
        #     print("no stall")
        #     memory='no stall'
        #     DETECTION_TIME_WINDOW = 0.3
        #     stall_nostall.append('b')
        else:
            #print(memory)
            if memory == 'in stall':
                #print("no stall")
                memory='no stall'
                DETECTION_TIME_WINDOW = 0.3
                stall_nostall.append('b')
            else:
                DETECTION_TIME_WINDOW = 0.3
                stall_nostall.append('b')
        #print(pkt_array)

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
    # Plotting cumulative time candidates with colored points

    # Adding horizontal lines at the top and bottom
    # Adding specific horizontal lines at the top and bottom
    # line_length_top = 2.0  # Length of the top line in x-axis units
    # line_length_bottom = 3.0  # Length of the bottom line in x-axis units
    # x_start_top = 0.1  # Starting x position for the top line
    # x_start_bottom = 0.1  # Starting x position for the bottom line
    y_position_top = max(cumulative_time_candidates[:limit]) + 500  # Y position for the top line
    y_position_bottom = -500  # Y position for the bottom line
    # Plot real stalls
    # for i in [0,2,3,4,5,6,7]:
    #     label = 'actual stall' if i == 0 else ""
    #     start, end = real_stalls[i]
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
    # for i in [0,1,2,3,4,5,6]:
    #     label = 'inferred stall' if i == 0 else ""
    #     start_d, end_d = stall_stoe[i]
    #     plt.plot([start_d - time_candidate_clean[0], end_d - time_candidate_clean[0]], [y_position_bottom, y_position_bottom], color='blue', linewidth=15, label=label)

    # for det_start, det_end in
    # plt.plot([x_start_bottom, x_start_bottom + line_length_bottom], [y_position_bottom, y_position_bottom], color='black', linewidth=2)

    #Adding vertical dotted lines for each start and end time in real_stalls
    # for start, end in real_stalls:
    #     plt.axvline(x=start - time_candidate_clean[0], color='r', linestyle=':', label='Stall Start' if start == real_stalls[0][0] else "")
    #     plt.axvline(x=end - time_candidate_clean[0], color='b', linestyle=':', label='Stall End' if end == real_stalls[0][1] else "")
    # Adding labels and title
    plt.xlabel('Time, s')
    plt.yticks([])
    plt.ylim(y_position_bottom - 1100, y_position_top + 1100)  # Adjust the padding as needed
    #plt.ylabel('Cumulative Occurrence')
    plt.gcf().subplots_adjust(bottom=0.2)  # add space down
    plt.gcf().subplots_adjust(left=0.15)  # add space left
    #plt.subplots_adjust(left=-0.25)
    plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
    plt.tick_params(axis='x', which='major', width=7, length=24)
    plt.tick_params(axis='y', which='major', width=7, length=24, pad=20)
    #plt.legend(fontsize=35, markerscale=2, bbox_to_anchor=(0.0, 0.45), loc='lower left')
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