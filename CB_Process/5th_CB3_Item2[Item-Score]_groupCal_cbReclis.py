outfile = 'C:/Users/DELL/music-top-recommend/data/cb_reclist.redis'
ofile = open(outfile, 'w')

MAX_RECLIST_SIZE = 100
PREFIX = 'CB_'


item1_set = set()
with open("C:/Users/DELL/music-top-recommend/data/cb_result", 'r') as fd:
    for line in fd:
        itemid_A, itemid_B, sim_score = line.strip().split('\t')
        if itemid_A not in item1_set:
            item1_set.add(itemid_A)

try:
    rec_dict = {}
    item2_set = set()
    while len(item2_set) != len(item1_set):
        with open("C:/Users/DELL/music-top-recommend/data/cb_result", 'r') as fd:
            for line in fd:
                itemid_A, itemid_B, sim_score = line.strip().split('\t')

                if len(rec_dict) > 20000:
                    if itemid_A not in rec_dict:
                        continue
                    rec_dict[itemid_A].append((itemid_B, sim_score))
                else:
                    # 判断itemA在不在该字典里面，若不在，创建一个key为itemA的列表，把与itemA相关联的itemB和score添加进去
                    if itemid_A not in rec_dict and itemid_A not in item2_set:
                        rec_dict[itemid_A] = []
                        item2_set.add(itemid_A)
                        rec_dict[itemid_A].append((itemid_B, sim_score))
                    if itemid_A in rec_dict and itemid_A not in item2_set:
                        rec_dict[itemid_A].append((itemid_B, sim_score))
                    if itemid_A not in rec_dict and itemid_A in item2_set:
                        continue
        # 循环遍历字典，格式化数据，把itemB和score中间以：分割，不同的itemB以_分割
        for k, v in rec_dict.items():
            key_item = PREFIX + k

            # 接下来格式化数据，将数据以从大到小排列后再格式化
            # 排序,由于数据量大，我们只取100个
            # 排好序后，我们来格式化数据
            reclist_result = '_'.join([':'.join([tu[0], str(round(float(tu[1]), 6))]) for tu in
                                       sorted(v, key=lambda x: x[1], reverse=True)[:MAX_RECLIST_SIZE]])

            ofile.write(' '.join(['SET', key_item, reclist_result]))
            ofile.write("\n")
        rec_dict.clear()
except BaseException as e:
    print(e)
ofile.close()

