import redis

import os

from dotenv import dotenv_values
config = dotenv_values(".env")

if len(config) > 0:
    REDIS_HOST = config["REDIS_HOST"]
    REDIS_PASSWORD = config["REDIS_PASSWORD"]
else:
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = "prod-saarthi-redis.1vscjj.ng.0001.aps1.cache.amazonaws.com"
REDIS_PASSWORD = ""

REDIS_PORT = 6379
REDIS_DB = 11

REDIS_DB_CONV = "0"
# DB specific to MAIA
red_maia_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)

def store_into_redis(customer_data):
    print("data",customer_data)
    for row in customer_data:
        red_maia_customers.hmset(row['contactInfo.primary'],row)
        print("duydigsi",type(row))
    return True

def fetch_data(phone_number):
    data=red_maia_customers.hgetall(phone_number)
    print(data)
    return data




