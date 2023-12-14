import argparse
import logging

import redis
import requests
import hashlib
import json
import datetime
from sanic import Sanic, response

import os

from dotenv import dotenv_values
config = dotenv_values(".env")


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

REDIS_HOST = "prod-saarthi-redis.1vscjj.ng.0001.aps1.cache.amazonaws.com"
REDIS_PASSWORD = ""

from bot_responses import generate_response,generate_response_hindi,generate_response_tamil,generate_response_malayalam,generate_response_kannada,generate_response_telugu
import redis

REDIS_PORT = 6379
REDIS_DB = 11
REDIS_DB_CONV = "0"

# DB specific to MAIA
red_maia_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)

# logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 9256

DEFAULT_SANIC_WORKERS = 1

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 11
REDIS_PASSWORD = "sam@1234"
REDIS_DB_CONV = "0"
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Request logger
request_logger = setup_logger('request_logger', 'logs/request_logger.log')
# Bot Response logger
orchestrator_response_logger = setup_logger('orchestrator_response_logger', 'logs/orchestrator_response_logger.log')
# In-Time Logger
time_logger = setup_logger("intime_logger","logs/intime_logger.log")

def maintain_time_log(start_time,end_time,session_id):
    # try:
    delay=end_time-start_time
    with open("time_tracker.txt","a") as f:
        f.write("session_id %s"%session_id+"\t"+"Incoming Time %s"%start_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n")
    # except IOError:
    #     with open("time_tracker.txt","w+") as f:
    #         f.write("Incoming Time %s"%start_time+"\t"+"Response Time %s"%end_time+"\n")
    return
def in_time_log(start_time,session_id):
    print("******************")
    print("Session id:",session_id)
    print("Start time:",start_time)
    intime_value = "session_id %s"%session_id+"\t"+"Incoming Time %s"%start_time+"\n"
    time_logger.info(intime_value)
    # with open("in_time_tracker.txt","a") as f:
    #     f.write("session_id %s"%session_id+"\t"+"Incoming Time %s"%start_time+"\n")


def create_argument_parser():
    """Parse all the command line arguments for the nlg server script."""
    
    parser = argparse.ArgumentParser(description="starts the nlg endpoint")
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_SERVER_PORT,
        type=int,
        help="port to run the server at",
    )
    parser.add_argument(
        "--workers",
        default=DEFAULT_SANIC_WORKERS,
        type=int,
        help="Number of processes to spin up",
    )

    return parser

def detect_language(data):
    print("data",data)
    user_id=data['user_id']
    print("phone_number",user_id)
    with open("customer_details.json", "r+", encoding='utf-8') as f:
        customer_details = json.load(f)
    for customer in customer_details:
        if int(customer['phone_number'])==int(user_id):
            return customer["custom_field_2"]
    user_id="12345"
    for customer in customer_details:
        if int(customer['phone_number'])==user_id:
            return customer["custom_field_2"]
    return "en"

def detect_language_based_on_redis(data):
    print("data",data)
    user_id=data['user_id']
    print("phone_number",user_id)
    data=red_maia_customers.hgetall(user_id)
    print('data-->',data,flush=True)
    language = data["primaryInfo.language"].lower()
    return language


app = Sanic(__name__)
@app.route("/webhook", methods=["POST", "OPTIONS"])
async def nlg(request):
    """Endpoint which processes the Core request for a bot response."""
    nlg_call = request.json
    request_logger.info("Logging BOT REQUEST")
    request_logger.info(nlg_call)
    in_time=datetime.datetime.now()
    sender_id = nlg_call.get("sender")
    intime_value = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\n"
    time_logger.info(intime_value)
    bot_response = await generate_response(nlg_call)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%nlg_call["sender"]+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    time_logger.info(out_time)
    orchestrator_response_logger.info(bot_response)
    orchestrator_response_logger.info("*******")
    return response.json(bot_response)
    
if __name__ == "__main__":
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()
    app.run(host="0.0.0.0", port=cmdline_args.port, workers=cmdline_args.workers,access_log=True)
