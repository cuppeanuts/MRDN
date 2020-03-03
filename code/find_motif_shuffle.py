#!/usr/bin/python3
# -*- coding:utf-8 -*-

import subprocess
from multiprocessing import Pool

def findMotif(filename):
    subprocess.check_call(["mfinder", "input/"+filename, "-q", "-r", "0", "-f", 
                           "motif/"+filename.replace(".txt", ""), 
                           "-nd", "-omem", "-ospmem", "238", "-maxmem", "50000"])
    return 0

p = Pool(20)
for i in range(10000):
	filename = "mfinder_input_shuffle_%d.txt"%i
	p.apply_async(findMotif, args=(filename,))

p.close()
p.join()
