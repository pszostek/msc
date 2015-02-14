#!/usr/bin/env python

import sys
import os
import shutil

coverage_report_path = sys.argv[1]
cutoff_threshold = sys.argv[2]
output_dir = sys.argv[3]

for line in [line.strip() for line in open(coverage_report_path).readlines()]:
	parts = line.split()
	try:
		coverage = int(parts[0])
		coverage_path = parts[1].strip()
	except:
		continue
	if coverage < cutoff_threshold:
		continue
	basedir = os.path.basedir(coverage_path)
	print("Moving %s to %s (coverage %d\%)" % (basedir, output_dir, coverage))
	shutil.move(basedir, output_dir)





