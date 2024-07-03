# Description
**Experiments**:
To run the experiments:
- First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script.
- Manually set the YouTube video quality to 720p.
- Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
  ```bash
  sudo /home/leonardo/Desktop/venv_310/bin/tcset wlo1 --rate 1000kbps --direction incoming
- Run *End-user_agent.py* with the value of p=0.2 using the command `python End-user agent.py 0.2` in a new terminal. This will generate folders with the results of the experiments in the structure Results_kind/Videoid_1000Kbps/p_0.2/Detected_clicks_0.2.txt, which contains the timestamps of when the autoplay button has been clicked four times.
- Finally, to complete the experiments, run Infer_other_p_values.py. This script will infer other p values from the detected clicks with p=0.2 and generate the results in folders with the structure Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt.
- Organize all the results in the Results folder with the following structure: Results/Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt for every kind and every p value.

**Plotting**: 
- Run *Plot_ground-truth_stall_duration.py* to generate the distributions of stall lengths for different genres.
- Run *Plot_precision_recall.py* to plot the bar chart for precision and recall at different p values, corresponding to Figure 3.
- Run *Plot_legend.py* to generate the relative legend.

**Results**: The folder should be organized as Results/Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt for every kind and every p value. The results contain the timestamps of when the autoplay button has been clicked four times for different p values and video genres.