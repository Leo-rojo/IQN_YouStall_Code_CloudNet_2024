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
#for kind in ['news', 'music', 'sport']:
associations_news=np.load('stalls_detection_infonews.npy', allow_pickle=True)
associations_music=np.load('stalls_detection_infomusic.npy', allow_pickle=True)
associations_sport=np.load('stalls_detection_infosport.npy', allow_pickle=True)
# print(len(associations))
# for ass in associations:
#     print(ass)
# Calculate ECDF of the error between detected and real lengths
error_lengths_news = [associations_news[i]['distance_length']*1000 for i in range(len(associations_news))]
error_lengths_music = [associations_music[i]['distance_length']*1000 for i in range(len(associations_music))]
error_lengths_sport = [associations_sport[i]['distance_length']*1000 for i in range(len(associations_sport))]
# error_lengths = np.abs(detected_lengths - real_lengths)
# Compute ECDF for all detected lengths
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
# Customizing the plot to maintain style
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
plt.tick_params(axis='x', which='major', width=7, length=24)
plt.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.50', '0.75', '0.1'])
plt.xticks()
plt.savefig('stallserrorsure_distribution_end-to-end_all.pdf', bbox_inches='tight')
plt.savefig('stallserrorsure_distribtuion_end-to-end_all.png', bbox_inches='tight')
plt.close(fig)