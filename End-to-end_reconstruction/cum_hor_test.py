import matplotlib.pyplot as plt
import numpy as np

font_axes_titles = {'family': 'sans-serif', 'color': 'black', 'size': 60}
font_title = {'family': 'sans-serif', 'color': 'black', 'size': 60}
font_general = {'family': 'sans-serif', 'size': 60}
plt.rc('font', **font_general)

# Parameters
total_points = 100  # Total number of points
base_start = 1719349000  # Start of the timestamp range
base_end = 1719350000  # End of the timestamp range

# Burst parameters
burst_density = 0.1  # Higher value means denser bursts
burst1_start_idx = 45  # Index in the base array where the first burst starts (shifted further)
burst1_end_idx = 55    # Index in the base array where the first burst ends (shifted further)
burst2_start_idx = 70  # Index in the base array where the second burst starts
burst2_end_idx = 75    # Shorter burst for the second burst (adjusted length)

# Generate base array excluding burst regions
base_before_burst1 = np.linspace(base_start, base_start + (burst1_start_idx * (base_end - base_start) / total_points), burst1_start_idx, endpoint=False)
base_after_burst1 = np.linspace(base_start + (burst1_end_idx * (base_end - base_start) / total_points), base_start + (burst2_start_idx * (base_end - base_start) / total_points), burst2_start_idx - burst1_end_idx, endpoint=False)
base_after_burst2 = np.linspace(base_start + (burst2_end_idx * (base_end - base_start) / total_points), base_end, total_points - burst2_end_idx, endpoint=True)

# Randomly remove points from base arrays
np.random.seed(0)  # For reproducibility
remove_fraction = 0.3  # Fraction of points to remove
remove_indices_before_burst1 = np.random.choice(base_before_burst1.size, int(base_before_burst1.size * remove_fraction), replace=False)
remove_indices_after_burst1 = np.random.choice(base_after_burst1.size, int(base_after_burst1.size * remove_fraction), replace=False)
remove_indices_after_burst2 = np.random.choice(base_after_burst2.size, int(base_after_burst2.size * remove_fraction), replace=False)

base_before_burst1 = np.delete(base_before_burst1, remove_indices_before_burst1)
base_after_burst1 = np.delete(base_after_burst1, remove_indices_after_burst1)
base_after_burst2 = np.delete(base_after_burst2, remove_indices_after_burst2)

# Generate bursts
burst1 = np.linspace(base_before_burst1[-1], base_after_burst1[0], int((burst1_end_idx - burst1_start_idx) / burst_density))
burst2 = np.linspace(base_after_burst1[-1], base_after_burst2[0], int((burst2_end_idx - burst2_start_idx) / burst_density))

# Combine base and bursts
timestamps = np.concatenate((base_before_burst1, burst1, base_after_burst1, burst2, base_after_burst2))
relative_time = (timestamps - timestamps[0]) / 10
cumulative_time_candidates = np.arange(1, len(timestamps) + 1)

print(timestamps)

# Plot
fig = plt.figure(figsize=(20, 10), dpi=100)

# Plot blue horizontal line for the first burst
y_position_top = max(cumulative_time_candidates) + 5  # Y position for the top line
y_position_bottom = -5  # Y position for the bottom line

plt.plot([relative_time[len(base_before_burst1)], relative_time[len(base_before_burst1) + len(burst1) - 1]],
         [y_position_top, y_position_top], color='blue', linewidth=11)

# Plot blue horizontal line for the second burst
plt.plot([relative_time[len(base_before_burst1) + len(burst1) + len(base_after_burst1)],
          relative_time[len(base_before_burst1) + len(burst1) + len(base_after_burst1) + len(burst2) - 1]],
         [y_position_top, y_position_top], color='blue', linewidth=11, label='actual stall')

# Plotting cumulative time candidates with colored points
plt.scatter(relative_time, cumulative_time_candidates, color='black', label='candidate packet', marker='o', s=100)

# Plot red horizontal line for the bursts at bottom
plt.plot([relative_time[len(base_before_burst1)], relative_time[len(base_before_burst1) + len(burst1) - 20]],
         [y_position_bottom, y_position_bottom], color='red', linewidth=9)
plt.plot([relative_time[len(base_before_burst1) + len(burst1) + len(base_after_burst1)],
          relative_time[len(base_before_burst1) + len(burst1) + len(base_after_burst1) + len(burst2) - 10]],
         [y_position_bottom, y_position_bottom], color='red', linewidth=9, label='inferred stall')

# Customize plot
plt.xlabel('Time, s')
plt.yticks([])
plt.ylim(y_position_bottom - 30, y_position_top + 30)  # Adjust the padding as needed
plt.gcf().subplots_adjust(bottom=0.2)  # Add space below
plt.gcf().subplots_adjust(left=0.15)  # Add space on the left
plt.margins(0.02, 0.01)  # Reduce margins between plot and edges
plt.tick_params(axis='x', which='major', width=7, length=24)
plt.tick_params(axis='y', which='major', width=7, length=24, pad=20)
plt.legend(frameon=False, loc='upper left', fontsize=35, markerscale=2)

# Save the figure
plt.savefig('cumulative_stalldet_horizontal_toy_madeup.pdf', bbox_inches='tight')

# Show the plot
#plt.show()
