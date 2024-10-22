# Description
**Experiments**:
- First, run *Selenium_chrome.py*. This script will automatically open a Chrome browser and start a YouTube video session as specified in the script. The script will not generate any results, it is used only to create a real setting.
- Manually set the YouTube video quality to 720p.
- Impose a bandwidth limit of 1 Mbps using the following command in a separate terminal:
  ```bash
  sudo /path/to/your/tcconfig/installation/tcset your_interface --rate 1000kbps --direction incoming
- Set parameters *i* and *k*, nr of sequential toggles and iteration number, in *End-user_agent.py* then run it using the command `python End-user_agent.py` in a new terminal. This will generate folders with the results of 
the experiments in the structure 'Results/CPUi_k.npy' and 'Results/Memoryi_k.npy', which contains the CPU percentage consumption and memory MB consumption collected every 5 seconds respect to the baseline. 
The baseline is the average CPU and memory consumption in the 5 seconds before the start of the End-user agent.

To remove the bandwidth limitation, run the following command:
  ```bash
  sudo /path/to/your/tcconfig/installation/tcdel your_interface --all
  ```

**Plotting**: 
- Run *Plots* to generate Figure 5 representing the End-user agent overhead in CPU and Memory terms.

**Results**: The folder should be organized as 'Results/CPUi_k.npy' and 'Results/Memoryi_k.npy' where i and k are the parameters of the experiment. The results are stored in the form of numpy arrays.