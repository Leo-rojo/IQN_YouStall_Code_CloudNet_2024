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


os.chdir('/home/leonardo/Desktop/ISP_user_collaboration/Stall_detection_abl_bar')

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

# Plot bars for each category
bar1 = ax.bar(index, precision_news, bar_width, label='News', color='r')
bar2 = ax.bar(index + 2*bar_width, precision_sport, bar_width, label='Sport', color='b')
bar3 = ax.bar(index +  bar_width, precision_music, bar_width, label='Music', color='g')

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
plt.xticks([0.2,1.2,2.2,3.2,4.2,5.2], ['200', '400', '800', '1200','1600', '2000'])
#plt.legend(frameon=False, markerscale=2)

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

# Plot bars for each category
bar1 = ax.bar(index, precision_news, bar_width, label='News', color='r')
bar2 = ax.bar(index + 2* bar_width, precision_sport, bar_width, label='Sport', color='b')
bar3 = ax.bar(index + bar_width, precision_music, bar_width, label='Music', color='g')

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
plt.xticks([0.2,1.2,2.2,3.2,4.2,5.2], ['200', '400', '800', '1200','1600', '2000'])
#plt.legend(frameon=False, markerscale=2)

# Save the plot as PDF and PNG
plt.savefig('recall.pdf', bbox_inches='tight')
plt.savefig('recall.png', bbox_inches='tight')
plt.close(fig)

