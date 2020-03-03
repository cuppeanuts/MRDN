#!/usr/bin/python3
# -*- coding:utf-8 -*-

def rdfile(filename):
	with open(filename, 'r') as fi:
		df = [row.strip().split("\t") for row in fi.readlines()]
	return df

def wtfile(filename, data):
	output = [[str(val) for val in row] for row in data]
	with open(filename, 'w') as fo:
		fo.writelines(["\t".join(row)+"\n" for row in output])
	return 0


method = "shuffle"

for i in range(10000):
	df = rdfile("net/Random_Network_%s_%d.txt"%(method, i))
	res = [[int(row[0])+1, int(row[1])+1, row[2]] for row in df]
	mfin = [row[:2]+[1] for row in res]
	wtfile("Random_Network_%s_%d.txt"%(method, i), res)
	wtfile("mfinder_input_%s_%d.txt"%(method, i), mfin)
	if (i+1)%1000 == 0:
		print i
