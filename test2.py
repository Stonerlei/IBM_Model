# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 19:40:17 2020

@author: Stoner
"""
import json
import linecache
import numpy as np


file = open('C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\pst2.txt', 'r')
js = file.read()
pst2 = json.loads(js)
file.close()

file = 'C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\a.npy'
c = np.load(file, allow_pickle=True)

punctions = [',', '.', '"', '\'', ';', '[', ']',':','!','?', \
                '，','。','：','‘','’','“','”','、','！','？','【','】']

file_cn = 'C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\cn.txt'
file_en = 'C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\en.txt'
line_ids = [84123, 48585, 48621, 78456, 86258, 96325, 18269, 47536, 31246, 42691]
result = []
test_en = []
test_cn = []
for test_id in range(len(line_ids)): 
    test_en.append(linecache.getline(file_en, line_ids[test_id]).lower())
    test_cn.append(linecache.getline(file_cn, line_ids[test_id]).lower())
    test_cn[test_id] = test_cn[test_id].strip()
    test_en[test_id] = test_en[test_id].strip()
    for punction in punctions:
            while punction in test_en[test_id]:
                test_en[test_id] = test_en[test_id].replace(punction, '')
                # print(punction)
    test_en[test_id] = test_en[test_id].strip('\n')
    test_cn[test_id] = test_cn[test_id].strip('\n')
    test_cn[test_id] = test_cn[test_id].split(' ')
    test_en[test_id] = test_en[test_id].split(' ')
    for punction in punctions:
            while punction in test_cn[test_id]:
                test_cn[test_id].remove(punction)
    
    
    # test
    # test_en = ['i', 'eat', 'rose', 'residence']
    # test_cn = ['我', '生病', '玫瑰', '吃', '房子']
    result.append([])
    result.append(test_en[test_id])
    best_match = []
    for i in range(len(test_en[test_id])):
        max_num = 0
        for j in range(len(test_cn[test_id])):
            if test_cn[test_id][j] in pst2[test_en[test_id][i]].keys():
                if test_cn[test_id][j] not in result[test_id]:
                    if max(pst2[test_en[test_id][i]][test_cn[test_id][j]] \
                           * (c[len(test_en[test_id])-1][len(test_cn[test_id])-1][i][j])**0.1, max_num) > max_num:
                        max_num = max(pst2[test_en[test_id][i]][test_cn[test_id][j]] \
                                      * (c[len(test_en[test_id])-1][len(test_cn[test_id])-1][i][j])**0.1, max_num)
                        best_match.append(test_cn[test_id][j])
                else:
                    if 0.0001*pst2[test_en[test_id][i]][test_cn[test_id][j]] \
                            * (c[len(test_en[test_id])-1][len(test_cn[test_id])-1][i][j])**0.1> max_num:
                        max_num = 0.0001*pst2[test_en[test_id][i]][test_cn[test_id][j]] \
                                      * (c[len(test_en[test_id])-1][len(test_cn[test_id])-1][i][j])**0.1
                        best_match.append(test_cn[test_id][j])
                      
        if max_num < 0.00001:
            result[2*test_id].append('')
            continue
        result[2*test_id].append(best_match[-1])
