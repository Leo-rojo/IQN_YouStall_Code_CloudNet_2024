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

real_stalls_length_news=np.load('real_stalls_lengthnews.npy',allow_pickle=True)
stall_lengths_news=np.load('stall_lengthsnews.npy',allow_pickle=True)
real_stalls_length_music=np.load('real_stalls_lengthmusic.npy',allow_pickle=True)
stall_lengths_music=np.load('stall_lengthsmusic.npy',allow_pickle=True)
real_stalls_length_sport=np.load('real_stalls_lengthsport.npy',allow_pickle=True)
stall_lengths_sport=np.load('stall_lengthssport.npy',allow_pickle=True)

#point2
# Compute ECDF for all detected lengths
x_all_rn, y_all_rn = ecdf(real_stalls_length_news)
x_all_dn, y_all_dn = ecdf(stall_lengths_news)
x_all_rm, y_all_rm = ecdf(real_stalls_length_music)
x_all_dm, y_all_dm = ecdf(stall_lengths_music)
x_all_rs, y_all_rs = ecdf(real_stalls_length_sport)
x_all_ds, y_all_ds = ecdf(stall_lengths_sport)

# Plot ECDF for all detected lengths
fig = plt.figure(figsize=(20, 10),dpi=100)
plt.step(x_all_rn, y_all_rn, linewidth='7', color='r', linestyle='-',label='real')
#plt.step(x_all_dn, y_all_dn, linewidth='7', color='black', linestyle='--',label='detected')
plt.step(x_all_rm, y_all_rm, linewidth='7', color='g', linestyle='-',label='real')
#plt.step(x_all_dm, y_all_dm, linewidth='7', color='black', linestyle='--',label='detected')
plt.step(x_all_rs, y_all_rs, linewidth='7', color='b', linestyle='-',label='real')
#plt.step(x_all_ds, y_all_ds, linewidth='7', color='black', linestyle='--',label='detected')
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
plt.tick_params(axis='x', which='major', width=7, length=24)
plt.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 0.25, 0.5, 0.75, 1], ['0', '25', '50', '75', '100'])
plt.xlim(0, 7.5)
plt.xlabel('Stall length')
plt.ylabel('Stall length %')
plt.legend()
plt.savefig('stalllength_distribution_end-to-end_all.pdf',bbox_inches='tight')
plt.savefig('stalllength_distribtuion_end-to-end_all.png',bbox_inches='tight')
plt.close(fig)