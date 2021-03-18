"""import pandas as pd
with open('C:/Users/DELL/music-top-recommend/data/cf_train.data', 'r', encoding='UTF-8') as fd:
    i = 0
    li = []
    for line in fd:
        for l in line.strip().split(','):
            li.append(l)
        if len(li) == 100:
            print(pd.DataFrame(li))
        i = i + 1
    print("user_to_item_score数目为：", i)"""
#########################################################################################################
"""
with open('C:/Users/DELL/music-top-recommend/data/cf_train3.data', 'r', encoding='UTF-8') as fd:
    for line in fd:
        print(line)
"""
with open("C:/Users/DELL/music-top-recommend/data/cf_reclist.redis", 'r', encoding='utf-8') as fd:
    i = 0
    for line in fd:
        i = i + 1
    print(i)