import redis
r = redis.Redis(host='localhost', port=6379, db=0)
with open('C:/Users/DELL/music-top-recommend/data/cf_reclist.redis', 'r', encoding='utf-8') as fd:
    for line in fd:
        set, key, value = line.strip().split(' ')
        r.set(key, value)
