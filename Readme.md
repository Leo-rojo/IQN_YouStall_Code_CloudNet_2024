# Folder Structure

To plot and replicate the results of the paper, the folder is organized with subfolders named after each figure intended to be replicated. Each subfolder contains the following structure:

- <h3>FigureX</h3>

  - **Experiments**: This contains the Python files needed to produce the results achieved by the paper. Detailed instructions on running the experiments are available in the Readme.md file.

  - **Plotting**: This contains the Python scripts used to plot the results of the experiments.

  - **Results**: This contains the results generated from running the experiments, which are then used by the scripts in the Plotting folder.

  - **Readme.md**: This file contains detailed instructions on how to run the experiments and plotting scripts, as well as how to structure the Results folder.

### General considerations
All experiments require running different scripts simultaneously, saving results in real-time. To achieve this, we recommend opening a new terminal for each script to 
maintain better control over the experiments. More details on how to run the experiments are provided in the Readme.md file of each figure. The ISP agent script has been run on 
a specific EC2 instance<sup>1</sup> where the local traffic is tunneled using OpenVPN<sup>2</sup>. However, with minor modifications, the script can be run locally to simulate the ISP.


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
In order to limit the bandwidth, we used `tcconfig`<sup>3</sup>, a is a tc command wrapper.

<sup>1</sup>https://aws.amazon.com/es/ec2/

<sup>2</sup>https://openvpn.net/

<sup>3</sup>https://tcconfig.readthedocs.io/en/latest/pages/introduction/index.html
