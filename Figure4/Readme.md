# Description
**Experiments**:
- First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script. The script will generate a file with the ground truth stall lengths in the folder 'Results_kind/Videoid_1000Kbps/, with file 'Real_stalls.txt'.
- Manually set the YouTube video quality to 720p.
- Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
  ```bash
  sudo /path/to/your/tcconfig/installation/tcset wlo1 --rate 1000kbps --direction incoming
- Run *End-user_agent.py* using the command `python End-user agent.py` in a new terminal. This will generate folders with the results of the experiments in the structure Results_kind/Videoid_1000Kbps/Detected_clicks_0.2.txt, which contains the timestamps of when the autoplay button has been clicked four times. This can be useful for debugging purposes.
- Run *ISP_detector.py* in the EC2 instance in order to capture the quic candidate packets. This will generate folders with the results of the experiments in the folder 'Results_kind/Videoid_1000Kbps/', it will generate timestamp_of_candidate.txt, which contains the timestamps of when the candidate packets has been sniffed.

This procedure should be repeated for each type of video: *music*, *news*, and *sports*. To do this, you need to change the parameters (variables) 'kind' and 'Video_link' in the scripts.
Once the results for each type of video are obtained:
- Organize all the results in the Results folder with the following structure: Results/Results_kind/Videoid_1000Kbps/Name.txt for every gendre and txt file generated.

**Plotting**: 
- Run *Plot_operational_example.py* to generate the operational example, Figure 4a. The data for the generation of the operational example are contained in Results/Operational_example folder. 
- Run *Plot_inferredvsactual_durationerrorsignificant.py* to plot Figure 4b and 4c, print aggragated and specific statistics for every gendre and plot additional figures that show cumulative candidate
packets and the detection of stalls over time.

**Results**: The folder should be organized as Results/Results_kind/Videoid_1000Kbps/Name.txt for every kind and every txt file generated. The results should contain 'Real_stalls.txt' and 'timestamp_of_candidate.txt' which are used for the 
plots, plus the 'Detected_clicks_0.2.txt' which is useful for debugging purposes.