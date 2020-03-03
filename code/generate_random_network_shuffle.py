#!/usr/bin/python3
# -*- coding:utf-8 -*-

import random
import numpy as np
from multiprocessing import Pool

with open("HMDD_Shuffle_input.txt", 'r') as fi:
	df = [row.strip().split("\t") for row in fi.readlines()]
	disease = sorted(list(set([row[0] for row in df])))
	weight = [float(row[-1]) for row in df]

def tonimoto(vi, vj):
    vi = [float(x) for x in vi]
    vj = [float(x) for x in vj]
    distance2_i = sum([x**2 for x in vi])
    distance2_j = sum([x**2 for x in vj])
    inner_product = sum([x*y for x, y in zip(vi, vj)])
    return inner_product/(distance2_i + distance2_j - inner_product)

def cutoff(weight):
	if float(weight) > 0:
		return "1"
	if float(weight) < 0:
		return "-1"


def output(filename):
	# 生成疾病向量字典
	random.shuffle(weight)
	rand_weight = np.array(weight).reshape(len(disease), -1).tolist()
	dvecs = {d: rand_weight[i] for i, d in enumerate(disease)}

	# 计算相似度
	dcnt = len(disease)
	allsim = [[str(i), str(j), tonimoto(dvecs[disease[i]], dvecs[disease[j]])] 
				for i in range(dcnt) for j in range(i)]

	# 取阈值并转换权重
	data = [row[:2]+[cutoff(row[2])] for row in allsim if abs(row[2]) > 0.05]

	with open(filename, 'w') as fo:
		fo.writelines(["\t".join(row)+"\n" for row in data])

	print("Finished")

	return 0

p = Pool(20)
for i in range(10000):

	netfile = "net/Random_Network_shuffle_%d.txt"%i
	p.apply_async(output, args=(netfile,))

p.close()
p.join()
