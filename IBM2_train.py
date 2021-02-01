# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:34:57 2020

@author: Stoner
"""

from collections import Counter
import numpy as np
from copy import deepcopy
import json
# import zhon.hanzi


# load corpus(split into lines) as list
workdir = 'C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse'
filename_cn = workdir + '\\cn.txt'
filename_en = workdir + '\\en.txt'
fpo_cn = open(filename_cn, encoding='utf-8-sig')
fpo_en = open(filename_en)

punctions = [',', '.', '"', '\'', ';', '[', ']',':','!','?', \
            '，','。','：','‘','’','“','”','、','！','？','【','】','']

lines_cn = []
for line in fpo_cn:
    line = line.strip()
    line = line.split(' ')
    for punction in punctions:
        while punction in line:
            line.remove(punction)         # line = line.decode('utf-8')
    lines_cn.append(line)
fpo_cn.close()

lines_en = []
for line in fpo_en:
    line = line.strip()
    line = line.lower()
    for punction in punctions:
        if punction in line:
            line = line.replace(punction,'')
    line = line.split(' ')
    for punction in punctions:
        while punction in line:
            line.remove(punction)
    # line = line.decode('utf-8')
    lines_en.append(line)
fpo_en.close()

# initialize p(s|t)
pst = {}
for i in range(len(lines_cn)):
    for en_word in lines_en[i]:
        # print(cn_word)
        pst.setdefault(en_word, {})
        for cn_word in lines_cn[i]:
            pst[en_word].setdefault(cn_word, 0)     
num_cn = {}
for en_word in pst.keys():
    for cn_word in pst[en_word].keys():
        # print(len(pst[cn_word]))
        # pst[en_word][cn_word] = 1.0/len(pst[cn_word])    # average initialization
        # print(pst[cn_word][en_word])
        num_cn.setdefault(cn_word, 0)
        num_cn[cn_word] += 1
for en_word in pst.keys():
    for cn_word in pst[en_word].keys():
        pst[en_word][cn_word] = 1/num_cn[cn_word]

# initialize a  defaultly think lenth of sentence is less than 50  l to cn, m to en
# m en words in a sentence
len_limit = 80
a = []
for m in range(len_limit):
    a.append([])
    for l in range(len_limit):
        a[m].append(np.ones((m+1,l+1))/(l+1))



for num_iteration in range(10):
    # initialize cs
    cst = {}
    cst_s = {}
    cij = []
    for m in range(len_limit):
        cij.append([])
        for l in range(len_limit):
            cij[m].append(np.ones((m+1,l+1)))
    cij_s = []
    for m in range(len_limit):
        cij_s.append([])
        for l in range(len_limit):
            cij_s[m].append(np.ones((1,l+1)))
    
    
    lens_en = []
    lens_cn = []
    for z in range(len(lines_en)):
        lens_cn.append(len(lines_cn[z]))
        lens_en.append(len(lines_en[z]))
        # calculate sum of pst along t
        sum_pst_t = {}
        for en_word in lines_en[z]:
            cst.setdefault(en_word, {})
            sum_pst_t.setdefault(en_word, 0)
            for cn_word in lines_cn[z]:
                sum_pst_t[en_word] += pst[en_word][cn_word]* \
                    a[lens_en[z]][lens_cn[z]] \
                        [lines_en[z].index(en_word)][lines_cn[z].index(cn_word)]
        
        # calculate sums of csts
        i = 0
        for en_word in lines_en[z]:
            for cn_word in lines_cn[z]:
                cst[en_word].setdefault(cn_word, 0)
                cst[en_word][cn_word] += pst[en_word][cn_word] * a[lens_en[z]][lens_cn[z]] \
                    [lines_en[z].index(en_word)][lines_cn[z].index(cn_word)] \
                          / sum_pst_t[en_word]
                cst_s.setdefault(cn_word, 0)
                cst_s[cn_word] += pst[en_word][cn_word] * a[lens_en[z]][lens_cn[z]] \
                    [lines_en[z].index(en_word)][lines_cn[z].index(cn_word)] \
                          / sum_pst_t[en_word]        #restore
                         
                         
        # calculate sums of cijs
        for j in range(lens_en[z]):
            for i in range(lens_cn[z]):
                cij[lens_en[z]-1][lens_cn[z]-1][j][i] += pst[lines_en[z][j]][lines_cn[z][i]]* \
                    a[lens_en[z]-1][lens_cn[z]-1][j][i] / sum_pst_t[lines_en[z][j]]
                cij_s[lens_en[z]-1][lens_cn[z]-1][0][i] += pst[lines_en[z][j]][lines_cn[z][i]]* \
                    a[lens_en[z]-1][lens_cn[z]-1][j][i] / sum_pst_t[lines_en[z][j]]
            # print('j: ',j,'\nlens_en[z]: ',lens_en[z])
        # print(z)
        
    
    # calculate new pst and a
    for en_word in pst.keys():
        for cn_word in pst[en_word].keys():
            pst[en_word][cn_word] = cst[en_word][cn_word]/cst_s[cn_word]
    for z in range(len(lines_en)):
        for j in range(lens_en[z]):
            for i in range(lens_cn[z]):
                a[lens_en[z]-1][lens_cn[z]-1][j][i] = cij[lens_en[z]-1][lens_cn[z]-1][j][i] / \
                    cij_s[lens_en[z]-1][lens_cn[z]-1][0][i]
    print(num_iteration)



    
    
# save matrix
js = json.dumps(pst)
file = open('C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\pst2.txt', 'w')
file.write(js)
file.close()

b = np.array(a)
filename = 'C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\a.npy'
np.save(filename, b)
