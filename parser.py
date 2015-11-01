#!/bin/python

import sys
import re
import json

channels = []

f = open(sys.argv[1])

for line in f:
	res = re.search("SCANNING: ([^ ]*)", line)
	if res:
		freq = res.group(1)

	res = re.search("PROGRAM ([^:]*): ([^ ]*) (.*)", line)

	if res:
		prog = res.group(1)
		numb = res.group(2)
		name = res.group(3)

		if "encrypted" in name:
			continue

		if "no data" in name:
			continue

		#print freq + " " + prog + " " + numb + " " + name

		data = {}

		data["freq"] = freq
		data["prog"] = prog
		data["numb"] = numb
		data["name"] = name

		channels.append(data)

f.close()

channels.sort(key=lambda x: float(x["numb"]))

f = open(sys.argv[2], "w")
json.dump(channels, f)
f.close()
