## Generate Figure 04

### LA
* input files: The data are numpy arrays containing end-user agent overhead for CPU consumption and memory.
The arrays are identified by their name of the kind: kind_of_overhead*n*_*r* with *n* and *r* two parameters that identify
nr of sequential toggles of the autoplay switch of the interface and the iteration number of the experiment. e.g CPU2_3 means that
the array contains the third experiment that consider two toggles in a row.
* Run generate_figure_4.py to generate Figure 4

### LB
* input files: None
* How to run new indipendent experiments using scripts in 'Scripts' folder:

  - First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script. The script will not generate any results, it is used only to create a real setting.
  - Manually set the YouTube video quality to 720p.
  - Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
    ```bash
    sudo /path/to/your/tcconfig/installation/tcset your_interface --rate 1000kbps --direction incoming
  - Set parameters *n* and *r*, nr of sequential toggles and iteration number, in *End-user_agent.py* then run it using the command `python End-user_agent.py` in a new terminal. This will generate folders with the results of 
  the experiments in the structure 'output_data/CPUi_k.npy' and 'output_data/Memoryi_k.npy', which contains the CPU percentage consumption and memory MB consumption collected every 5 seconds respect to the baseline. 
  The baseline is the average CPU and memory consumption in the 5 seconds before the start of the End-user agent.

  To remove the bandwidth limitation, run the following command:
    ```bash
    sudo /path/to/your/tcconfig/installation/tcdel your_interface --all
    ```

  - Run generate_figure_4.py to generate Figure 4