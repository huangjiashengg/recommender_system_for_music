import sys
import math

cur_token = None
item_score_list = []
item2item_score_list = []
itemA2B_dict = {}
cb_train = open('C:/Users/DELL/music-top-recommend/data/cb_train1.data', 'r', encoding='utf-8')
cb_result = open('C:/Users/DELL/music-top-recommend/data/cb_result', 'w', encoding='utf-8')
# sys.stdin = open('C:/Users/DELL/music-top-recommend/data/cb_train1.data', 'r')
for line in cb_train:
    ss = line.strip().split(',')
    itemid = ss[1]
    score = float(ss[2])
    if len(ss) != 3:
        continue
    if cur_token == None:
        cur_token = ss[0]

    if cur_token != ss[0]:
        for i in range(0, len(item_score_list) - 1):
            for j in range(i + 1, len(item_score_list)):
                item_a, score_a = item_score_list[i]
                item_b, score_b = item_score_list[j]
                # score = float(score_a * score_b)/float(math.sqrt(pow(score_a,2))*math.sqrt(pow(score_b,2)))
                # 输出两遍的目的是为了形成II矩阵的对称
                if score_a < 0.7:
                    continue
                if score_b < 0.7:
                    continue
                score = float(score_a * score_b)
                if item_a == item_b:
                    continue
                if score < 0.6:
                    continue
                # CB—item2Item最终生成数据量太大，所以增加了去除重复项的操作，待斟酌更改
                if item_a in itemA2B_dict and itemA2B_dict[item_a][0] == item_b:
                    itemA2B_dict[item_a][1] = (itemA2B_dict[item_a][1] + score) / 2
                    continue

                if item_b in itemA2B_dict and itemA2B_dict[item_b][0] == item_a:
                    itemA2B_dict[item_b][1] = (itemA2B_dict[item_b][1] + score) / 2
                    continue

                itemA2B_dict[item_a] = [item_b, float(score)]
                itemA2B_dict[item_b] = [item_a, float(score)]
                # print("%s\t%s\t%s" % (item_a, item_b, score))
                cb_result.write('\t'.join([item_a, itemA2B_dict[item_a][0], str(itemA2B_dict[item_a][1])]))
                cb_result.write('\n')
                # print("%s\t%s\t%s" % (item_b, item_a, score))
                cb_result.write('\t'.join([item_b, itemA2B_dict[item_b][0], str(itemA2B_dict[item_b][1])]))
                cb_result.write('\n')
        cur_token = ss[0]
        item_score_list = []
    item_score_list.append((itemid, float(score)))

for i in range(0, len(item_score_list) - 1):
    for j in range(i + 1, len(item_score_list)):
        item_a, score_a = item_score_list[i]
        item_b, score_b = item_score_list[j]
        # score = (score_a * score_b) / (math.sqrt(pow(score_a, 2)) * math.sqrt(pow(score_b, 2))
        # 输出两遍的目的是为了形成II矩阵的对称
        if score_a < 0.7:
            continue
        if score_b < 0.7:
            continue
        score = float(score_a * score_b)
        if item_a == item_b:
            continue
        if score < 0.6:
            continue

        # CB—item2Item最终生成数据量太大，所以增加了去除重复项的操作，待斟酌更改
        if item_a in itemA2B_dict and itemA2B_dict[item_a][0] == item_b:
            itemA2B_dict[item_a][1] = (itemA2B_dict[item_a][1] + score) / 2
            continue

        if item_b in itemA2B_dict and itemA2B_dict[item_b][0] == item_a:
            itemA2B_dict[item_b][1] = (itemA2B_dict[item_b][1] + score) / 2
            continue

        itemA2B_dict[item_a] = [item_b, float(score)]
        itemA2B_dict[item_b] = [item_a, float(score)]
        # print("%s\t%s\t%s" % (item_a, item_b, score))
        cb_result.write('\t'.join([item_a, itemA2B_dict[item_a][0], str(itemA2B_dict[item_a][1])]))
        cb_result.write('\n')
        # print("%s\t%s\t%s" % (item_b, item_a, score))
        cb_result.write('\t'.join([item_b, itemA2B_dict[item_b][0], str(itemA2B_dict[item_b][1])]))
        cb_result.write('\n')

cb_result.close()


