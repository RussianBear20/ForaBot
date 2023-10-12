
#!/bin/bash

# Update package list and upgrade packages
echo "Updating package list..."
sudo apt update

echo "Upgrading packages..."
sudo apt upgrade -y

# Uninstall Python 2 (with caution)
echo "Uninstalling Python 2..."
sudo apt remove -y python

# Verify Python 3 and install pip3
echo "Verifying Python 3..."
python3 --version

echo "Installing pip for Python 3..."
sudo apt install -y python3-pip

# Make Python 3 the default
echo "Making Python 3 the default..."
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Here we begin the install for ROS2 Foxy (as specified by https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html)

locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update

sudo apt upgrade

sudo apt install ros-foxy-desktop python3-argcomplete

sudo apt install ros-dev-tools

# Replace ".bash" with your shell if you're not using bash
# Possible values are: setup.bash, setup.sh, setup.zsh
source /opt/ros/foxy/setup.sh

# Create a ROS2 workspace
echo "Creating ROS2 workspace..."

mkdir -p ~/ForaBotResearch/ros2_foxy_workspace/src
cd ~/ForaBotResearch/ros2_foxy_workspace
colcon build

# Source the workspace
source ~/ForaBotResearch/ros2_foxy_workspace/install/setup.bash

echo "ROS2 workspace created and sourced."

echo "Setup complete."


