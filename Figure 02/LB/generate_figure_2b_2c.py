import matplotlib.pyplot as plt
import numpy as np
import math
font_axes_titles = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 60,
                        }
font_title = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 60,
                        }
font_general = {'family' : 'sans-serif',
                        #'weight' : 'bold',
                        'size'   : 60}
plt.rc('font', **font_general)
music='output_data/Results_music/cL710l090u0_1000Kbps/'
news='output_data/Results_news/mzdfGCdNSHQ_1000Kbps/'
sport='output_data/Results_sport/znN1GoKbPf4_1000Kbps/'
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
            if abs(real_start - detected_start) <= tolerance and detected_end > real_start:
                tp += 1
                detected_associated[i] = True
                detected = True
                detected_length = detected_end - detected_start  # +p   #text does like that but results are worse
                if detected_length == 0:
                    detected_length = p
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
def evaluate_stalls_with_details_filter(real_stalls, stall_stoe, tolerance):
    tp = 0
    fn = 0
    fp = 0

    detected_associated = [False] * len(stall_stoe)
    associations = []
    real_lengths = []
    detected_lengths = []

    # Filter out real stalls with length less than 0.4
    filtered_real_stalls = [(start, end) for start, end in real_stalls if (end - start) >= 0.4]

    for real_start, real_end in filtered_real_stalls:
        detected = False
        real_length = real_end - real_start
        for i, (detected_start, detected_end) in enumerate(stall_stoe):
            if abs(real_start - detected_start) <= tolerance and detected_end > real_start:
                tp += 1
                detected_associated[i] = True
                detected = True
                detected_length = detected_end - detected_start
                if detected_length == 0:
                    detected_length = tolerance
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

for nr,folder_path in enumerate([news, music,sport]):
    if nr==0:
        kind='news'
    elif nr==1:
        kind='music'
    else:
        kind='sport'
    print('----------------'+kind)
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
    # Detection algorithm
    for actual_time_pkt in time_candidate_clean:
        pkt_array.append(actual_time_pkt)
        # Remove packets that are outside the sliding window
        pkt_array = [pkt for pkt in pkt_array if actual_time_pkt - pkt <= DETECTION_TIME_WINDOW]
        if len(pkt_array) >= NR_OF_CLICKS:
            memory='in stall'
            DETECTION_TIME_WINDOW = 0.8
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
    # Create cumulative occurrence arrays
    cumulative_time_candidates = np.arange(1, len(time_candidate_clean) + 1)

    # Plot the cumulative occurrences
    fig = plt.figure(figsize=(20, 10),dpi=100)
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
    #plt.savefig('cumulative_stalldet_'+kind+'.pdf',bbox_inches='tight')
    #plt.savefig('cumulative_stalldet_'+kind+'.png',bbox_inches='tight')
    plt.close(fig)


    #Calculate Real length and Detected length stalls without filtering
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

    #REAL STALL LENGTHS / DETECTED STALL LENGTHS
    print('nr of ground turth stall/nr of detected stalls',len(real_stalls),'/',len(stall_stoe))
    np.save('output_data/real_stalls_length'+str(kind)+'.npy',real_stalls_length)
    np.save('output_data/stall_lengths'+str(kind)+'.npy',stall_lengths)


    ###################################################################################################################
    ##Calculate Real length and Detected length stalls with filtering
    # remove stalls with less than 0.4s
    real_stalls_significance = [stall for stall in real_stalls if stall[1] - stall[0] >= 0.4]
    # no filter small stall
    tolerance = 1
    tp, fn, fp_original, mae, rmse, associations_before = evaluate_stalls_with_details(real_stalls, stall_stoe, tolerance)
    #print('TP before removal of insignificant', tp)

    # filter stall
    tp, fn, fp, mae, rmse, associations_after = evaluate_stalls_with_details_filter(real_stalls, stall_stoe, tolerance)
    stall_detected_after_removal_of_significant = len([assoc for assoc in associations_after if assoc['detected_start'] is not None and assoc['real_start'] is not None])
    print('nr of ground turth stall/nr of actual singificant stalls/nr of detected significant stalls', len(real_stalls_length), '/',len(real_stalls_significance), '/', stall_detected_after_removal_of_significant)
    print('fp_original', fp_original)
    print('fn_deduced', len(real_stalls_significance) - stall_detected_after_removal_of_significant)
    print('tp_deduced', stall_detected_after_removal_of_significant)
    fp = fp_original
    tp = stall_detected_after_removal_of_significant
    fn = len(real_stalls_significance) - stall_detected_after_removal_of_significant
    # print other metrics
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1 Score:', f1)

    real_lengths_filtered = [assoc['real_length'] for assoc in associations_after if assoc['real_start'] is not None and assoc['detected_start'] is not None]
    detected_lengths_filtered = [assoc['detected_length'] for assoc in associations_after if assoc['real_start'] is not None and assoc['detected_start'] is not None]
    np.save('output_data/rl_' + str(kind), real_lengths_filtered)
    np.save('output_data/dl_' + str(kind), detected_lengths_filtered)

    # Calculate RMSE and MAE between detected and real stalls
    rmse_filtered = math.sqrt(sum((r - d) ** 2 for r, d in zip(real_lengths_filtered, detected_lengths_filtered)) / len(real_lengths_filtered))
    mae_filtered = sum(abs(r - d) for r, d in zip(real_lengths_filtered, detected_lengths_filtered)) / len(real_lengths_filtered)
    # measure difference real length detected length
    diff = [np.abs(real_lengths_filtered[i] - detected_lengths_filtered[i]) for i in range(len(real_lengths_filtered))]
    np.save('output_data/stalls_detection_info' + str(kind) + '_filter.npy', diff)
    print('mae', mae_filtered)
    print('rmse', rmse_filtered)

####################################################################################################
#Figure 4b
real_stalls_length_news=np.load('output_data/real_stalls_lengthnews.npy',allow_pickle=True)*1000
stall_lengths_news=np.load('output_data/stall_lengthsnews.npy',allow_pickle=True)*1000
real_stalls_length_music=np.load('output_data/real_stalls_lengthmusic.npy',allow_pickle=True)*1000
stall_lengths_music=np.load('output_data/stall_lengthsmusic.npy',allow_pickle=True)*1000
real_stalls_length_sport=np.load('output_data/real_stalls_lengthsport.npy',allow_pickle=True)*1000
stall_lengths_sport=np.load('output_data/stall_lengthssport.npy',allow_pickle=True)*1000
x_all_rn, y_all_rn = ecdf(real_stalls_length_news)
x_all_dn, y_all_dn = ecdf(stall_lengths_news)
x_all_rm, y_all_rm = ecdf(real_stalls_length_music)
x_all_dm, y_all_dm = ecdf(stall_lengths_music)
x_all_rs, y_all_rs = ecdf(real_stalls_length_sport)
x_all_ds, y_all_ds = ecdf(stall_lengths_sport)
# Plot ECDF for all detected lengths
fig = plt.figure(figsize=(20, 10), dpi=100)
line1, = plt.step(x_all_rn, y_all_rn, linewidth=4, color='m', linestyle='-', label='actual stalls')
line2, = plt.step(x_all_dn, y_all_dn, linewidth=9, color='r', linestyle=':', label='news')
line3, = plt.step(x_all_rm, y_all_rm, linewidth=4, color='m', linestyle='-', label='')
line4, = plt.step(x_all_dm, y_all_dm, linewidth=9, color='g', linestyle='--', label='music')
line5, = plt.step(x_all_rs, y_all_rs, linewidth=4, color='m', linestyle='-', label='')
line6, = plt.step(x_all_ds, y_all_ds, linewidth=9, color='b', linestyle='-.', label='sports')
plt.xlabel('Stall duration, ms')
plt.ylabel('Fraction of stalls')
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # reduce margins between plot and edge
ax = plt.gca()
ax.tick_params(axis='x', which='major', width=7, length=24)
ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.50', '0.75', '1'])
# Get the handles and labels from the plot
handles, labels = ax.get_legend_handles_labels()
# Reorder the legend entries (move 'actual stalls' to the last position)
handles = [line2, line4, line6, line1]  # manually specify the order
labels = ['news', 'music', 'sports', 'actual stalls']
# Add the legend with custom order
plt.legend(handles, labels, frameon=False, markerscale=2, bbox_to_anchor=(0.45, -0.1), loc='lower left')
ax.set_xlim([0, 6800])
plt.savefig('stalllength_distribution_end-to-end_all.pdf', bbox_inches='tight')
plt.savefig('stalllength_distribtuion_end-to-end_all.png', bbox_inches='tight')
plt.close(fig)

#############################################################################
#Figure 4c
associations_news=np.load('output_data/stalls_detection_infonews_filter.npy', allow_pickle=True)
associations_music=np.load('output_data/stalls_detection_infomusic_filter.npy', allow_pickle=True)
associations_sport=np.load('output_data/stalls_detection_infosport_filter.npy', allow_pickle=True)
error_lengths_news = [i*1000 for i in associations_news]
error_lengths_music = [i*1000 for i in associations_music]
error_lengths_sport = [i*1000 for i in associations_sport]
x_all_n, y_all_n = ecdf(error_lengths_news)
x_all_m, y_all_m = ecdf(error_lengths_music)
x_all_s, y_all_s = ecdf(error_lengths_sport)
# Plot ECDF for all detected lengths
fig = plt.figure(figsize=(20, 10), dpi=100)
plt.step(x_all_n, y_all_n, linewidth='9', color='r', linestyle=':',label='news')
plt.step(x_all_m, y_all_m, linewidth='9', color='g', linestyle='--',label='music')
plt.step(x_all_s, y_all_s, linewidth='9', color='b', linestyle='-.',label='sports')
plt.xlabel('Absolute duration error, ms')
plt.ylabel('Fraction of stalls')
plt.legend(frameon=False,markerscale=2)
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
plt.tick_params(axis='x', which='major', width=7, length=24)
plt.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.50', '0.75', '0.1'])
plt.xlim(0, 900)
plt.xticks()
plt.legend(loc='lower right',frameon=False)
plt.savefig('stallserrorsure_distribution_end-to-end_all_filter.pdf', bbox_inches='tight')
plt.savefig('stallserrorsure_distribtuion_end-to-end_all_filter.png', bbox_inches='tight')
plt.close(fig)



################################################################
#print aggregate mae and rmse
rl_news=np.load('output_data/rl_news.npy',allow_pickle=True)
dl_news=np.load('output_data/dl_news.npy',allow_pickle=True)
rl_music=np.load('output_data/rl_music.npy',allow_pickle=True)
dl_music=np.load('output_data/dl_music.npy',allow_pickle=True)
rl_sport=np.load('output_data/rl_sport.npy',allow_pickle=True)
dl_sport=np.load('output_data/dl_sport.npy',allow_pickle=True)
#calculate mae and rmse of the concatenation of rl and dl
real_lengths=np.concatenate((rl_news,rl_music,rl_sport))
detected_lengths=np.concatenate((dl_news,dl_music,dl_sport))
mae = sum(abs(r - d) for r, d in zip(real_lengths, detected_lengths)) / len(real_lengths)
rmse = math.sqrt(sum((r - d) ** 2 for r, d in zip(real_lengths, detected_lengths)) / len(real_lengths))
print('----------------')
print('Aggregate results:')
print('mae',mae)
print('rmse',rmse)