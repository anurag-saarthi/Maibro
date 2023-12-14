import redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB_ENGLISH = 1
REDIS_DB_HINDI = 2
REDIS_DB_TELUGU = 3
REDIS_DB_KANNADA = 4
REDIS_DB_TAMIL = 5
REDIS_DB_BENGALI = 6
REDIS_DB_MALAYALAM = 7
REDIS_DB_PUNJABI = 8
REDIS_DB_MARATHI = 9
REDIS_DB_GUJARATI = 10

REDIS_PASSWORD = "sam@1234"
REDIS_DB_CONV = "0"
red_hindi = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_HINDI, password=REDIS_PASSWORD)
sender_id = "12344"
code=red_hindi.set(str(sender_id),"changed")
code=str(red_hindi.get(str(sender_id)),'utf-8')
print(code)