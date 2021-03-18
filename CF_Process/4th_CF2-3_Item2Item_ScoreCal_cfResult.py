cur_user = None
item_score_list = []
itemA2B_dict = {}
input_file = 'C:/Users/DELL/music-top-recommend/data/cf_train3.data'
output_file = open('C:/Users/DELL/music-top-recommend/data/cf_result.data', 'w', encoding='UTF-8')

with open(input_file, 'r', encoding='UTF-8') as fd:
    for line in fd:
        user, item, score = line.strip().split(',')
        if cur_user == None:
            cur_user = user

        if cur_user != user:

            # 进行两两pair，利用range函数
            for i in range(0, len(item_score_list) - 1):
                for j in range(i + 1, len(item_score_list)):
                    item_a, score_a = item_score_list[i]
                    item_b, score_b = item_score_list[j]
                    score = score_a * score_b

                    if item_a in itemA2B_dict and itemA2B_dict[item_a][0] == item_b:
                        itemA2B_dict[item_a][1] = itemA2B_dict[item_a][1] + float(score)
                        continue

                    if item_b in itemA2B_dict and itemA2B_dict[item_b][0] == item_a:
                        itemA2B_dict[item_b][1] = itemA2B_dict[item_b][1] + float(score)
                        continue

                    itemA2B_dict[item_a] = [item_b, float(score)]
                    itemA2B_dict[item_b] = [item_a, float(score)]
                    # 输出两遍的目的是为了形成II矩阵的对称
                    # print("%s\t%s\t%s" % (item_a, item_b, score_a * score_b))
                    output_file.write('\t'.join([item_a, itemA2B_dict[item_a][0], str(itemA2B_dict[item_a][1])]))
                    output_file.write('\n')
                    # print("%s\t%s\t%s" % (item_b, item_a, score_a * score_b))
                    output_file.write('\t'.join([item_b, itemA2B_dict[item_b][0], str(itemA2B_dict[item_b][1])]))
                    output_file.write('\n')

            cur_user = user
            item_score_list = []
        item_score_list.append((item, float(score)))

    for i in range(0, len(item_score_list) - 1):
        for j in range(i + 1, len(item_score_list)):
            item_a, score_a = item_score_list[i]
            item_b, score_b = item_score_list[j]

            if item_a in itemA2B_dict and itemA2B_dict[item_a][0] == item_b:
                itemA2B_dict[item_a][1] = itemA2B_dict[item_a][1] + float(score)
                continue

            if item_b in itemA2B_dict and itemA2B_dict[item_b][0] == item_a:
                itemA2B_dict[item_b][1] = itemA2B_dict[item_b][1] + float(score)
                continue

            itemA2B_dict[item_a] = [item_b, float(score)]
            itemA2B_dict[item_b] = [item_a, float(score)]
            # 输出两遍的目的是为了形成II矩阵的对称
            # print("%s\t%s\t%s" % (item_a, item_b, score_a * score_b))
            output_file.write('\t'.join([item_a, itemA2B_dict[item_a][0], str(itemA2B_dict[item_a][1])]))
            output_file.write('\n')
            # print("%s\t%s\t%s" % (item_b, item_a, score_a * score_b))
            output_file.write('\t'.join([item_b, itemA2B_dict[item_b][0], str(itemA2B_dict[item_b][1])]))
            output_file.write('\n')
    output_file.close()

