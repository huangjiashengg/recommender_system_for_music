input_file = "C:/Users/DELL/music-top-recommend/data/merge_base.data"
# 输出cf训练数据
output_file = "C:/Users/DELL/music-top-recommend/data/cf_train.data"
ofile = open(output_file, 'w', encoding='UTF-8')

key_dict = {}
with open(input_file, 'r', encoding='UTF-8') as fd:
    for line in fd:
        ss = line.strip().split('\001')
        # 用户行为
        userid = ss[0].strip()
        itemid = ss[1].strip()
        watch_len = ss[2].strip()
        hour = ss[3].strip()
        # 用户画像
        gender = ss[4].strip()
        age = ss[5].strip()
        salary = ss[6].strip()
        user_location = ss[7].strip()
        # 物品元数据
        name = ss[8].strip()
        desc = ss[9].strip()
        total_timelen = ss[10].strip()
        item_location = ss[11].strip()
        tags = ss[12].strip()
        #拼接key，为了将同一个用户对相同物品的时长全部得到，需要做个聚合
        key = '_'.join([userid, itemid])
        if key not in key_dict:
            key_dict[key] = []
        key_dict[key].append((int(watch_len), int(total_timelen)))

#循环处理相同用户对相同item的分数
for k, v in key_dict.items():
    t_finished = 0
    t_all = 0
    # 以<userid, itemid>为key进行分数聚合
    for vv in v:
        t_finished += vv[0]
        t_all += vv[1]

    # 得到userid对item的最终分数
    score = float(t_finished) / float(t_all)
    userid, itemid = k.strip().split('_')


    ofile.write(','.join([userid, itemid, str(score)]))
    ofile.write("\n")
# 测试文件最终得到：user_to_item_score数目为： 247999
ofile.close()
