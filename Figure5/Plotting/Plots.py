import numpy as np
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

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
os.chdir('/home/leonardo/Desktop/ISP_user_collaboration/Figure5')
cpu2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU2.npy', allow_pickle=True))
cpu2_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU2.npy', allow_pickle=True))
cpu3=np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU3.npy', allow_pickle=True)
cpu4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU4.npy', allow_pickle=True))
cpu4_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU4.npy', allow_pickle=True))
cpu5=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU5.npy', allow_pickle=True))
cpu5_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU5.npy', allow_pickle=True))
cpu6=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU6.npy', allow_pickle=True))
cpu6_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU6.npy', allow_pickle=True))
mem2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory2.npy', allow_pickle=True))
mem2_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory2.npy', allow_pickle=True))
mem3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory3.npy', allow_pickle=True))
mem3_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory3.npy', allow_pickle=True))
mem4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory4.npy', allow_pickle=True))
mem4_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory4.npy', allow_pickle=True))
mem5=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory5.npy', allow_pickle=True))
mem5_long=(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory5.npy', allow_pickle=True))
mem5_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory5.npy', allow_pickle=True))
mem6=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory6.npy', allow_pickle=True))
mem6_st=np.std(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory6.npy', allow_pickle=True))
#####2
cpu2_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU2_2.npy', allow_pickle=True))
cpu3_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU3_2.npy', allow_pickle=True))
cpu4_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU4_2.npy', allow_pickle=True))
cpu5_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU5_2.npy', allow_pickle=True))
cpu6_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU6_2.npy', allow_pickle=True))
####3
cpu2_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU2_3.npy', allow_pickle=True))
cpu3_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU3_3.npy', allow_pickle=True))
cpu4_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU4_3.npy', allow_pickle=True))
cpu5_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU5_3.npy', allow_pickle=True))
cpu6_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU6_3.npy', allow_pickle=True))
####4
cpu2_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU2_4.npy', allow_pickle=True))
cpu3_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU3_4.npy', allow_pickle=True))
cpu4_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU4_4.npy', allow_pickle=True))
cpu5_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU5_4.npy', allow_pickle=True))
cpu6_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/CPU6_4.npy', allow_pickle=True))
####mem 2
mem2_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory2_2.npy', allow_pickle=True))
mem3_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory3_2.npy', allow_pickle=True))
mem4_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory4_2.npy', allow_pickle=True))
mem5_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory5_2.npy', allow_pickle=True))
mem6_2=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory6_2.npy', allow_pickle=True))
####mem 3
mem2_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory2_3.npy', allow_pickle=True))
mem3_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory3_3.npy', allow_pickle=True))
mem4_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory4_3.npy', allow_pickle=True))
mem5_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory5_3.npy', allow_pickle=True))
mem6_3=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory6_3.npy', allow_pickle=True))
####mem 4
mem2_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory2_4.npy', allow_pickle=True))
mem3_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory3_4.npy', allow_pickle=True))
mem4_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory4_4.npy', allow_pickle=True))
mem5_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory5_4.npy', allow_pickle=True))
mem6_4=np.mean(np.load('/home/leonardo/Desktop/ISP_user_collaboration/Figure5/Results/Memory6_4.npy', allow_pickle=True))


mem2=mem2/1024/1024
mem3=mem3/1024/1024
mem4=mem4/1024/1024
mem6=mem6/1024/1024
mem2_2=mem2_2/1024/1024
mem3_2=mem3_2/1024/1024
mem4_2=mem4_2/1024/1024
mem6_2=mem6_2/1024/1024
mem2_3=mem2_3/1024/1024
mem3_3=mem3_3/1024/1024
mem4_3=mem4_3/1024/1024
mem6_3=mem6_3/1024/1024
mem5_2=mem5_2/1024/1024
mem5_3=mem5_3/1024/1024
mem2_st=mem2_st/1024/1024
mem3_st=mem3_st/1024/1024
mem4_st=mem4_st/1024/1024
mem5_st=mem5_st/1024/1024
mem2_4=mem2_4/1024/1024
mem3_4=mem3_4/1024/1024
mem4_4=mem4_4/1024/1024
mem5_4=mem5_4/1024/1024
mem6_4=mem6_4/1024/1024




# mem1=mem1/1024/1024
# mem2=mem2/1024/1024

#calcualte average of all CPU
#mean of only positive numbers for cpu3
cpu3 = np.mean([i for i in cpu3 if i > 0])
mem5 = np.mean([i for i in mem5_long if i > 0])
mem5=mem5/1024/1024
#cpu3_st = np.std([i for i in cpu3 if i > 0])
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
#mem
mem2 = np.mean([mem2, mem2_2,mem2_4])# mem2_3
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

#cpu_errors = [cpu2_st, cpu3_st, cpu4_st, cpu5_st, cpu6_st]
plt.bar(['2', '3', '4', '5', '6'], cpu_values, color='r', label='CPU Usage, %',width=0.6, yerr=cpu_errors,)
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
plt.savefig('cpu_usage_bar_4.pdf', bbox_inches='tight')
plt.savefig('cpu_usage_bar_4.png', bbox_inches='tight')
plt.close(fig_cpu)

# Create Memory bar plot
fig_mem = plt.figure(figsize=(20, 10), dpi=100)
mem_values = [mem2, mem3, mem4, mem5, mem6]
mem_errors = [mem2_st, mem3_st, mem4_st, mem5_st, mem6_st]
#mem_errors = [mem2_st, mem3_st, mem4_st, mem5_st, mem6_st]
plt.bar(['2', '3', '4', '5', '6'], mem_values, color='r', label='Memory Usage (MB)',width=0.6, yerr=mem_errors,)
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
plt.savefig('memory_usage_bar_4.pdf', bbox_inches='tight')
plt.savefig('memory_usage_bar_4.png', bbox_inches='tight')


##################











#
# # Create a figure for plotting
# fig = plt.figure(figsize=(20, 10), dpi=100)
# # Plot CPU and memory usage
# iterations = np.arange(len(cpu_perc))
# plt.plot(iterations, cpu_perc, label='CPU Usage (%)', color='r', linewidth=7)
# plt.fill_between(iterations, np.array(cpu_perc) - cpu_std, np.array(cpu_perc) + cpu_std, alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
# # Set labels and title
# plt.xlabel("Seconds", fontdict=font_axes_titles)
# plt.ylabel('CPU percentage', fontdict=font_axes_titles)
# # # Customize ticks and margins
# plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
# # plt.yticks(range(0, 110, 20))
# # plt.gcf().subplots_adjust(bottom=0.2)
# # plt.margins(0.02, 0.01)
# # # Customize axis ticks
# # ax = plt.gca()
# # ax.tick_params(axis='x', which='major', width=7, length=24)
# # ax.tick_params(axis='y', which='major', width=7, length=24)
# # ax.set_ylim([0, 100])
# #
# # # Add a legend
# # plt.legend()
# plt.gcf().subplots_adjust(bottom=0.2)  # add space down
# plt.gcf().subplots_adjust(left=0.15)  # add space left
# #plt.ylim(2, 70)
# #plt.xticks([i for i in range(9)], [str(i) for i in range(9)])
# #plt.xlim(0, max(stalls))
# plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
# ax = plt.gca()
# ax.tick_params(axis='x', which='major', width=7, length=24)
# ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
# plt.yticks([0, 5, 10, 15, 20, 25], ['0', '5', '10', '15', '20', '25'])
# #ax.set_xlim([0, max(stalls)+0.5])
# # Save the plot
# plt.savefig('cpu_percentage.pdf',bbox_inches='tight')
# plt.savefig('cpu_percentage.png',bbox_inches='tight')
# plt.close(fig)
#
# #####################
#
# # Create a figure for plotting
# fig = plt.figure(figsize=(20, 10), dpi=100)
# # Plot CPU and memory usage
# plt.plot(iterations, memory_perc, label='Memory Usage (%)', color='r', linewidth=7)
# # Set labels and title
# plt.xlabel("Seconds", fontdict=font_axes_titles)
# plt.ylabel('Memory in MB', fontdict=font_axes_titles)
# # # Customize ticks and margins
# plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
# # plt.yticks(range(0, 110, 20))
# # plt.gcf().subplots_adjust(bottom=0.2)
# # plt.margins(0.02, 0.01)
# # # Customize axis ticks
# # ax = plt.gca()
# # ax.tick_params(axis='x', which='major', width=7, length=24)
# # ax.tick_params(axis='y', which='major', width=7, length=24)
# # ax.set_ylim([0, 100])
# #
# # # Add a legend
# # plt.legend()
# plt.gcf().subplots_adjust(bottom=0.2)  # add space down
# plt.gcf().subplots_adjust(left=0.15)  # add space left
# #plt.ylim(2, 70)
# #plt.xticks([i for i in range(9)], [str(i) for i in range(9)])
# #plt.xlim(0, max(stalls))
# plt.margins(0.02, 0.01)  # riduci margini tra plot e bordo
# ax = plt.gca()
# ax.tick_params(axis='x', which='major', width=7, length=24)
# ax.tick_params(axis='y', which='major', width=7, length=24, pad=20)
# plt.yticks([0, 50, 100, 150, 200], ['0', '50', '100', '150', '200'])
# # Save the plot
# plt.savefig('memory_percentage.pdf',bbox_inches='tight')
# plt.savefig('memory_percentage.png',bbox_inches='tight')
# plt.close(fig)
