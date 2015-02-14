#!/usr/bin/env python
import sys

lines = open(sys.argv[1],'r').readlines()
for line in lines:
	if line.startswith('kernel'):
		print(line.split(':')[0])
	elif '[local]' in line:
		local_idx = line.index('[local]')
		line = line[local_idx+len('[local]'):]
		line = line[:line.index(')')+1]
		parts = line.split()
		print("%s %s %s" % (parts[0], parts[1], parts[2]))
