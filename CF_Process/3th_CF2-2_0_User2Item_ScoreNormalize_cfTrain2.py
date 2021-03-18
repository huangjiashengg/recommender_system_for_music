'''
    在map的基础上将每个item进行归一化，map已经将相同的item排好序，根据map的结果进行给先平方再开根号：
    思路 ：
        1、截取字符串，取出item，user，socre
        2、在for循环中进行判断，当前的item和下一个是否相同，要是相同，将相同的放到列表（user，score）列表里面，否则往下执行
        3、若不相同，循环user和score列表，进行模计算，然后再次循环，进行单位化计算
'''
# 主要目的是进行score单位化计算，最后输出形式是user_item_score
import math
cur_item = None
user_score_list = []
input_file = 'C:/Users/DELL/music-top-recommend/data/cf_train1.data'
output_file = open('C:/Users/DELL/music-top-recommend/data/cf_train2.data', 'w', encoding='UTF-8')
with open(input_file, 'r', encoding='UTF-8') as fd:
    for line in fd:
        ss = line.strip().split(',')
        if len(ss) != 3:
            continue
        item, userid, score = ss

        if cur_item == None:
            cur_item = item
        if cur_item != item:
            # 定义sum
            sum = 0.0
            # 循环列表进行模向量计算
            for ss in user_score_list:
                user, s = ss
                sum += pow(s, 2)
            sum = math.sqrt(sum)
            # 单位化计算
            for touple in user_score_list:
                u, s = touple
                # 进行单位化完成后，我们输出重置成原来的user-item-score输出
                output_file.write('\t'.join((u, cur_item, str(float(s / sum)))))
                output_file.write('\n')
                # print("%s\t%s\t%s" % (u, cur_item, float(s / sum)))
            # 初始化这两个变量
            cur_item = item
            user_score_list = []
        user_score_list.append((userid, float(score)))

    # 定义sum
    sum = 0.0
    # 循环列表进行模向量计算
    for ss in user_score_list:
        user, s = ss
        sum += pow(s, 2)
    sum = math.sqrt(sum)
    # 单位化计算
    for touple in user_score_list:
        u, s = touple
        # 进行单位化完成后，我们输出重置成原来的user-item-score输出
        output_file.write('\t'.join((u, cur_item, str(float(s / sum)))))
        output_file.write('\n')
        # print("%s\t%s\t%s" % (u, cur_item, float(s / sum)))
    output_file.close()