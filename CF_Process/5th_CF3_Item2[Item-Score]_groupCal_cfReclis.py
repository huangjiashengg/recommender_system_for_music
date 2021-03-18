
infile = 'C:/Users/DELL/music-top-recommend/data/cf_result.data'
outfile = 'C:/Users/DELL/music-top-recommend/data/cf_reclist.redis'

ofile = open(outfile, 'w')

MAX_RECLIST_SIZE = 100
PREFIX = 'CF_'

rec_dict = {}
with open(infile, 'r') as fd:
    for line in fd:
        itemid_A, itemid_B, score = line.strip().split('\t')
        #判断itemA在不在该字典里面，若不在，创建一个key为itemA的列表，把与itemA相关联的itemB和score添加进去
        if itemid_A not in rec_dict:
            rec_dict[itemid_A] = []
        rec_dict[itemid_A].append((itemid_B, score))

#循环遍历字典，格式化数据，把itemB和score中间以：分割，不同的itemB以_分割
for k, v in rec_dict.items():
    key = PREFIX+k
    # 接下来格式化数据，将数据以从大到小排列后再格式化
    # 排序,由于数据量大，我们只取100个
    list = sorted(v, key=lambda x: x[1], reverse=True)[:MAX_RECLIST_SIZE]
    # 拍好序后，我们来格式化数据
    result = '_'.join([':'.join([str(val[0]), str(round(float(val[1]), 6))]) for val in list])

    ofile.write(' '.join([key, result]))
    ofile.write("\n")

ofile.close()
