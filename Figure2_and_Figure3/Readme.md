# Description
**Experiments**:
- First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script. The script will 
automatically save the ground truth information about stall length in files named Real_stalls.txt. 
Additionally, it will reset any bandwidth limitations previously imposed using the tcconfig command.
- Manually set the YouTube video quality to 720p.
- Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
  ```bash
  sudo /path/to/your/tcconfig/installation/tcset your_interface --rate 1000kbps --direction incoming
- Run *End-user_agent.py* with the value of *p=0.2* using the command `python End-user_agent.py 0.2` in a new terminal. This will generate folders with the results of the experiments in the structure Results_kind/Videoid_1000Kbps/p_0.2/Detected_clicks_0.2.txt, which contains the timestamps of when the autoplay button has been clicked four times.

This procedure should be repeated for each type of video: *music*, *news*, and *sports*. To do this, you need to change the parameters (variables) 'kind' and 'Video_link' in the scripts. 
Once the results for each type of video with a p value of 0.2 are obtained:

- Run *Infer_other_p_values.py*. This script will infer other *p* values from the detected clicks with p=0.2 and generate the results in folders with the structure Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt.
- Organize all the results in the 'Results' folder with the following structure: Results/Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt for every kind and every p value.

To remove the bandwidth limitation, run the following command:
  ```bash
  sudo /path/to/your/tcconfig/installation/tcdel your_interface --all
  ```

**Plotting**: 
- Run *Plot_ground-truth_stall_duration.py* to generate the distributions of stall lengths for different genres.
- Run *Plot_precision_recall.py* to plot the bar chart for precision and recall at different p values, corresponding to Figure 3.
- Run *Plot_legend.py* to generate the relative legend.

**Results**: The folder should be organized as Results/Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt for every kind and every p value. The results contain the timestamps of when the autoplay button has been clicked four times for different p values and video genres.