#!/usr/bin/env python

from __future__ import division 
from __future__ import print_function
import sys
import os.path
import os
import re
import itertools
from collections import defaultdict
from Counter import Counter
import pickle

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib

LABEL_COUNTER, ZONES_NR, PAGE_NR, LABEL_LENGTH = 1,2,3,4

def barplot_from_counter(counter):
	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x()+rect.get_width()/2., 1.10*height, '%d'%int(height),
	                ha='center', va='bottom', rotation='90')
	pairs = sorted(counter.items(), key=lambda x:-x[1])
	values = [value for _, value in pairs]
	labels = [label for label,_ in pairs]
	ind = np.arange(len(values)+1)[1:]
	width = 0.35
	fig, ax = plt.subplots(figsize=(10,6))
	rects = ax.bar(ind, values, width,color='r')
	ax.set_ylabel("Label counts")
	ax.set_ylim([100,10000000])
	ax.set_title("Total number of zones with a given label in GROTOAP2")
	#ax.set_xticklabels( tuple(labels), rotation=45)
	plt.yscale('log', nonposy='clip')
	plt.subplots_adjust(bottom=0.3)
	xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in rects]
	plt.xticks(xticks_pos, tuple(labels), rotation=45, ha='right')
	#ax.set_xticks(ind+width)
	autolabel(rects)
	plt.grid(True)
	fig.savefig('../plots/label_barplot.pdf')

def barplot_from_counter2(counter):
	ALL_DOCS = 13210
	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%f'%float(height),
	                ha='center', va='bottom')
	pairs = sorted(counter.items(), key=lambda x:-x[1])
	values = [value/ALL_DOCS for _, value in pairs]
	labels = [label for label,_ in pairs]
	ind = np.arange(len(values)+1)[1:]
	width = 0.35
	fig, ax = plt.subplots(figsize=(10,6))
	rects = ax.bar(ind, values, width, color='r')
	ax.set_ylabel("Fraction of dataset")
	ax.set_title("Documents including a given label in GROTOAP2")
	plt.subplots_adjust(bottom=0.3)
	xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in rects]
	plt.xticks(xticks_pos, tuple(labels), rotation=45, ha='right')
	# ax.set_xticks(ind+width)
	# ax.set_xticklabels( tuple(labels), rotation=45)
	ax.grid(True)
	fig.savefig('../plots/docs_with_labels_barplot.pdf')

def histogram_from_counter(counter):
	min_bin = min(counter.keys())
	max_bin = max(counter.keys())
	bins = max_bin - min_bin + 1
	data = []
	for label, count in counter.items():
		for _ in xrange(count):
			data.append(label)
	fig = plt.figure(figsize=(8,8))
	n, bins, patches = plt.hist(data, bins/4, facecolor='g', alpha=0.75, histtype='stepfilled')
	plt.xlabel("number of zones")
	plt.ylabel("number of documents")
	plt.title("Histogram of number of zones in GROTOAP2 documents")
	plt.grid(True)
	fig.savefig('../plots/zones_histogram.pdf')

def histogram_from_counter2(counter, xlabel, ylabel, title, filename, color=None):
	if color is None:
		color = "green"
	min_bin = min(counter.keys())
	max_bin = max(counter.keys())
	bins = max_bin - min_bin + 1
	data = []
	for label, count in counter.items():
		for _ in xrange(count):
			data.append(label)
	fig = plt.figure(figsize=(8,8))
	n, bins, patches = plt.hist(data, bins, facecolor=color, alpha=0.75, histtype='stepfilled')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.grid(True)
	fig.savefig(filename)

font = {'family' : 'verdana',
        #'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)
#label_counts, zones_count, pages_count, label_length = 
data = pickle.load(open('../grotoap2_summary.pickle', 'r'))
global_label_counter = Counter()
global_zone_counter = Counter()
global_page_counter = Counter()
global_label_length_counter = defaultdict(Counter)
number_of_docs_with_label = Counter()

for document_counters in data:
	label_counts = document_counters[0][1]
	global_label_counter.update(label_counts)
	for label in label_counts.keys():
		number_of_docs_with_label[label] += 1	
	
	label_length = document_counters[1][1]
	for label, length in label_length:
		global_label_length_counter[label][length] += 1

	zones_count = document_counters[2][1]
	global_zone_counter[zones_count] += 1

	pages_count = document_counters[3][1]
	global_page_counter[pages_count] += 1

barplot_from_counter(global_label_counter)
barplot_from_counter2(number_of_docs_with_label)
histogram_from_counter(global_zone_counter)
histogram_from_counter2(global_page_counter, "number of pages", "number of documents", "Histogram of number of pages in documents of GROTOAP2", "../plots/pages_histogram.pdf")
print(global_label_length_counter.keys())
print(len(global_label_length_counter.keys()))
for label in global_label_length_counter.keys():
	histogram_from_counter2(global_label_length_counter[label], "number of zones labeled as %s" % label, "number of documents", "", "../plots/%s_histogram.pdf" % label, "orange")
#barplot_from_counter(global_zone_counter)
#plt.show()
# print(global_label_counter)
# print(global_zone_counter)
# print(global_page_counter)
# print(global_label_length_counter)

