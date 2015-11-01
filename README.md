# Easy CLI for the Silicon Dust HDHomeRun

These python programs automate a few tedious tasks with the HDHomeRun:
* Parsing the output from a scan
* Selecting which channel to view
* Setting frequency and program based on that selection
* Setting the target of the UDP stream
* Opening VLC to recieve the stream when it starts
* Resetting the tuner after you are finished watching the stream (press enter or close VLC)

# Getting Started
1. Download and compile the hdhomerun_config software from http://www.silicondust.com/support/downloads/linux/
2. Scan using the hdhomerun_config command, and output the results to a text file
3. Run parse.py like ./parse.py \<scan.txt\> \<scan.json\>
4. Modify config.json to match your environment
5. Run ./stream.py
 
# Notes
* Only tested on Cygwin on Windows
* Remove the VLC pair from the JSON to prevent VLC from opening
* You may need to manually add firewall rules to allow VLC to reciev the stream
