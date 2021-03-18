import redis
r = redis.Redis(host='localhost', port=6379, db=0)
req_itemid = input("请输入itemid:")
key = '_'.join(['CF', req_itemid])
if r.exists(key):
    s = str(r.get(key))
    print(s)
    print(len(s))
