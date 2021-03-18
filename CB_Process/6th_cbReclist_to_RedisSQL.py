import redis
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline()
with open('C:/Users/DELL/music-top-recommend/data/cb_reclist.redis', 'r', encoding='utf-8') as fd:
    for line in fd:
        pre, key, value = line.strip().split(' ')
        pipe.set(key, value)
        pipe.execute()