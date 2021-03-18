
# 按照Item进行排序
import math
cur_item = None
item_user_score_list = []
input_file = 'C:/Users/DELL/music-top-recommend/data/cf_train.data'
output_file = open('C:/Users/DELL/music-top-recommend/data/cf_train1.data', 'w', encoding='UTF-8')
with open(input_file, 'r', encoding='UTF-8') as fd:
    for line in fd:
        ss = line.strip().split(',')
        if len(ss) != 3:
            continue
        userid, itemid, score = ss
        # 注意新的列表元素位置换了下顺序
        item_user_score_list.append((itemid, userid, score))
    new_item_user_score_list = sorted(item_user_score_list, key=lambda x: x[0], reverse=True)
    for y in new_item_user_score_list:
        output_file.write(','.join(y))
        output_file.write('\n')
    # 测试文件最终得到：item_to_user_score数目为： 247999
    output_file.close()



