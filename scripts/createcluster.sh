#!/bin/bash

# Update package repositories and install required packages
sudo apt update
sudo apt install -y tmux neofetch default-jre unzip

# Download Spigot
wget https://download.getbukkit.org/spigot/spigot-1.20.6.jar

# Make server dirs
mkdir ~/server01
mkdir ~/server02
mkdir ~/server03
mkdir ~/server04

# Make the tmux sessions and
cd ~/server01

tmux new-session -d -s server01
tmux set mouse on
tmux split-window -h
tmux split-window -t 1 -v
tmux send-keys -t 0 'java -Xmx1G -Xms1G -jar ~/spigot-1.20.6.jar nogui && echo "eula=true" > eula.txt && clear && java -Xmx1024M -Xms1024M -jar ~/spigot-1.20.6.jar --port 25501 nogui' Enter
tmux send-keys -t 1 'clear && neofetch && ko-fi.com/playbox && echo -e "\nServer IP: " && curl ifconfig.me && echo -e "\nPort: 25501" && echo -e "\n"' Enter
tmux send-keys -t 2 'clear && htop' Enter

cd ~/server02

tmux new-session -d -s server02
tmux set mouse on
tmux split-window -h
tmux split-window -t 1 -v
tmux send-keys -t 0 'java -Xmx1G -Xms1G -jar ~/spigot-1.20.6.jar nogui && echo "eula=true" > eula.txt && clear && java -Xmx1024M -Xms1024M -jar ~/spigot-1.20.6.jar --port 25502 nogui' Enter
tmux send-keys -t 1 'clear && neofetch && echo "Consider donating to my Ko-fi: ko-fi.com/playbox" && echo -e "\nServer IP: " && curl ifconfig.me && echo -e "\nPort: 25502" && echo -e "\n"' Enter
tmux send-keys -t 2 'clear && htop' Enter

cd ~/server03

tmux new-session -d -s server03
tmux set mouse on
tmux split-window -h
tmux split-window -t 1 -v
tmux send-keys -t 0 'java -Xmx1G -Xms1G -jar ~/spigot-1.20.6.jar nogui && echo "eula=true" > eula.txt && clear && java -Xmx1024M -Xms1024M -jar ~/spigot-1.20.6.jar --port 25503 nogui' Enter
tmux send-keys -t 1 'clear && neofetch && echo -e "\nServer IP: " && curl ifconfig.me && echo -e "\nPort: 25503" && echo -e "\n"' Enter
tmux send-keys -t 2 'clear && htop' Enter

cd ~/server04

tmux new-session -d -s server04
tmux set mouse on
tmux split-window -h
tmux split-window -t 1 -v
tmux send-keys -t 0 'java -Xmx1G -Xms1G -jar ~/spigot-1.20.6.jar nogui && echo "eula=true" > eula.txt && clear && java -Xmx1024M -Xms1024M -jar ~/spigot-1.20.6.jar --port 25504 nogui' Enter
tmux send-keys -t 1 'clear && neofetch && echo -e "\nServer IP: " && curl ifconfig.me && echo -e "\nPort: 25504" && echo -e "\n"' Enter
tmux send-keys -t 2 'clear && htop' Enter

tmux attach-session -t server01