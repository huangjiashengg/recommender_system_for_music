import jieba
import jieba.posseg
import jieba.analyse

input_file = "C:/Users/DELL/music-top-recommend/data/merge_base.data"
output_file = "C:/Users/DELL/music-top-recommend/data/cb_train.data"
outfile = open(output_file, 'w', encoding='utf-8')
RATIO_FOR_NAME = 0.4
RATIO_FOR_DESC = 0.3
RATIO_FOR_TAGS = 0.3
# 读入tags权重值？
idf_file = "C:/Users/DELL/music-top-recommend/data/idf.txt"
idf_dict = {}
with open(idf_file, 'r', encoding='utf-8') as fd:
    for line in fd:
        token, idf_score = line.strip().split(' ')
        idf_dict[token] = idf_score

itemid_set = set()
with open(input_file, 'r', encoding='utf-8') as fd:
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

        # 对item去重，相同的itemid不用再计算，因为都一样，这里用到continue特性，当不同的时候才继续执行下面的代码
        if itemid not in itemid_set:
            itemid_set.add(itemid)
        else:
            continue

        # 去掉重复后的itemid，然后我们进行分词，计算权重，放到字典里面
        token_dict = {}
        #对name统计
        for a in jieba.analyse.extract_tags(name, withWeight=True):
            token = a[0]
            score = float(a[1])
            if token in token_dict:
                token_dict[token] += score * RATIO_FOR_NAME
            else:
                token_dict[token] = score * RATIO_FOR_NAME

        #对desc进行分词，这里需要注意的是描述一般会含有name中的词，这里我们把有的词的分数进行相加，没有的放入
        for a in jieba.analyse.extract_tags(desc, withWeight=True):
            token = a[0]
            score = float(a[1])
            if token in token_dict:
                token_dict[token] += score * RATIO_FOR_DESC
            else:
                token_dict[token] = score * RATIO_FOR_DESC

        # 对tags 进行分数计算
        for tag in tags.strip().split(','):
            if tag not in idf_dict:
                continue
            else:
                if tag in token_dict:
                    token_dict[tag] += float(idf_dict[tag]) * RATIO_FOR_TAGS
                else:
                    token_dict[tag] = float(idf_dict[tag]) * RATIO_FOR_TAGS

        #循环遍历token_dict，输出toke，itemid，score
        for k, v in token_dict.items():
            token = k.strip()
            score = str(v)
            outfile.write(','.join([token, itemid, score]))
            outfile.write("\n")

outfile.close()