# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:52:17 2020

@author: Stoner
cst 较全， 而pst只包含出现次数不为零的词对 actually a complete may be unnecessary
However, doing so will 将概率限制在数据集中出现的词对，其它都是零
cst 及其求和中去掉了delta项， 因为它用处不大，且拖慢运行速度
"""

from collections import Counter
import json


# load corpus(split into lines) as list
workdir = 'C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse'
filename_cn = workdir + '\\cn.txt'
filename_en = workdir + '\\en.txt'
fpo_cn = open(filename_cn, encoding='utf-8-sig')
fpo_en = open(filename_en)

lines_cn = []
for line in fpo_cn:
    line = line.strip()
    # line = line.decode('utf-8')
    lines_cn.append(line.split(' '))
fpo_cn.close()

lines_en = []
for line in fpo_en:
    line = line.strip()
    line = line.lower()
    # line = line.decode('utf-8')
    lines_en.append(line.split(' '))
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
        num_cn.setdefault(cn_word, 0)
        num_cn[cn_word] += 1
        
for en_word in pst.keys():
    for cn_word in pst[en_word].keys():
        pst[en_word][cn_word] = 1/num_cn[cn_word]


for num_iteration in range(50):
    # calculate c(s|t; S, T)
    cst = {}
    total = {}
    for z in range(len(lines_cn)):
        sum_pst_t = {}
        for en_word in lines_en[z]:
            cst.setdefault(en_word, {})
            sum_pst_t.setdefault(en_word, 0)
            sum_pst_t[en_word] += sum(pst[en_word].values())
                
        # calculate sums of csts
        sum_cst_z_s = {}
        sum_cst_z = {}
        i = 0
        for en_word in lines_en[z]:
            sum_cst_z.setdefault(en_word, {})
            for cn_word in lines_cn[z]:
                cst[en_word].setdefault(cn_word, 0)
                cst[en_word][cn_word] += pst[en_word][cn_word] / sum_pst_t[en_word]
                total.setdefault(cn_word, 0)
                total[cn_word] += pst[en_word][cn_word]/sum_pst_t[en_word]
    print(num_iteration)
        
    
                   
    
    
    
    # calculate new pst
    for en_word in pst.keys():
        for cn_word in pst[en_word].keys():
            pst[en_word][cn_word] = cst[en_word][cn_word]/total[cn_word]


# save matrix
js = json.dumps(pst)
file = open('C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\pst1.txt', 'w')
file.write(js)
file.close()
