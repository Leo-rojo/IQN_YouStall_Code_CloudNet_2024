import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
mpl.rc('hatch', color='k', linewidth=3)

font_axes_titles = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 70,
                        }
font_title = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 70,
                        }
font_general = {'family' : 'sans-serif',
                        #'weight' : 'bold',
                        'size'   : 70}
plt.rc('font', **font_general)

def read_stalls_from_lines(lines):
    stalls = []
    for i in range(0, len(lines), 2):
        start_time = float(lines[i].strip().split('-')[1])
        end_time = float(lines[i + 1].strip().split('-')[1])
        stalls.append((start_time, end_time))
    return stalls
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
def evaluate_stalls_with_details(real_stalls, detected_stalls, tolerance):
    tp = 0
    fn = 0
    fp = 0

    detected_associated = [False] * len(detected_stalls)
    associations = []
    real_lengths = []
    detected_lengths = []

    for real_start, real_end in real_stalls:
        detected = False
        real_length = real_end - real_start
        for i, (detected_start, detected_end) in enumerate(detected_stalls):
            if abs(real_start - detected_start) <= tolerance:
                tp += 1
                detected_associated[i] = True
                detected = True
                detected_length = detected_end - detected_start
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

    for i, (detected_start, detected_end) in enumerate(detected_stalls):
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
def count_events_in_windows(stalls, detected_clicks, WINDOW_SIZE):
    # Convert detected clicks to float, ignoring '----------'
    detector_1_timestamps = [float(click.strip()) for click in detected_clicks if click.strip() != '----------']

    results = []
    used_detectors = set()

    for start, end in stalls:
        window_end = end + WINDOW_SIZE
        # Count detections within the window
        detector_count = sum(start <= detector <= window_end for detector in detector_1_timestamps)
        results.append((start, end, detector_count))

        # Mark detectors that fall within the window as used
        used_detectors.update(detector for detector in detector_1_timestamps if start <= detector <= window_end)

    # Calculate false positives
    false_positive_detectors = len(detector_1_timestamps) - len(used_detectors)
    false_positive_detector_timestamps = [detector for detector in detector_1_timestamps if detector not in used_detectors]

    return results, false_positive_detectors, false_positive_detector_timestamps
def parse_detected_clicks(detected_clicks):
    parsed_clicks = []
    for click in detected_clicks:
        prefix, timestamp = click.split('-')
        timestamp = float(timestamp.strip())
        parsed_clicks.append((prefix, timestamp))
    return parsed_clicks
def count_timestamps(parsed_clicks, stalls, tolerance_out, tolerance_in):
    N_in = 0
    N_out = 0
    S_in = 0
    S_out = 0

    for prefix, timestamp in parsed_clicks:
        in_stall = any(start-tolerance_in <= timestamp <= end+tolerance_out for start, end in stalls)
        if prefix == 'N':
            if in_stall:
                N_in += 1
            else:
                N_out += 1
        elif prefix == 'S':
            if in_stall:
                S_in += 1
            else:
                S_out += 1

    return {
        "True Positives (S in)": S_in,
        "True Negatives (N out)": N_out,
        "False Positives (S out)": S_out,
        "False Negatives (N in)": N_in
    }

x_alls = []
y_alls = []
for main_results_directory in ['Results_news','Results_music','Results_sport']:#,'Results_music','Results_sport']:#'Results_news','Results_music','Results_sport']:#, 'Results_sport','Results_music']:
    for folder in os.listdir('../Results/'+main_results_directory+'/'):
        folder_path = '../Results/'+main_results_directory+'/' + folder + '/'
        with open(folder_path + 'Real_stalls.txt', 'r') as f:
            real_stalls_lines = f.readlines()
        real_stalls_parsed = parse_stalls(real_stalls_lines)
        #calculate the stall length
        #real_stalls_length = [(end-start)*1000 for start, end in real_stalls]
        save_precision = []
        save_recall = []
        for i in [0.2,0.4,0.8,1.2,1.6,2.0]:

            folder_path_txts = folder_path +'p_'+str(i)+'/' #+'/Detected_stalls.'+str(i)+'txt'
            print(folder_path_txts)

            with open(folder_path_txts + 'Detected_clicks_'+str(i)+'.txt', 'r') as f:
                detected_clicks = f.readlines()

            parsed_clicks = parse_detected_clicks(detected_clicks)
            results = count_timestamps(parsed_clicks, real_stalls_parsed, 0.25, 0)

            if (results["True Positives (S in)"] + results["False Positives (S out)"]) == 0:
                precision = 0
            else:
                precision = results["True Positives (S in)"] / (results["True Positives (S in)"] + results["False Positives (S out)"])

            if (results["True Positives (S in)"] + results["False Negatives (N in)"]) == 0:
                recall = 0
            else:
                recall = results["True Positives (S in)"] / (results["True Positives (S in)"] + results["False Negatives (N in)"])

            # if (precision + recall) == 0:
            #     f1 = 0
            # else:
            #     f1 = 2 * (precision * recall) / (precision + recall)

            print("True Positives (S in):", results["True Positives (S in)"])
            print("True Negatives (N out):", results["True Negatives (N out)"])
            print("False Positives (S out):", results["False Positives (S out)"])
            print("False Negatives (N in):", results["False Negatives (N in)"])
            #print("Accuracy:", accuracy)
            print("Precision:", precision)
            print("Recall:", recall)
            #print("F1 Score:", f1)
            save_precision.append(precision)
            save_recall.append(recall)

        np.save('precision_stalls_'+main_results_directory+'.npy', save_precision)
        np.save('recall_stalls_'+main_results_directory+'.npy', save_recall)

# Load the precision data
precision_news = np.load('precision_stalls_Results_news.npy', allow_pickle=True)
precision_sport = np.load('precision_stalls_Results_sport.npy', allow_pickle=True)
precision_music = np.load('precision_stalls_Results_music.npy', allow_pickle=True)

# Define the number of groups and bars per group
n_groups = len(precision_news)  # Assuming all arrays have the same length
n_bars = 3

# Create the plot
fig, ax = plt.subplots(figsize=(20, 10), dpi=100)

# Set the bar width
bar_width = 0.2
index = np.arange(n_groups)

def lighten_color(color, amount=0.5):
    """Lightens the given color by mixing it with white. 'amount' ranges from 0 (no change) to 1 (white)."""
    c = mcolors.to_rgba(color)
    return [(1.0 - amount) * c[i] + amount for i in range(3)] + [1]  # Keep alpha as 1

# Define lighter versions of the colors by mixing them with white
light_red = lighten_color('red', 0.5)  # Lighter red
light_blue = lighten_color('blue', 0.5)  # Lighter blue
light_green = lighten_color('green', 0.5)  # Lighter green

# Plot bars for each category with lighter colors and hatches
bar1 = ax.bar(index, precision_news, bar_width, label='News', color=light_red, hatch='//', alpha=1)  # Lighter red with diagonal lines
bar2 = ax.bar(index + 2 * bar_width, precision_sport, bar_width, label='Sport', color=light_blue, hatch='\\', alpha=1)  # Lighter blue with opposite diagonal lines
bar3 = ax.bar(index + bar_width, precision_music, bar_width, label='Music', color=light_green, hatch='.', alpha=1)  # Lighter green with star pattern

# Add labels, title, and legend
ax.set_xlabel('Sampling period $\\it{p}$, ms')
ax.set_ylabel('Precision, %')
ax.set_xticks(index + bar_width)
ax.set_xticklabels([str(i) for i in range(n_groups)])

# Customizing the plot to maintain style
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
ax.tick_params(axis='x', which='major', width=7, length=24)
ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '25', '50', '75', '100'])
plt.xticks([0.2, 1.2, 2.2, 3.2, 4.2, 5.2], ['200', '400', '800', '1200', '1600', '2000'])
# plt.legend(frameon=False, markerscale=2)

# Save the plot as PDF and PNG
plt.savefig('precision.pdf', bbox_inches='tight')
plt.savefig('precision.png', bbox_inches='tight')
plt.close(fig)

###############################recall
# Load the precision data
precision_news = np.load('recall_stalls_Results_news.npy', allow_pickle=True)
precision_sport = np.load('recall_stalls_Results_sport.npy', allow_pickle=True)
precision_music = np.load('recall_stalls_Results_music.npy', allow_pickle=True)

# Define the number of groups and bars per group
n_groups = len(precision_news)  # Assuming all arrays have the same length
n_bars = 3

# Create the plot
fig, ax = plt.subplots(figsize=(20, 10), dpi=100)

# Set the bar width
bar_width = 0.2
index = np.arange(n_groups)

# Plot bars for each category with hatches and no transparency
bar1 = ax.bar(index, precision_news, bar_width, label='News', color=light_red, hatch='//', alpha=1)  # Diagonal lines pattern, no transparency
bar2 = ax.bar(index + 2 * bar_width, precision_sport, bar_width, label='Sport', color=light_blue, hatch='\\', alpha=1)  # Opposite diagonal lines, no transparency
bar3 = ax.bar(index + bar_width, precision_music, bar_width, label='Music', color=light_green, hatch='.', alpha=1)  # Star pattern, no transparency

# Add labels, title, and legend
ax.set_xlabel('Sampling period $\\it{p}$, ms')
ax.set_ylabel('Recall, %')
ax.set_xticks(index + bar_width)
ax.set_xticklabels([str(i) for i in range(n_groups)])

# Customizing the plot to maintain style
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
ax.tick_params(axis='x', which='major', width=7, length=24)
ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '25', '50', '75', '100'])
plt.xticks([0.2, 1.2, 2.2, 3.2, 4.2, 5.2], ['200', '400', '800', '1200', '1600', '2000'])
# plt.legend(frameon=False, markerscale=2)

# Save the plot as PDF and PNG
plt.savefig('recall.pdf', bbox_inches='tight')
plt.savefig('recall.png', bbox_inches='tight')
plt.close(fig)