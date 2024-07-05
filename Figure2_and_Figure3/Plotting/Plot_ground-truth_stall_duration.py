import os
import math
import numpy as np
import matplotlib.pyplot as plt

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

os.chdir('/your/path/ISP_user_collaboration/Figure2_and_Figure3')
def read_stalls_from_lines(lines):
    stalls = []
    for i in range(0, len(lines), 2):
        start_time = float(lines[i].strip().split('-')[1])
        end_time = float(lines[i + 1].strip().split('-')[1])
        stalls.append((start_time, end_time))
    return stalls

x_alls = []
y_alls = []
real_stalls_length_all = []
for main_results_directory in ['Results_news/', 'Results_sport/','Results_music/']:
    print(main_results_directory)
    for folder in os.listdir(main_results_directory):
        folder_path = main_results_directory + folder + '/'

        #print(folder_path)

        with open(folder_path + 'Real_stalls.txt', 'r') as f:
            real_stalls_lines = f.readlines()
        real_stalls = read_stalls_from_lines(real_stalls_lines)
        #calculate the stall length
        real_stalls_length = [(end-start)*1000 for start, end in real_stalls]

        print(np.mean(real_stalls_length))
        real_stalls_length_all.extend(real_stalls_length)


        def ecdf(data):
            """Compute ECDF"""
            n = len(data)
            x = np.sort(data)
            y = np.arange(1, n + 1) / n
            return x, y

        x_all, y_all = ecdf(real_stalls_length)
        x_alls.append(x_all)
        y_alls.append(y_all)


# Plot ECDF for all detected lengths
fig = plt.figure(figsize=(20, 10), dpi=100)
plt.step(x_alls[0], y_alls[0], linewidth='9', color='r', linestyle=':', label='news')
plt.step(x_alls[2], y_alls[2], linewidth='9', color='g', linestyle='--', label='music')
plt.step(x_alls[1], y_alls[1], linewidth='9', color='b', linestyle='-.', label='sports')
plt.xlabel('Stall duration, ms')
plt.ylabel('Fraction of stalls')
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
# plt.ylim(2, 70)
#plt.xticks([i for i in range(9)], [str(i) for i in range(9)])
#plt.xlim(0, max(stalls))
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
ax = plt.gca()
ax.tick_params(axis='x', which='major', width=7, length=24)
ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.50', '0.75', '0.1'])
plt.legend(frameon=False,markerscale=2)
ax.set_xlim([0, 6000+800])
plt.savefig('stalls_ecdf.pdf', bbox_inches='tight')
plt.savefig('stalls_ecdf.png', bbox_inches='tight')
plt.close(fig)