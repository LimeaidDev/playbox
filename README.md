# Playbox
<a href='https://ko-fi.com/X8X3XQ995' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi4.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a><br>
Playbox is a easy to use Minecraft server creation and management tool that uses <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html">AWS EC2</a> instances to create servers
Servers must be <a src='https://aws.amazon.com/ec2/graviton/'>ARM Instances
If you have any questions or concerns, <a href='https://discord.gg/MZWav7eVQb'>join my Discord server</a>, Or dm me @limeadetv

Server Instance must be ARM based. <a href="https://aws.amazon.com/ec2/graviton/">Compatable Instance Types</a>
## Quick Start
1. Clone the Repository
```
git clone https://github.com/LimeaidDev/playbox.git
```
2. Paste your AWS keys in `values.py`
```py
aws_access_key_id = 'Insert Access Key ID Here'
aws_secret_access_key = 'Insert Access Key Here'
region_name = 'us-east-2'
```
3. Run `playbox.bat` and create your first server
```
$ create MyFirstServer t4g.medium vanilla
```
After a while your server should be up and running. In the upper right window, you should see your IP address.
```
Server IP:
xxx.xxx.xxx.xxx
```
## Commands
* `create <Box Name> <Instance Type> <Server Type>` Creates a new server
* `ip <Box Name>` Shows the ip of the server
* `list` Shows all active servers
* `session <Box Name>` Connects you to the <a href="https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/">tmux</a> session
* `upload <Box Name> path/to/file` Uploads a file to the server
* `kill <Box Name>` Terminates the associated EC2 instance and deletes all box data
