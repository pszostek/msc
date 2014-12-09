#!/usr/bin/env python

from __future__ import division 
from __future__ import print_function
import sys
import os.path
import os
import re
import Queue
import threading
import libxml2
from multiprocessing import Pool
import pickle
import matplotlib.pyplot as plt
from collections import Counter
import unicodedata
import numpy as np
import matplotlib

PUBLISHER = 1
PUB_YEAR = 2
JOURNAL = 3

def shorten_name(name):
    parts = name.split(' ')
    ret = []
    for part in parts:
        if part[0].isalpha():
            ret.append(part[0])
    return ''.join(ret)

def histogram_from_counter2(counter, xlabel, ylabel, title):
    min_bin = min(counter.keys())
    max_bin = max(counter.keys())
    bins = max_bin - min_bin + 1
    data = []
    for label, count in counter.items():
        for _ in xrange(count):
            data.append(label)
    n, bins, patches = plt.hist(data, bins, facecolor='g', alpha=0.75, histtype='stepfilled')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

font = {'family' : 'verdana',
        #'weight' : 'bold',
        'size'   : 12}

matplotlib.rc('font', **font)

content = pickle.load(open('arts_summary.pickle','r'))

publishers = [item[1] for item in content if item[0] == PUBLISHER]
pub_years = [item[1] for item in content if item[0] == PUB_YEAR]
journals = [item[1] for item in content if item[0] == JOURNAL]

publishers_counter = Counter(publishers)
pub_years_counter = Counter(pub_years)
pub_years_counter = dict((int(key), value) for key, value in pub_years_counter.items())
journal_counter = Counter(journals)

publisher_labels = []
publisher_numbers = []
other = 0

for idx, tup in enumerate(publishers_counter.most_common()):
    publisher, count = tup
    if idx >= 15:
        other += count 
    else:
        #publisher_labels.append(unicodedata.normalize('NFKD', publisher).encode('ascii','ignore'))
        label = publisher.decode('utf-8')
        if len(label) > 30:
            label = shorten_name(label)
        publisher_labels.append(label)
        publisher_numbers.append(count)
publisher_labels.append("others")
publisher_numbers.append(other)

# publisher_anon_counter = Counter()
# for publisher, count in publishers_counter.items():
#     publisher_anon_counter[count] += 1

my_norm = matplotlib.colors.Normalize(0,5000)
cmap = plt.cm.gist_ncar
colors = cmap(np.linspace(0., 1., len(publisher_numbers)))
fig = plt.figure(figsize=(20,10))
print(publisher_numbers)
patches, texts, autotexts = plt.pie(publisher_numbers, labels=publisher_labels, startangle=90, shadow=True, colors=colors, autopct="%4.2f%%")
for t in texts:
    t.set_size("large")
plt.axis("equal")
fig.savefig('../plots/publishers_pieplot.pdf')


journal_labels = []
journal_numbers = []
other = 0

for idx, tup in enumerate(journal_counter.most_common()):
    journal, count = tup
    if idx >= 20:
        other += count 
    else:
        #journal_labels.append(unicodedata.normalize('NFKD', journal).encode('ascii','ignore'))
        journal_labels.append(journal.decode('utf-8'))
        journal_numbers.append(count)
journal_labels.append("others")
journal_numbers.append(other)

my_norm = matplotlib.colors.Normalize(0,5000)
cmap = plt.cm.gist_ncar
colors = cmap(np.linspace(0., 1., len(journal_numbers)))

fig = plt.figure(figsize=(20,10))
patches, texts, autotexts = plt.pie(journal_numbers, labels=journal_labels, startangle=90, shadow=True, colors=colors, autopct="%2.2f%%")
for t in texts:
    t.set_size("large")
plt.axis("equal")
fig.savefig('../plots/journals_pieplot.pdf')

fig = plt.figure(figsize=(8,8))
histogram_from_counter2(pub_years_counter, "publication year", "number of articles", "Histogram of GROTOAP2 articles publication years")
fig.savefig('../plots/publication_year_histogram.pdf')

plt.show()