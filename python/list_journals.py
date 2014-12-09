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


PUBLISHER = 1
PUB_YEAR = 2
JOURNAL = 3



class CheckThread(threading.Thread):
    def __init__(self, data_q, file_q):
        super(CheckThread, self).__init__()
        self.stoprequest = threading.Event()
        self.data_q = data_q
        self.file_q = file_q
    
    def run(self):
        while not self.stoprequest.isSet() and not file_q.empty():
            filename = self.file_q.get()
            doc = libxml2.parseFile(filename)
            print("parsing %s" % filename)
            context = doc.xpathNewContext()
            context.xpathRegisterNs('nxml', 'http://dtd.nlm.nih.gov/2.0/xsd/archivearticle')
            for tag, path in [(PUBLISHER,'//nxml:journal-meta/nxml:publisher/nxml:publisher-name'),
                              (PUB_YEAR, '//nxml:pub-date/nxml:year'),
                              (JOURNAL, '//nxml:journal-title')]:
                res = context.xpathEval(path)
                content = res[0].getContent()
                data_q.put((tag, content))
            doc.freeDoc()
            context.xpathFreeContext()
            file_q.task_done()


    def join(self):
        self.stoprequest.set()
        super(CheckThread, self).join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: list_content.py /path/to/xml/directory")
        exit(1)
        
    dir_path = sys.argv[1]

    all_files = []

    for root, _, files in os.walk(dir_path):
        for filename in files:
            if filename.endswith(".nxml"):
                all_files.append(os.path.join(root, filename))
    print("number of all NXML files: %d" % len(all_files))

    file_q = Queue.Queue() 
    data_q = Queue.Queue()

    for file in all_files:
        file_q.put(file)

    check_threads_pool = [CheckThread(data_q, file_q) for _ in xrange(0,10)] 
    for thread in check_threads_pool:
        thread.start()
        
    while not file_q.empty():
        pass 

    [thread.join() for thread in check_threads_pool]

    content_list = []
    while not data_q.empty():
        content = data_q.get()
        content_list.append(content)

    import pickle
    pickle.dump(content_list, open('arts_summary.pickle','w'))