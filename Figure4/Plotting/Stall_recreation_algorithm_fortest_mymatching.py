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
music='/home/leonardo/Desktop/In_Band_Quality_Notification_from_End_Users_to_ISPs/Figure4/Results/100_stalls_music_p02_detectorlight/Results_endtoend/cL710l090u0_1000Kbps/p_0.2 w_0.1/'
news='/home/leonardo/Desktop/In_Band_Quality_Notification_from_End_Users_to_ISPs/Figure4/Results/100_stalls_news_p02_detectorlight/Results_endtoend/mzdfGCdNSHQ_1000Kbps/p_0.2 w_0.1/'
sport='/home/leonardo/Desktop/In_Band_Quality_Notification_from_End_Users_to_ISPs/Figure4/Results/100_stalls_sport_p02_detectorlight/Results_endtoend/znN1GoKbPf4_1000Kbps/p_0.2 w_0.1/'

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

for nr,folder_path in enumerate([news, music,sport]):
    if nr==0:
        kind='news'
    elif nr==1:
        kind='music'
    else:
        kind='sport'
    print('----------------'+kind)
    # with open(folder_path+'time_diff_orig.txt', 'r') as f:
    #     time_diff = f.readlines()
    # time_diff_clean = [float(time.strip()) for time in time_diff]
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
        #print(pkt_array)
        # Check for stall detection
        # if len(pkt_array) >= NR_OF_CLICKS:
        #     print("stall")
        #     memory='stall'
        #     DETECTION_TIME_WINDOW = 0.8
        #     stall_nostall.append('r')
        #     #reset_pattern_array()
        # elif len(pkt_array)==1:
        #     print("no stall")
        #     memory='no stall'
        #     DETECTION_TIME_WINDOW = 0.3
        #     stall_nostall.append('b')
        # else:
        #     print(memory)
        #     if memory == 'stall':
        #         DETECTION_TIME_WINDOW = 0.8
        #         stall_nostall.append('r')
        #     else:
        #         DETECTION_TIME_WINDOW = 0.3
        #         stall_nostall.append('b')
        # print(pkt_array)

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

    # Create cumulative occurrence arrays
    cumulative_time_candidates = np.arange(1, len(time_candidate_clean) + 1)

    # Plot the cumulative occurrences
    fig = plt.figure(figsize=(20, 10),dpi=100)
    # Plotting cumulative time candidates
    #plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, label='Candidate packets', marker='o')
    # Plotting cumulative time candidates with colored points
    plt.scatter([t - time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, c=stall_nostall, cmap='coolwarm', label='Candidate packets', marker='o')
    # Adding vertical dotted lines for each start and end time in real_stalls
    for start, end in real_stalls:
        plt.axvline(x=start - time_candidate_clean[0], color='r', linestyle=':', label='Stall Start' if start == real_stalls[0][0] else "")
        plt.axvline(x=end - time_candidate_clean[0], color='b', linestyle=':', label='Stall End' if end == real_stalls[0][1] else "")
    # Adding labels and title
    plt.xlabel('Time in sec respect first candidate packet')
    plt.ylabel('Cumulative Occurrence')
    plt.legend()
    plt.grid(True)
    plt.savefig('cumulative_stalldet_'+kind+'.pdf',bbox_inches='tight')
    plt.savefig('cumulative_stalldet_'+kind+'.png',bbox_inches='tight')


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
    stall_stoe=[]
    stall_detected_sel=[]
    for i in range(len(b_to_r_timestamps)):
        stall_stoe.append((b_to_r_timestamps[i], r_to_b_timestamps[i]))
        if r_to_b_timestamps[i]-b_to_r_timestamps[i]<p:
            stall_lengths.append(r_to_b_timestamps[i]-b_to_r_timestamps[i]+p)#+p)
        else:
            stall_lengths.append(r_to_b_timestamps[i]-b_to_r_timestamps[i])
        stall_detected_sel.append((b_to_r_timestamps[i], r_to_b_timestamps[i], r_to_b_timestamps[i]-b_to_r_timestamps[i])) ###+p


    real_stalls_length = [(end-start) for start, end in real_stalls] #*1000
    real_stalls_sel = [(start,end,end-start) for start, end in real_stalls] #*1000




    import math
    tolerance=1
    def evaluate_stalls_with_details(real_stalls, stall_stoe, tolerance):
        tp = 0
        fn = 0
        fp = 0

        detected_associated = [False] * len(stall_stoe)
        associations = []
        real_lengths = []
        detected_lengths = []

        for real_start, real_end in real_stalls:
            detected = False
            real_length = real_end - real_start
            for i, (detected_start, detected_end) in enumerate(stall_stoe):
                if abs(real_start - detected_start) <= tolerance:
                    tp += 1
                    detected_associated[i] = True
                    detected = True
                    detected_length = detected_end - detected_start #+p   #text does like that but results are worse
                    associations.append({
                        'real_start': real_start,
                        'real_end': real_end,
                        'real_length': real_length,
                        'detected_start': detected_start,
                        'detected_end': detected_end,
                        'detected_length': detected_length
                    })
                    real_lengths.append(real_length)
                    detected_lengths.append(detected_length)
                    break
            if not detected:
                fn += 1
                associations.append({
                    'real_start': real_start,
                    'real_end': real_end,
                    'real_length': real_length,
                    'detected_start': None,
                    'detected_end': None,
                    'detected_length': 0
                })
                real_lengths.append(real_length)
                detected_lengths.append(0)

        for i, (detected_start, detected_end) in enumerate(stall_stoe):
            if not detected_associated[i]:
                fp += 1
                detected_length = detected_end - detected_start
                associations.append({
                    'real_start': None,
                    'real_end': None,
                    'real_length': 0,
                    'detected_start': detected_start,
                    'detected_end': detected_end,
                    'detected_length': detected_length
                })
                real_lengths.append(0)
                detected_lengths.append(detected_length)

        # Calculate MAE and RMSE
        mae = sum(abs(r - d) for r, d in zip(real_lengths, detected_lengths)) / len(real_lengths)
        rmse = math.sqrt(sum((r - d) ** 2 for r, d in zip(real_lengths, detected_lengths)) / len(real_lengths))

        return tp, fn, fp, mae, rmse, associations
    tp, fn, fp, mae, rmse, associations = evaluate_stalls_with_details(real_stalls, stall_stoe, tolerance)

    # print("\nDetailed Associations:")
    # conta=0
    # for assoc in associations:
    #     print(assoc)
    # print('#########')
    # print(real_stalls_sel)
    # print('----')
    # print(stall_detected_sel)
    #     if assoc['detected_start']!=None and assoc['real_start']!=None and assoc['detected_start']<assoc['real_start']:
    #         print(assoc)
    #         conta+=1
    # print(conta)


    #remove from real_stalls and  the one that are less than 0.2
    #real_stalls = [stall for stall in real_stalls if stall[1] - stall[0] >= 0.2]


    # Print the results
    # print(f"True Positives (TP): {tp}")
    # print(f"False Negatives (FN): {fn}")
    # print(f"False Positives (FP): {fp}")
    # print(f"Mean Absolute Error (MAE): {mae}")
    # precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    # recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    # f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    # print(f"Precision: {precision}")
    # print(f"Recall: {recall}")
    # print(f"F1 Score: {f1}")
    # print(f"Root Mean Square Error (RMSE): {rmse}")

    #REAL STALL LENGTHS / DETECTED STALL LENGTHS
    print('nr_gtstall/detstall',len(real_stalls),len(stall_stoe))
    np.save('real_stalls_length'+str(kind)+'.npy',real_stalls_length)
    np.save('stall_lengths'+str(kind)+'.npy',stall_lengths)