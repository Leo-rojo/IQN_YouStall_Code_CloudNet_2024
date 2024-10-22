## Generate Figure 02

### LA
* input files: the data for the generation of the operational example are contained in 'Operational_example' folder. The data regarding real stalls and clicks detected with the timestamp for every experiments 
are organized as '/Results_kind/Videoid_1000Kbps/Name.txt' for every kind and every txt file generated which contains:
  - 'Real_stalls.txt': This file logs the stalls experienced during an experiment. Each stall is documented on separate lines, with the start and end of the stall marked by "S" (start) or "E" (end), followed by the corresponding timestamp.
  - 'timestamp_of_candidate.txt': Contains the timestamps of when the ISP's detector identifies a potential IQN packet.
  - 'Detected_clicks_0.2.txt': Records timestamps when the end-user agent takes screenshots, along with an identifier for each stall event: "N" for no stall and "S" for a stall.
* Run generate_figure_2a.py to generate Figure 2a
* Run generate_figure_2b_2c.py to generate Figure 2b and 2c. This script will also print aggregated and specific statistics for each genre and plot additional figures, including cumulative candidate packets and stall detection over time.

### LB
* input files: None
* How to run new indipendent experiments using scripts in 'Scripts' folder:

  - First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script. The script will generate a file with the ground truth stall lengths in the folder 'Results_kind/Videoid_1000Kbps/, with file 'Real_stalls.txt'.
  - Manually set the YouTube video quality to 720p.
  - Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
    ```bash
    sudo /path/to/your/tcconfig/installation/tcset your_interface --rate 1000kbps --direction incoming
  - Run *End-user_agent.py* using the command `python End-user_agent.py` in a new terminal. This will generate folders with the results of the experiments in the structure Results_kind/Videoid_1000Kbps/Detected_clicks_0.2.txt, which contains the timestamps of when the autoplay button has been clicked four times. This can be useful for debugging purposes.
  - Run *ISP_detector.py* in the EC2 instance in order to capture the quic candidate packets. This will generate folders with the results of the experiments in the folder 'Results_kind/Videoid_1000Kbps/', it will generate timestamp_of_candidate.txt, which contains the timestamps of when the candidate packets has been sniffed. 
  The script can be run locally in a new terminal to emulate an ISP. Be sure to change the network interface accordingly.

  This procedure should be repeated for each type of video: *music*, *news*, and *sports*. To do this, you need to change the parameters (variables) 'kind' and 'Video_link' in the scripts.
  Once the results for each type of video are obtained:
  - Organize all the results in the Results folder with the following structure: 'input_files/Results_kind/Videoid_1000Kbps/Name.txt' for every gendre and txt file generated.
  
  To remove the bandwidth limitation, run the following command:
    ```bash
    sudo /path/to/your/tcconfig/installation/tcdel your_interface --all
    ```
  - All the results folder should be placed into output_data folder
  - Run generate_figure_2a.py to generate Figure 2a 
  - Run generate_figure_2b_2c.py to generate Figure 2b and 2c and to 