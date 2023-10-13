# This repo is a continuation of The Forabot research previously done by the contributors at https://github.com/ARoS-NCSU/ForaBot
## Overview:
We are currently in the progress of switching the Raspberry Pi we used for a Jetson Orin Nano. We are also converting the original Python process of this robot into ROS2 Foxy code. Later on this research will be passed along for the purpose of implementing a ML Classification node that will classify the species of forams for accurate sorting. The hardware must also be converted into mostly 3d printed parts due to supply chain issues for ease of open source repeatability. 

Prereqs: Download tic gui software at https://www.pololu.com/docs/0J71/3.2 and download maestro controller at https://www.pololu.com/docs/0J40/3.b 

To use this repo, you must clone it and then at the top level of the directory run 
$ bash ./setup.sh 
all packages must be built with
~/ForabotResearch/ros2_foxy_workspace$ colcon build -packages--select <package names>
~/ForabotResearch/ros2_foxy_workspace$ source ./install/setup.bash



## Related publications
Richmond, T. et al. (2022) “Forabot: Automated planktic foraminifera isolation and imaging,” Geochemistry, Geophysics, Geosystems [Preprint]. Available at: https://doi.org/10.1029/2022gc010689. 
