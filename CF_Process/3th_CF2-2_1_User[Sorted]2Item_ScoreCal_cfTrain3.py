
# 主要目的是按照User字段进行排序，方便下一步的两两配对
user_item_score_list = []
input_file = 'C:/Users/DELL/music-top-recommend/data/cf_train2.data'
output_file = open('C:/Users/DELL/music-top-recommend/data/cf_train3.data', 'w', encoding='UTF-8')
with open(input_file, 'r', encoding='UTF-8') as fd:
    for line in fd:
        ss = line.strip().split('\t')
        if len(ss) != 3:
            continue
        userid, itemid, score = ss
        # 注意新的列表元素位置换了下顺序
        user_item_score_list.append((userid, itemid, score))
    new_user_item_score_list = sorted(user_item_score_list, key=lambda x: x[0], reverse=True)
    for y in new_user_item_score_list:
        output_file.write(','.join(y))
        output_file.write('\n')
    # 测试文件最终得到：item_to_user_score数目为： 247999
    output_file.close()