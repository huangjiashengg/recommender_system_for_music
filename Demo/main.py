import web
import redis
import math

urls = (
    '/', 'index',
    '/test', 'test',
)

app = web.application(urls, globals())

# 加载user特征
user_fea_dict = {}
with open('C:/Users/DELL/music-top-recommend/data/user_feature.data', 'r', encoding='UTF-8') as fd:
    for line in fd:
        userid, fea_list_str = line.strip().split('\t')
        user_fea_dict[userid] = fea_list_str


# 加载item特征
item_fea_dict = {}
with open('C:/Users/DELL/music-top-recommend/data/item_feature.data', 'r', encoding='UTF-8') as fd:
    for line in fd:
        ss = line.strip().split('\t')
        if len(ss) != 2:
            continue
        itemid, fea_list_str = ss
        item_fea_dict[itemid] = fea_list_str


class index:
    def GET(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        # step 1 : 解析请求，上面我们已经得到userid，itemid
        params = web.input()
        userid = params.get('userid', '')
        req_itemid = params.get('itemid', '')
        # userid = input("请输入userid:")
        # req_itemid = input("请输入Itemid:")

        # step 2 : 加载模型
        model_w_file_path = 'C:/Users/DELL/music-top-recommend/data/model.w'
        model_b_file_path = 'C:/Users/DELL/music-top-recommend/data/model.b'

        model_w_list = []
        model_b = 0.
        with open(model_w_file_path, 'r', encoding='UTF-8') as fd:
            for line in fd:
                ss = line.strip().split(',')
                if len(ss) != 2:
                    continue
                model_w_list.append(float(ss[1].strip()))

        with open(model_b_file_path, 'r', encoding='UTF-8') as fd:
            for line in fd:
                ss = line.strip().split(',')
                if len(ss) != 2:
                    continue
                model_b = float(ss[1].strip())

        # step 3 : 检索候选(match)，这里我们分两次，cb，cf
        #将检索回来的item全部放到recallitem列表里面
        rec_item_mergeall = []
        # 3.1 cf
        cf_recinfo = 'null'
        key = '_'.join(['CF', req_itemid])
        if r.exists(key):
            cf_recinfo = str(r.get(key))

        if len(cf_recinfo) > 6:
            for cf_iteminfo in cf_recinfo.strip().split('_'):
                item, score = cf_iteminfo.strip().split(':')
                rec_item_mergeall.append(item)

        # 3.2 cb
        cb_recinfo = 'null'
        key = '_'.join(['CB', req_itemid])
        if r.exists(key):
            cb_recinfo = str(r.get(key))
        if len(cb_recinfo) > 6:
            for cb_iteminfo in cb_recinfo.strip().split('_'):
                item, score = cb_iteminfo.strip().split(':')
                rec_item_mergeall.append(item)

        # step 4: 获取用户特征,将获取的用户特征处理后放到字典里面，方便后续计算内积
        user_fea = ''
        if userid in user_fea_dict:
            user_fea = user_fea_dict[userid]

        u_fea_dict = {}
        for fea_idx in user_fea.strip().split(' '):
            ss = fea_idx.strip().split(':')
            if len(ss) != 2:
                continue
            idx = int(ss[0].strip())
            score = float(ss[1].strip())
            u_fea_dict[idx] = score

        # step 5: 获取物品的特征 ,循环遍历刚刚得到itemid，判断item是否在item特征中，若在开始进行处理
        rec_list = []
        for itemid in rec_item_mergeall:
            if itemid in item_fea_dict:
                item_fea = item_fea_dict[itemid]

                i_fea_dict = dict()
                for fea_idx in item_fea.strip().split(' '):
                    ss = fea_idx.strip().split(':')
                    if len(ss) != 2:
                        continue
                    idx = int(ss[0].strip())
                    score = float(ss[1].strip())
                    i_fea_dict[idx] = score

                #得到召回item对应的特征和用户的特征，之后根据模型求出来的w，b，进行打分
                wx_score = 0.
                #这里我们求个内积，wx，然后做sigmoid，先将两个字典拼接起来，然后计算分数
                total_dict = {}
                for k, v in u_fea_dict.items():
                    total_dict[k] = v
                for k, v in i_fea_dict.items():
                    total_dict[k] = v
                for fea, score in total_dict.items():
                    wx_score += (score * model_w_list[fea])

                #**计算sigmoid: 1 / (1 + exp(-wx))**
                final_rec_score = 1 / (1 + math.exp(-(wx_score + model_b)))
                #将itemid和分数放入列表中，方便后续排序
                rec_list.append((itemid, final_rec_score))
        # print(rec_list)

        # step 6 : 精排序(rank)
        rec_sort_list = []
        rec_sort_list = sorted(rec_list, key=lambda x: x[1], reverse=True)
        # print(rec_sort_list)

        # step 7 : 过滤(filter)取top10
        rec_fitler_list = rec_sort_list[:10]
        # print(rec_fitler_list)

        # step 8 : 返回+包装(return)，进行将itemid转换成name

        item_dict = {}
        with open('C:/Users/DELL/music-top-recommend/data/name_id.dict', 'r', encoding='UTF-8') as fd:
            for line in fd:
                raw_itemid, name = line.strip().split('\t')
                item_dict[raw_itemid] = name
        # print(item_dict)
        # print(rec_fitler_list)

        ret_list = []
        for tup in rec_fitler_list:
            req_item_name = item_dict[req_itemid]
            item_name = item_dict[tup[0]]
            item_rank_score = str(tup[1])
            ret_list.append('   ->   '.join([req_item_name, item_name, item_rank_score]))
        # print(ret_list)
        ret = '\n'.join(ret_list)

        # print(ret)
        return ret

class test:
    def GET(self):
        print(web.input())
        return '222'

if __name__ == "__main__":
    app.run()
