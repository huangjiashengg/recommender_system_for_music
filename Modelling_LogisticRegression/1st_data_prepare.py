import jieba.analyse
import jieba.posseg

merge_base_infile = 'C:/Users/DELL/music-top-recommend/data/merge_base.data'
output_file = 'C:/Users/DELL/music-top-recommend/data/samples.data'

# 我们这里需要再生成两个文件，一个是用户样本和item样本，因为要对实时推荐的化，必须使用这两个样本
output_user_feature_file = 'C:/Users/DELL/music-top-recommend/data/user_feature.data'
output_item_feature_file = 'C:/Users/DELL/music-top-recommend/data/item_feature.data'
# 这里生成个类似name和id对应的字典信息
output_itemid_to_name_file = 'C:/Users/DELL/music-top-recommend/data/name_id.dict'


# 定义函数，来获取各类数据
def get_base_samples(infile):
    #放待处理样本数据
    ret_samples_list = []
    #放user用户数据
    user_info_set = set()
    #放物品数据
    item_info_set = set()
    item_name2id = {}
    item_id2name = {}

    with open(infile, 'r', encoding='UTF-8') as fd:
        for line in fd:
            ss = line.strip().split('\001')
            if len(ss) != 13:
                continue
            userid = ss[0].strip()
            itemid = ss[1].strip()
            # 这两个时间为了计算label而使用
            watch_time = ss[2].strip()
            total_time = ss[10].strip()

            # 用户数据
            gender = ss[4].strip()
            age = ss[5].strip()
            user_feature = '\001'.join([userid, gender, age])

            # 物品数据
            name = ss[8].strip()
            item_feature = '\001'.join([itemid, name])

            # 计算标签
            label = float(watch_time) / float(total_time)
            final_label = '0'

            if label >= 0.82:
                final_label = '1'
            elif label <= 0.3:
                final_label = '0'
            else:
                continue

            # 接下来装载数据，并返回结果，首先我们装在itemid2name和itemname2id
            item_name2id[name] = itemid
            item_id2name[itemid] = name

            # 装在待处理的标签数据
            ret_samples_list.append([final_label, user_feature, item_feature])

            user_info_set.add(user_feature)
            item_info_set.add(name)

    return ret_samples_list, user_info_set, item_info_set, item_name2id, item_id2name


# step 1 程序的入口，开始调用函数，开始处理文件，得到相应的数据
base_sample_list, user_info_set, item_info_set, item_name2id, item_id2name = get_base_samples(merge_base_infile)
# step 2 抽取用户画像信息，用户标签转换，将年龄和age进行转换，用于样本使用
user_fea_dict = {}
for info in user_info_set:
    userid, gender, age = info.strip().split('\001')
    # 设置标签idx，将男(1)和女(0)用数剧的形式表示，权重都设置为1
    idx = 0  # default 女
    if gender == '男':
        idx = 1
    # 将标签和权重拼接起来
    gender_fea = ':'.join([str(idx), '1'])
    # 性别设置完成，我们接下来设置年龄，将年龄进行划分，0-18，19-25，26-35，36-45
    idx = 0
    if age == '0-18':
        idx = 0
    elif age == '19-25':
        idx = 1
    elif age == '26-35':
        idx = 2
    elif age == '36-45':
        idx = 3
    else:
        idx = 4

    idx += 2

    age_fea = ':'.join([str(idx), '1'])

    user_fea_dict[userid] = ' '.join([gender_fea, age_fea])

# step 3 抽取物品特征，这里我们要用到分词，将name进行分词，并且把分词后的token转换成id，这里就需要我们来做生成tokenid词表
token_set = set()
item_fs_dict = {}
for name in item_info_set:
    token_score_list = []
    for x, w in jieba.analyse.extract_tags(name, withWeight=True):
        token_score_list.append((x, w))
        token_set.add(x)
    item_fs_dict[name] = token_score_list

# 进行token2id的转换
token_id_dict = {}
# 这里我们要用到刚刚利用set去重过的token列表，生成tokenid的字典表
i = 0
for s in enumerate(list(token_set)):
    token_id_dict[s[1]] = s[0]
    i = i + 1
print("总token数目为：", i)


# 接下来，我们需要把第三步生成的item_fs_dict中name对应的token全部替换成id，然后当作字典，为下面的全量替换做准备
item_fea_dict = {}
user_feature_offset = 10
for name, fea in item_fs_dict.items():
    token_score_list = []
    for (token, score) in fea:
        if token not in token_id_dict:
            continue
        token_id = token_id_dict[token] + user_feature_offset
        token_score_list.append(':'.join([str(token_id), str(score)]))

    # 接下来输出到字典中
    item_fea_dict[name] = ' '.join(token_score_list)

# step 4 将第一步输出的样本数据整体替换并且替换user_feature和item_feature,并输出到文件中
ofile = open(output_file, 'w', encoding='UTF-8')
for (label, userfea, itemfea) in base_sample_list:
    userid = userfea.strip().split('\001')[0]
    item_name = itemfea.strip().split('\001')[1]

    if userid not in user_fea_dict:
        continue
    if item_name not in item_fea_dict:
        continue

    ofile.write('\001'.join([label, user_fea_dict[userid], item_fea_dict[item_name]]))
    ofile.write('\n')

ofile.close()

# step 5 为了能够实时使用userfeatre，我们需要输出一下
out_put_file = open(output_user_feature_file, 'w', encoding='UTF-8')
for userid, fea in user_fea_dict.items():
    out_put_file.write('\t'.join([userid, fea]))
    out_put_file.write('\n')
out_put_file.close()

# step 6 输出item_feature
out_file = open(output_item_feature_file, 'w', encoding='UTF-8')
for name, fea in item_fea_dict.items():
    if name not in item_name2id:
        continue
    itemid = item_name2id[name]
    out_file.write('\t'.join([itemid, fea]))
    out_file.write('\n')

# step 7 输出id2name的对应的字典
o_file = open(output_itemid_to_name_file, 'w', encoding='UTF-8')
for id, name in item_id2name.items():
    o_file.write('\t'.join([id, name]))
    o_file.write('\n')
o_file.close()
