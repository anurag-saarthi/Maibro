import argparse
import logging
import requests
import ast
import json
import os
import hashlib
import datetime
from pymongo import MongoClient
from dotenv import dotenv_values
from convert_num_to_text import convert_numbers
from sanic import Sanic, response

config = dotenv_values(".env")

if len(config) > 0:
    REDIS_HOST = config["REDIS_HOST"]
    REDIS_PASSWORD = config["REDIS_PASSWORD"]
    ATLAS_URI = config["ATLAS_URI"]
    DB_NAME = config["DB_NAME"]
    NAME_LEXICON_URL = config.get("NAME_LEXICON_URL")
else:
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
    ATLAS_URI = os.environ.get("ATLAS_URI")
    DB_NAME = os.environ.get("DB_NAME")
    NAME_LEXICON_URL = os.environ.get("NAME_LEXICON_URL")

REDIS_HOST = "prod-saarthi-redis.1vscjj.ng.0001.aps1.cache.amazonaws.com"
REDIS_PASSWORD = ""

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

nlg_logger = setup_logger('nlg_logger', 'logs/nlg_logger.log')

DEFAULT_SERVER_PORT = 15618

DEFAULT_SANIC_WORKERS = 1


async def hash_conversion(audio_id,sessionID):
    hash_object = hashlib.md5((audio_id+sessionID).encode('utf-8'))
    file_name = str(hash_object.hexdigest())
    return file_name


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


def connection():
    mongodb_client = MongoClient(ATLAS_URI)
    database = mongodb_client[DB_NAME]
    return database

db = connection()

async def get_response_from_db(template_name,language):
    value = list(db["botcollectionmaianews"].find({'templateId':template_name,"language":language}))
    return value


async def generate_response(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    args = nlg_call.get("arguments", {})
    print("Args", args)
    template = nlg_call.get("template")
    sessionID = nlg_call["tracker"]["sender_id"]
    bot_response = dict()
    audio_server = nlg_call["tracker"]["slots"]["audio_server"]
    language_value = nlg_call["tracker"]["slots"]["cust_lang"]
    account_name = nlg_call["tracker"]["slots"]["client_name_slot"].lower()
    data = {
        "en":"english",
        "tam":"tamil",
        "tel":"telugu",
        "ka":"kannada",
        "bn":"bengali",
        "ml":"malayalam",
        "hi":"hindi",
        "ma":"marathi",
        "pa":"punjabi",
        "gu":"gujarati",
        "od":"odia",
        "english":"english",
        "tamil":"tamil",
        "telugu":"telugu",
        "kannada":"kannada",
        "bangla":"bengali",
        "malayalam":"malayalam",
        "hindi":"hindi",
        "marathi":"marathi",
        "punjabi":"punjabi",
        "gujarati":"gujarati",
        "odia":"odia",
    }
    language_value = data[language_value]
    response_data = await get_response_from_db(template_name=template,language=language_value.capitalize())
    if (response_data == []):
        error = "Response missing in DB-> "+template+","+language_value
        text = "Error. response missing in D-B "+ template+", "+language_value
        if ("testing" in account_name):
            bot_response["text"] = text+"<template>"+template+"<template>"+"1234"+"<template>"+"ABCD"+"<template>"+"Response Missing in DB"+"<template>"+"123456"+"<template>"+"NOTrequired"+"<template>"+str(args)+"<template>"+text+"<template>"+language_value
        else:
            bot_response["text"] = ""+"<template>"+template+"<template>"+"1234"+"<template>"+"ABCD"+"<template>"+"Response Missing in DB "+template+"<template>"+"123456"+"<template>"+"NOTrequired"+"<template>"+str(args)+"<template>"+text+"<template>"+language_value
    else:
        data = response_data[0]

        try:
            if audio_server == "False":
                print("The response date from Mongo English",response_data)
                raw_text = data["message"]
                text = raw_text.format(**(args)).format(**args) 
                transcript_text = data["message"].format(**(args)).format(**args)
                bot_response["text"] = text+"<template>"+template+"<template>"+"1234"+"<template>"+"ABCD"+"<template>"+"12345qwerty"+"<template>"+"123456"+"<template>"+"NOTrequired"+"<template>"+str(args)+"<template>"+transcript_text+"<template>"+language_value
            else:
                print("coming here")
                raw_text = data["message"]
                print("message",raw_text)
                number_entitites_list = ["{monthly_emi}","{EMI_Amount}","{emi_amount}","{intrest_rate}","{loan_remaining_amount}","{late_fee_percentage}","{principal_amount}","{amount}","{partial_payment_amount}","{ptp_partial_amount}","{total_emi}","{no_of_loans}","{total_amount}","{min_amount_percentage}","{dpd_days}","{interest_rate}","{DPD_Days}","{DPD_days}","{max_amount_percentage}","{EMI_amount}","{total_loan_amount}","{min_pp_percentage}","{min_pp_amount}","{max_pp_amount}","{Threshold_time}","{threshold_time}","{payment_threshold_days}","{offer_amount}","{amount}"]#,"{PTP_date}","{PTP_Date}","{ptp_date}"
                for i in number_entitites_list:
                    if i in raw_text:
                        print("The value of I",i)
                        i = i.replace("{", "").replace("}", "")
                        number = args[i]
                        print("The number getting pased",number)
                        print(":coming here")
                        change_amount = await convert_numbers(str(number),language_value.lower()) 
                        print(":coming here")
                        args.update({i: change_amount})
                transcript = data["message"]
                transcript_text = transcript.format(**(args)).format(**args)
                text = raw_text.format(**(args)).format(**args)
                
                callId = ""
                campaignId = ""
                audio_id = data["audioId"]
                hash_obj = await hash_conversion(audio_id,sessionID)
                bot_response["text"] = text+"<template>"+template+"<template>"+callId+"<template>"+audio_id+"<template>"+hash_obj+"<template>"+campaignId+"<template>"+raw_text+"<template>"+str(args)+"<template>"+transcript_text+"<template>"+language_value
        except Exception as e:
            error = "ERROR: Entity issue--> "+template+language_value+ "---->" +str(e)
            raw_text = data.get("message",None)
            text = "Error. response entity issue "+ template
            if ("testing" in account_name):
                bot_response["text"] = text+"<template>"+template+"<template>"+"1234"+"<template>"+"ABCD"+"<template>"+"Response Entity issue"+"<template>"+"123456"+"<template>"+raw_text+"<template>"+str(args)+"<template>"+str(e)
            else:
                bot_response["text"] = ""+"<template>"+template+"<template>"+"1234"+"<template>"+"ABCD"+"<template>"+"Response Entity issue"+"<template>"+"123456"+"<template>"+raw_text+"<template>"+str(args)+"<template>"+str(e)
    return bot_response


# async def generate_response(nlg_call):
#     """Mock response generator.

#     Generates the responses from the bot's domain file.
#     """
#     args = nlg_call.get("arguments", {})
#     print("Args", args)
#     template = nlg_call.get("template")
#     bot_response = dict()
#     utterance_transcript = "English Responses"
#     utterance = 'English TTS'
#     audio_code = 'English_Audio_ID'
#     print("Started reading JSON files")
#     json_data = "nlg/emi_english/json_files/"
#     files = os.listdir(json_data)
#     data = []
    
#     for f in files:
#         with open(json_data + f, "r+", encoding='utf-8') as q:
#             try:
#                 data1 = json.load(q)
#                 data = data +data1
#             except Exception as e:
#                 print(e)
#     print("Completed reading JSON files",flush = True)
#     for item in data:
#         if item and "Response_ID" in item and item["Response_ID"] == template and \
#                 utterance in item:
#             if "buttons" in item and item["buttons"] and item["buttons"] == "":
#                 text = "".join(x.get(utterance, '') for x in item)
#                 args_list = list(args.keys())
#                 audio_id = "".join(item.get(audio_code))
#                 if len(args_list) == 0:
#                     bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id
#                 else:
#                     text = text.format(**args)
#                     bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id
#             else:
#                 text = "".join(item.get(utterance))
#                 text_1 = "".join(item.get(utterance_transcript))
#                 audio_id = "".join(item.get(audio_code))
#                 print("TEXT: ", text)
#                 args_list = list(args.keys())
#                 print("ARG: ", args_list)
#                 if len(args_list) == 0:
#                     bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id+"<transcript_text>"+text_1
#                 else:
#                     text = text.format(**args)
#                     text_1 = text_1.format(**args)
#                     bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id+"<transcript_text>"+text_1

#                 x = ast.literal_eval(item["buttons"]) if "buttons" in item and \
#                                                          item["buttons"] else []
#                 bot_response["buttons"] = x
#     return bot_response


def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/nlg", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        in_time=datetime.datetime.now()
        nlg_call = request.json
        print("NLG Response", nlg_call)
        bot_response = await generate_response(nlg_call)
        end_time=datetime.datetime.now()
        delay=end_time-in_time
        sender_id = nlg_call["tracker"]["sender_id"]
        out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
        nlg_logger.info(out_time)
        return response.json(bot_response)

    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)
