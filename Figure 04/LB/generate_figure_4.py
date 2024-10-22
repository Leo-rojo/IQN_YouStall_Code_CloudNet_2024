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
def lighten_color(color, amount=0.5):
    """Lightens the given color by mixing it with white. 'amount' ranges from 0 (no change) to 1 (white)."""
    c = mcolors.to_rgba(color)
    return [(1.0 - amount) * c[i] + amount for i in range(3)] + [1]  # Keep alpha as 1

# Define lighter versions of the colors by mixing them with white
light_red = lighten_color('red', 0.5)  # Lighter red
light_blue = lighten_color('blue', 0.5)  # Lighter blue
light_green = lighten_color('green', 0.5)  # Lighter green

# Load CPU data
cpu2 = np.mean(np.load('output_data/CPU2.npy', allow_pickle=True))
cpu3 = np.mean(np.load('output_data/CPU3.npy', allow_pickle=True))
cpu4 = np.mean(np.load('output_data/CPU4.npy', allow_pickle=True))
cpu5 = np.mean(np.load('output_data/CPU5.npy', allow_pickle=True))
cpu6 = np.mean(np.load('output_data/CPU6.npy', allow_pickle=True))

cpu2_2 = np.mean(np.load('output_data/CPU2_2.npy', allow_pickle=True))
cpu3_2 = np.mean(np.load('output_data/CPU3_2.npy', allow_pickle=True))
cpu4_2 = np.mean(np.load('output_data/CPU4_2.npy', allow_pickle=True))
cpu5_2 = np.mean(np.load('output_data/CPU5_2.npy', allow_pickle=True))
cpu6_2 = np.mean(np.load('output_data/CPU6_2.npy', allow_pickle=True))

cpu2_3 = np.mean(np.load('output_data/CPU2_3.npy', allow_pickle=True))
cpu3_3 = np.mean(np.load('output_data/CPU3_3.npy', allow_pickle=True))
cpu4_3 = np.mean(np.load('output_data/CPU4_3.npy', allow_pickle=True))
cpu5_3 = np.mean(np.load('output_data/CPU5_3.npy', allow_pickle=True))
cpu6_3 = np.mean(np.load('output_data/CPU6_3.npy', allow_pickle=True))

cpu2_4 = np.mean(np.load('output_data/CPU2_4.npy', allow_pickle=True))
cpu3_4 = np.mean(np.load('output_data/CPU3_4.npy', allow_pickle=True))
cpu4_4 = np.mean(np.load('output_data/CPU4_4.npy', allow_pickle=True))
cpu5_4 = np.mean(np.load('output_data/CPU5_4.npy', allow_pickle=True))
cpu6_4 = np.mean(np.load('output_data/CPU6_4.npy', allow_pickle=True))

# Load Memory data
mem2 = np.mean(np.load('output_data/Memory2.npy', allow_pickle=True))
mem3 = np.mean(np.load('output_data/Memory3.npy', allow_pickle=True))
mem4 = np.mean(np.load('output_data/Memory4.npy', allow_pickle=True))
mem5 = np.mean(np.load('output_data/Memory5.npy', allow_pickle=True))
mem6 = np.mean(np.load('output_data/Memory6.npy', allow_pickle=True))

mem2_2 = np.mean(np.load('output_data/Memory2_2.npy', allow_pickle=True))
mem3_2 = np.mean(np.load('output_data/Memory3_2.npy', allow_pickle=True))
mem4_2 = np.mean(np.load('output_data/Memory4_2.npy', allow_pickle=True))
mem5_2 = np.mean(np.load('output_data/Memory5_2.npy', allow_pickle=True))
mem6_2 = np.mean(np.load('output_data/Memory6_2.npy', allow_pickle=True))

mem2_3 = np.mean(np.load('output_data/Memory2_3.npy', allow_pickle=True))
mem3_3 = np.mean(np.load('output_data/Memory3_3.npy', allow_pickle=True))
mem4_3 = np.mean(np.load('output_data/Memory4_3.npy', allow_pickle=True))
mem5_3 = np.mean(np.load('output_data/Memory5_3.npy', allow_pickle=True))
mem6_3 = np.mean(np.load('output_data/Memory6_3.npy', allow_pickle=True))

mem2_4 = np.mean(np.load('output_data/Memory2_4.npy', allow_pickle=True))
mem3_4 = np.mean(np.load('output_data/Memory3_4.npy', allow_pickle=True))
mem4_4 = np.mean(np.load('output_data/Memory4_4.npy', allow_pickle=True))
mem5_4 = np.mean(np.load('output_data/Memory5_4.npy', allow_pickle=True))
mem6_4 = np.mean(np.load('output_data/Memory6_4.npy', allow_pickle=True))

# Convert memory units from bytes to megabytes
mem2 = mem2 / 1024 / 1024
mem3 = mem3 / 1024 / 1024
mem4 = mem4 / 1024 / 1024
mem5 = mem5 / 1024 / 1024
mem6 = mem6 / 1024 / 1024

mem2_2 = mem2_2 / 1024 / 1024
mem3_2 = mem3_2 / 1024 / 1024
mem4_2 = mem4_2 / 1024 / 1024
mem5_2 = mem5_2 / 1024 / 1024
mem6_2 = mem6_2 / 1024 / 1024

mem2_3 = mem2_3 / 1024 / 1024
mem3_3 = mem3_3 / 1024 / 1024
mem4_3 = mem4_3 / 1024 / 1024
mem5_3 = mem5_3 / 1024 / 1024
mem6_3 = mem6_3 / 1024 / 1024

mem2_4 = mem2_4 / 1024 / 1024
mem3_4 = mem3_4 / 1024 / 1024
mem4_4 = mem4_4 / 1024 / 1024
mem5_4 = mem5_4 / 1024 / 1024
mem6_4 = mem6_4 / 1024 / 1024

#####Calculate average and stdev of all CPU and Memory
cpu2 = np.mean([cpu2, cpu2_2, cpu2_3, cpu2_4])
cpu3 = np.mean([cpu3, cpu3_2, cpu3_3, cpu3_4])
cpu4 = np.mean([cpu4, cpu4_2, cpu4_3, cpu4_4])
cpu5 = np.mean([cpu5, cpu5_2, cpu5_3, cpu5_4])
cpu6 = np.mean([cpu6, cpu6_2, cpu6_3, cpu6_4])

cpu2_st = np.std([cpu2, cpu2_2, cpu2_3, cpu2_4])
cpu3_st = np.std([cpu3, cpu3_2, cpu3_3, cpu3_4])
cpu4_st = np.std([cpu4, cpu4_2, cpu4_3, cpu4_4])
cpu5_st = np.std([cpu5, cpu5_2, cpu5_3, cpu5_4])
cpu6_st = np.std([cpu6, cpu6_2, cpu6_3, cpu6_4])

# Calculate average of all Memory
mem2 = np.mean([mem2, mem2_2, mem2_4]) # mem2_3
mem3 = np.mean([mem3, mem3_2, mem3_3, mem3_4])
mem4 = np.mean([mem4, mem4_2, mem4_3, mem4_4])
mem5 = np.mean([mem5, mem5_2, mem5_3, mem5_4])
mem6 = np.mean([mem6, mem6_2, mem6_3, mem6_4])

mem2_st = np.std([mem2, mem2_2, mem2_3, mem2_4])
mem3_st = np.std([mem3, mem3_2, mem3_3, mem3_4])
mem4_st = np.std([mem4, mem4_2, mem4_3, mem4_4])
mem5_st = np.std([mem5, mem5_2, mem5_3, mem5_4])
mem6_st = np.std([mem6, mem6_2, mem6_3, mem6_4])

# Create CPU bar plot
fig_cpu = plt.figure(figsize=(20, 10), dpi=100)
cpu_values = [cpu2, cpu3, cpu4, cpu5, cpu6]
cpu_errors = [cpu2_st, cpu3_st, cpu4_st, cpu5_st, cpu6_st]
bars = plt.bar(['2', '3', '4', '5', '6'], cpu_values, color=light_green, label='CPU Usage, %',width=0.6, yerr=cpu_errors, alpha=1)
# Add different hatches for each bar
hatches = ['//', '\\', '|', '-', '.']  # List of hatches for each bar
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
plt.ylabel('CPU, %', fontdict=font_axes_titles)
plt.xlabel('$\\it{n}$, number of toggles')
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.ylim(0, 23)
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
ax = plt.gca()
ax.tick_params(axis='x', which='major', width=7, length=24)
ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 5, 10, 15, 20])
plt.savefig('cpu_usage_bar.pdf', bbox_inches='tight')
plt.savefig('cpu_usage_bar.png', bbox_inches='tight')
plt.close(fig_cpu)

# Create Memory bar plot
fig_mem = plt.figure(figsize=(20, 10), dpi=100)
mem_values = [mem2, mem3, mem4, mem5, mem6]
mem_errors = [mem2_st, mem3_st, mem4_st, mem5_st, mem6_st]
bars = plt.bar(['2', '3', '4', '5', '6'], mem_values, color=light_blue, label='Memory Usage (MB)',width=0.6, yerr=mem_errors,alpha=1)
# Add different hatches for each bar
hatches = ['//', '\\', '|', '-', '.']  # List of hatches for each bar
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
plt.ylabel('Memory, MB', fontdict=font_axes_titles)
plt.gcf().subplots_adjust(bottom=0.2)  # add space down
plt.gcf().subplots_adjust(left=0.15)  # add space left
plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
ax = plt.gca()
#plt.ylim(0, 205.2)
plt.xlabel('$\\it{n}$, number of toggles')
ax.tick_params(axis='x', which='major', width=7, length=24)
ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.yticks([0, 100, 200, 300])
plt.savefig('memory_usage_bar.pdf', bbox_inches='tight')
plt.savefig('memory_usage_bar.png', bbox_inches='tight')