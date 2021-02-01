# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 19:05:09 2020

@author: Stoner
"""

import json
import linecache

file = open('C:\\Users\\Stoner\\Desktop\\NLP-PPT\\Machine-Translation-reverse\\pst1.txt', 'r')
js = file.read()
pst1 = json.loads(js)
file.close()


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
            if test_cn[test_id][j] in pst1[test_en[test_id][i]].keys() and test_cn[test_id][j] not in best_match:
            # if test_cn[test_id][j] in pst1[test_en[test_id][i]].keys():
                if max(pst1[test_en[test_id][i]][test_cn[test_id][j]], max_num) > max_num:
                    max_num = max(pst1[test_en[test_id][i]][test_cn[test_id][j]], max_num)
                    best_match.append(test_cn[test_id][j])
        if i < len(best_match):
            result[2*test_id].append(best_match[i])
