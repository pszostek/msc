#!/usr/bin/env python

from __future__ import division 
from __future__ import print_function
from segmedit.fasttrueviz import load
import sys
import os.path
import os
import re
import itertools
import Queue
import threading
from collections import Counter
from xml.sax import SAXParseException

write_q = Queue.Queue()
file_q = Queue.Queue() 

LABEL_COUNTER, ZONES_NR, PAGE_NR, LABEL_LENGTH = 1,2,3,4

class CheckThread(threading.Thread):
    def __init__(self, write_q, file_q):
        super(CheckThread, self).__init__()
        self.stoprequest = threading.Event()
        self.write_q = write_q
        self.file_q = file_q
    
    def run(self):
        while not self.stoprequest.isSet() and not file_q.empty():
            try:
                filename = self.file_q.get()
                labels_count = Counter()
                label_length = set()
                zones_count = 0
                print("check " + filename)
                doc = load(filename)
		    
                pages_count = len(doc)
                for page in doc:
                    zones_count += len(page)
                    for zone in page:
                        if zone.label and zone.label.name:
                            labels_count[zone.label.name] += 1
                            label_length.add((zone.label.name, len(zone)))
                        else:
                            labels_count["NONAME"] += 1
                self.file_q.task_done()
            except Queue.Empty:
                break
    	    except SAXParseException:
                print("SAXParseException")
            self.write_q.put((LABEL_COUNTER, labels_count))
            self.write_q.put((LABEL_LENGTH, label_length))
            self.write_q.put((ZONES_NR, zones_count))
            self.write_q.put((PAGE_NR, pages_count))

    def join(self):
        self.stoprequest.set()
        super(CheckThread, self).join()


if len(sys.argv) != 2:
    print("Usage: measure_grotoap2.py /path/to/xml/directory")
    exit(1)
    
dir_path = sys.argv[1]
all_files = []

for root, x, files in os.walk(dir_path):
    for filename in files:
        if filename.endswith('.cxml'):
            all_files.append(os.path.join(root, filename))
print("number of all files: %d" % len(all_files))

for file in all_files:
    file_q.put(file)

check_threads_pool = [CheckThread(write_q, file_q) for _ in xrange(0,8)] 
for thread in check_threads_pool:
    thread.start()
    
while not file_q.empty():
    continue

[thread.join() for thread in check_threads_pool]

print("Processing files done")

label_counts = list()
zones_count = Counter()
pages_count = Counter()
label_length = set()

while not write_q.empty():
    tag, element = write_q.get()
    if tag == LABEL_COUNTER:
        label_counts.append(element)
    elif tag == ZONES_NR:
        zones_count[element] += 1
    elif tag == PAGE_NR:
        pages_count[element] += 1
    elif tag == LABEL_LENGTH:
        label_length |= element


total_count = Counter()
for counter in label_counts:
    total_count += counter

documents_with_labels = Counter()
for counter in label_counts:
    documents_with_labels += Counter(counter.keys())

import pickle
dumpf = open('grotoap2_summary.pickle','w')
pickle.dump(label_counts, dumpf)
pickle.dump(zones_count, dumpf)
pickle.dump(pages_count, dumpf)
pickle.dump(label_length, dumpf)
dumpf.close()
