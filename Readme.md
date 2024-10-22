# IQN and YouStall: Code and Experimental Configurations
The repository collects and openly releases the dataset and accompanying code for the results published in the following article: 
    
    Leonardo Peroni, Sergey Gorinsky, and Farzad Tashtarian. 2024. In-Band Quality Notification from Users to ISPs.

To reproduce the results, please follow the instructions provided in the readme.md files located inside the subfolders.

### Structure
We support the reproducibility on two levels characterized by different resource requirements and time commitments. Level A (LA) recreates all figures, mostly by running
our Python code. The reproduction performs limited calculations based on data in final representations, such as the length of stalls experienced during a live streaming session. Level B (LB) carries out in-depth replication 
through new indipendent experiments that generates new data. While LA is
primarily for validating the results of this paper, LB targets the long-term impact of the artifacts
through their reuse in future research.

### Artifact checklist
- Programs: (LA) Python 3.10 with supporting libraries; (LB) Pillow, pyautogui, threading, pyshark, selenium, psutil
- Hardware: no particular requirements.
- Output: (LA) all figures of the paper; (LB) new data obtained from independent experiments.
- Approximate disk space requirement: (LA) 5.8 MB; (LB) depends on the length of experiments and value of parameter p.
- Approximate experiment completion time: (LA) minutes; (LB) depends on the length of experiments.
- Availability: public on GitHub.

### Artifact access
We structure the GitHub repository in folders dedicated to a figure. Each folder contains LA and/or LB
subfolders corresponding to the two levels of result reproducibility. The subfolders hold all the data
and code required for generating the respective results.
### Hardware dependencies
There are no specific hardware requirements except for support of
Python. The machine used in our experiments is an Intel i7 with six cores, 2.6-GHz CPUs, 16-GB
RAM, and Ubuntu 22.04.5 LTS.
### Software dependencies 
The requirements.txt file in the repository lists the software dependencies, with readme.md files in individual subfolders supplying any further details and clarifications.
### Datasets
Experiment-specific data in each subfolder.

### Installation
The LA reproducibility involves installation of Python 3.10 with libraries as described in the
requirements.txt file. For the in-depth LB replication, the additional installations include the Chrome browser<sup>1</sup> and various 
Python libraries such as Pillow<sup>2</sup> for the end-user agent, pyautogui<sup>3</sup> for interacting with YouTube's interface, 
pyshark<sup>4</sup> for packet detection and analysis from the ISP perspective, selenium<sup>5</sup> for automating browser activities, 
and psutil<sup>6</sup> for monitoring performance overhead.

### Evaluation and expected results
The repository allocates a separate self-contained folder for reproducing the results of each figure on the LA and/or LB levels, with readme.md files providing
specific instructions.

The LA reproducibility of the results consists in running the provided Python code on the associated dataset.

For completeness of the LA reproducibility, the GitHub repository includes the .pptx source of
our diagrams in Fig. 1.

Comprehensive replication of our results on the LB level involves additional existing and newly
developed software.

All experiments require running different scripts simultaneously, saving results in real-time. To achieve this, we recommend opening a new terminal for each script to 
maintain better control over the experiments. More details on how to run the experiments are provided in the Readme.md file of each figure. The ISP agent script has been run on 
a specific EC2 instance<sup>7</sup> where the local traffic is tunneled using OpenVPN<sup>8</sup>. However, with minor modifications, the script can be run locally to simulate the ISP.

The standalone *get_mouse_position.py* script is useful for obtaining the mouse position on the screen; it prints the current position of the mouse every second.

### Requirements

We tested the code with `Python 3.10` with the following additional requirements that can be found in the `requirements.txt` file:

```
matplotlib==3.8.2
numpy==1.25.2
Pillow==10.4.0
psutil==5.9.5
PyAutoGUI==0.9.54
pyshark==0.6
selenium==4.22.0
```
In order to limit the bandwidth, we used `tcconfig`<sup>9</sup>, which is a tc command wrapper.

<sup>1</sup>https://www.google.com/chrome/

<sup>2</sup>https://pypi.org/project/pillow/

<sup>3</sup>https://pyautogui.readthedocs.io/en/latest/

<sup>4</sup>https://pypi.org/project/pyshark/

<sup>5</sup>https://pypi.org/project/selenium/

<sup>6</sup>https://pypi.org/project/psutil/

<sup>7</sup>https://aws.amazon.com/es/ec2/

<sup>8</sup>https://openvpn.net/

<sup>9</sup>https://tcconfig.readthedocs.io/en/latest/pages/introduction/index.html
