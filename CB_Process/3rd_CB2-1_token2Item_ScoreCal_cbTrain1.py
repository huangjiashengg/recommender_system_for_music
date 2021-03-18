# out_CB_2to1data_file = open('C:/Users/DELL/music-top-recommend/data/cb_train1.data', 'w', encoding='utf-8')
import pandas as pd
import numpy as np
cb_train_list = []
score_list = []
with open('C:/Users/DELL/music-top-recommend/data/cb_train.data', 'r', encoding='utf-8') as f:
    for line in f:
        ss = line.strip().split(',')
        token, itemid, score = ss
        score = float(score)
        # cb_train_list.append((token, itemid, score))
        score_list.append(score)
    # new_cb_train_list = sorted(cb_train_list, key=lambda x: x[0])
s = pd.Series(score_list)
print(s.min())
print(s.quantile(0.25))
print("二分之一分位数：", s.quantile(0.5))
print("均值：", s.mean())
print(s.quantile(0.75))
print(s.max())
"""for k in new_cb_train_list:
    out_CB_2to1data_file.write(','.join(k))
    out_CB_2to1data_file.write('\n')
out_CB_2to1data_file.close()"""

