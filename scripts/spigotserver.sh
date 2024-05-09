#!/bin/bash

# Update package repositories and install required packages
sudo apt update
sudo apt install -y tmux neofetch default-jre unzip

# Download Spigot
wget https://download.getbukkit.org/spigot/spigot-1.20.6.jar

# Make server dir
mkdir ~/server01

# Make the tmux session
cd ~/server01

tmux new-session -d -s server01
tmux set mouse on
tmux split-window -h
tmux split-window -t 1 -v
tmux send-keys -t 0 'java -jar ~/spigot-1.20.6.jar nogui && echo "eula=true" > eula.txt && clear && java -jar ~/spigot-1.20.6.jar nogui' Enter
tmux send-keys -t 1 'clear && neofetch && echo "Consider donating to my Ko-fi: ko-fi.com/playbox" && echo -e "\nServer IP: " && curl ifconfig.me' Enter
tmux send-keys -t 2 'clear && htop' Enter

tmux attach-session -t server01