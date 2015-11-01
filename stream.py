#!/usr/bin/python
import json
import signal
import os
import sys
import platform
import subprocess


def pingVerify(conf):
	if "NT" in platform.system():
		pingCom = "ping -n 1 "
	else:
		pingCom = "ping -c 1 "
	#ping tuner
	res = os.system(pingCom + conf["tuner_ip"] + " > /dev/null")
	if res == 1:
		print "Can't reach tuner"
		sys.exit(-1)

	#ping self
	res = os.system(pingCom + conf["my_ip"] + " > /dev/null")
	if res == 1:
		print "Can't reach myself"
		sys.exit(-2)


def exit_handler(signal, frame):
	pass

###### Execution Begins Here ######
signal.signal(signal.SIGINT, exit_handler)

#load config
with open("config.json") as f:
	conf = json.load(f)

pingVerify(conf)
tunStr = "/tuner" + conf["tuner"] + "/"
comBase = conf["command"] + " " + conf["tuner_ip"]
getBase = comBase + " get " + tunStr
setBase = comBase + " set " + tunStr

#ensure tuner valid
com = getBase + "channel"
output = os.popen(com).read()

if "ERROR" in output:
	print "Error communicating with tuner"
	sys.exit(-3)

#load channels
with open(conf["channels"]) as f:
	channels = json.load(f)


if conf["gui"] in ['true', 'True']:
	title = "Channel Chooser"
	msg = "Select the channel to stream:"
	choices = []
	for i in range(0, len(channels)):
		chan = channels[i]
		choices.append("{} {}".format(chan["numb"], chan["name"]))

	#TODO: message box

else:
	print "*** Enter the Channel to Stream ***"

	for i in range(0, len(channels) - 1, 2):
		chan = channels[i]
		chanStr =  "{}) {} {}".format(i, chan["numb"], chan["name"])
		chanStr = chanStr.ljust(25)
		print chanStr,
		j = i + 1
		chan = channels[j]
		print "{}) {} {}".format(j, chan["numb"], chan["name"])


	print "*** Enter the Channel to Stream ***"
	choice = input("> ")

chan = channels[choice]

com = setBase + "channel " + chan["freq"]
output = os.popen(com).read()

com = setBase + "program " + chan["prog"]
output = os.popen(com).read()

com = setBase + "target " + conf["my_ip"] + ":" + conf["my_port"]
output = os.popen(com).read()

print "{} is now streaming to port {} on {}".format(conf["tuner_ip"], conf["my_port"], conf["my_ip"])

if conf["vlc"]:
	path = os.path.normcase(conf["vlc"])
	com = [path, "--play-and-exit", "--deinterlace=1", "udp://@:" + conf["my_port"], "vlc://quit"]
	with open(os.devnull, "w") as fnull:
		p = subprocess.Popen(com, stdout=fnull, stderr=fnull)
	print "Close VLC to end the stream"
	p.communicate()

else:
	raw_input("Press Enter to end the stream...")

com = setBase + "target none"
output = os.popen(com).read()

com = setBase + "program none"
output = os.popen(com).read()

com = setBase + "channel none"
output = os.popen(com).read()
