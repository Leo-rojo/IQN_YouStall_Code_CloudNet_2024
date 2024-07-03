import matplotlib.pyplot as plt
import numpy as np

font_axes_titles = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 30,
                        }
font_title = {'family': 'sans-serif',
                        'color':  'black',
                        #'weight': 'bold',
                        'size': 30,
                        }
font_general = {'family' : 'sans-serif',
                        #'weight' : 'bold',
                        'size'   : 30}
plt.rc('font', **font_general)
path='/home/leonardo/Desktop/ISP_user_collaboration/Figure4/Results_endtoend/mzdfGCdNSHQ_1000Kbps/p_0.2 w_0.1/'
with open(path+'Detected_clicks.txt', 'r') as f:
    detected_clicks = f.readlines()
with open(path+'timestamp_of_candidate.txt', 'r') as f:
    time_candidate = f.readlines()
clicks_clean = [click.strip() for click in detected_clicks if click != '----------\n']
time_candidate_clean = [time.strip() for time in time_candidate]




import matplotlib.pyplot as plt
import numpy as np

# Assuming clicks_clean and time_candidate_clean are provided
# clicks_clean = [...]
# time_candidate_clean = [...]

# Convert timestamps from string to float
clicks_clean = list(map(float, clicks_clean))
time_candidate_clean = list(map(float, time_candidate_clean))

# Sort the timestamps
clicks_clean.sort()
time_candidate_clean.sort()

# Create cumulative occurrence arrays
cumulative_clicks = np.arange(1, len(clicks_clean) + 1)
cumulative_time_candidates = np.arange(1, len(time_candidate_clean) + 1)

# Plot the cumulative occurrences
fig = plt.figure(figsize=(20, 10),dpi=100)
# Plotting cumulative clicks
plt.plot([c-time_candidate_clean[0] for c in clicks_clean], cumulative_clicks, label='Clicks', marker='o')
# Plotting cumulative time candidates
plt.plot([t-time_candidate_clean[0] for t in time_candidate_clean], cumulative_time_candidates, label='Candidate packets', marker='o')
# Adding labels and title
plt.xlabel('Time in sec respect first candidate packet')
plt.ylabel('Cumulative Occurrence')
plt.legend()
plt.grid(True)

# Show plot
plt.show()
