## Generate Figure 03

### LA
* input files: The data contains timestamps of when end-user agent takes screenshots and 
an identifier for stall: N not stall and S is a stall. Those data are grouped in different subfolders called
'p_value' depending on the value of parameter *p*. The valued spanned by our experiments are 0.2-0.4-0.8-1.6-2.0 for the three genres.
Additionally inside each folder there is file 'Real_stalls.txt' containing the length of the stalls codified as S-timestamp E-timestamp for 
the starting and ending timestamp, respectively.
* Run generate_figure_3.py to generate Figure 3
* Run generate_legend.py to generate legend of Figure 3
* Run Plot_ground-truth_stall_duration.py to generate ground truth stalls ecdf for the three genders.

### LB
* input files: None
* How to run new indipendent experiments using scripts in 'Scripts' folder:

    - First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script. The script will 
    automatically save the ground truth information about stall length in Results_kind/Videoid_1000Kbps/p_0.2/Real_stalls.txt. 
    Additionally, it will reset any bandwidth limitations previously imposed using the tcconfig command.
    - Manually set the YouTube video quality to 720p.
    - Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
      ```bash
      sudo /path/to/your/tcconfig/installation/tcset your_interface --rate 1000kbps --direction incoming
    - Run *End-user_agent.py* with the value of *p=0.2* using the command `python End-user_agent.py 0.2` in a new terminal. This will generate folders with the results of the experiments in the structure Results_kind/Videoid_1000Kbps/p_0.2/Detected_clicks_0.2.txt, which contains the timestamps of when the autoplay button has been clicked four times.
    - Put 'Results_kind' folder with results inside 'output_data' folder

  This procedure should be repeated for each type of video: *music*, *news*, and *sports*. To do this, you need to change the parameters (variables) 'kind' and 'Video_link' in the scripts. 
  Once the results for each type of video with a p value of 0.2 are obtained:

  - Run *Infer_other_p_values.py*. This script will infer other *p* values from the detected clicks with p=0.2 and generate the results in folders with the structure Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt.
    - Put and organize all the results in the 'output_data' folder with the following structure: output_data/Results_kind/Videoid_1000Kbps/p_interval/Detected_clicks_interval.txt for every kind and every p value.

  To remove the bandwidth limitation, run the following command:
    ```bash
    sudo /path/to/your/tcconfig/installation/tcdel your_interface --all
    ```
  - Run generate_figure_3.py to generate Figure 3
  - Run generate_legend.py to generate legend of Figure 3
  - Run Plot_ground-truth_stall_duration.py to generate ground truth stalls ecdf for the three genders.

