import numpy as np
import matplotlib.pyplot as plt

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

real_stalls_length_news=np.load('real_stalls_lengthnews.npy',allow_pickle=True)*1000
stall_lengths_news=np.load('stall_lengthsnews.npy',allow_pickle=True)*1000
real_stalls_length_music=np.load('real_stalls_lengthmusic.npy',allow_pickle=True)*1000
stall_lengths_music=np.load('stall_lengthsmusic.npy',allow_pickle=True)*1000
real_stalls_length_sport=np.load('real_stalls_lengthsport.npy',allow_pickle=True)*1000
stall_lengths_sport=np.load('stall_lengthssport.npy',allow_pickle=True)*1000

#point2
# Compute ECDF for all detected lengths
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





# line2, = plt.step(x_all_rn, y_all_rn, linewidth=9, color='r', linestyle=':', label='news')
# line4, = plt.step(x_all_rm, y_all_rm, linewidth=9, color='g', linestyle='--', label='music')
# line6, = plt.step(x_all_rs, y_all_rs, linewidth=9, color='b', linestyle='-.', label='sports')

# line1, = plt.step(x_all_ds, y_all_ds, linewidth=4, color='m', linestyle='-', label='actual stalls')
# line3, = plt.step(x_all_dn, y_all_dn, linewidth=4, color='m', linestyle='-', label='')
# line5, = plt.step(x_all_dm, y_all_dm, linewidth=4, color='m', linestyle='-', label='')



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