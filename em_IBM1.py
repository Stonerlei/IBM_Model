# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 16:03:59 2020

@author: Stoner
"""

import copy


def em_for_IBM1(lines_cn, lines_en, pst):
    # # calculate c(s|t; S, T)
    # cst = []
    # for z in range(len(lines_cn)):
    #     cst.append(copy.deepcopy(pst))                 #深度复制
    #     for cn_word in pst.keys():
    #         # these if and else can be deleted, actually(possibly)
    #         if lines_cn[z].count(cn_word) == 0:
    #             for en_word in pst[cn_word].keys():
    #                 cst[z][cn_word][en_word] = 0
    #         else:
    #             for en_word in pst[cn_word].keys():
    #                 if lines_en[z].count(en_word) == 0:
    #                     cst[z][cn_word][en_word] = 0
    #                 else:
    #                     # cst[z][cn_word][en_word] = pst[cn_word][en_word]/
    #                     sum_pst_t = 0
    #                     for cn_word2 in pst.keys():         #加个if
    #                         if en_word in pst[cn_word2].keys(): 
    #                             sum_pst_t += pst[cn_word2][en_word]
    #                     cst[z][cn_word][en_word] = pst[cn_word][en_word] / sum_pst_t
    #                     cst[z][cn_word][en_word] *= lines_cn[z].count(cn_word) * \
    #                         lines_en[z].count(en_word)
        # print(z)
    
    
    # calculate c(s|t; S, T)
    cst = []
    for z in range(len(lines_cn)):
        cst.append({})
        for en_word in lines_en[z]:
            cst[z].setdefault(en_word, {})
            sum_pst_t = 0
            for cn_word in lines_cn[z]:
                sum_pst_t += sum(pst[en_word].values())
                cst[z][en_word][cn_word] = pst[en_word][cn_word] / sum_pst_t
                cst[z][en_word][cn_word] *= lines_cn[z].count(cn_word) * \
                    lines_en[z].count(en_word)
        print(z)
    
    
    
    
    
    
    # calculate sums of csts
    sum_cst_z_s = {}
    sum_cst_z = {}
    i = 0
    for en_word in pst.keys():
        sum_cst_z.setdefault(en_word, {})
        for cn_word in pst[en_word].keys():
            sum_cst_z[en_word].setdefault(cn_word, 0)
            for z in range(len(lines_cn)):
                if cn_word in lines_cn[z] and en_word in lines_en[z]:
                    sum_cst_z[en_word][cn_word] += cst[z][en_word][cn_word]
        i += 1
        print(i)
    for en_word in pst.keys():
        for cn_word in pst[en_word].keys():
            sum_cst_z_s.setdefault(cn_word, 0)
            sum_cst_z_s[cn_word] += sum_cst_z[en_word][cn_word]
    
    
    # calculate new pst
    for en_word in pst.keys():
        for cn_word in pst[en_word].keys():
            pst[en_word][cn_word] = sum_cst_z[en_word][cn_word]/sum_cst_z_s[cn_word]
    return pst
