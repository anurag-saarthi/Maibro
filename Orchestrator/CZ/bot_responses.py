import hashlib
import logging
import redis
import requests
import datetime
import socket
import aiohttp
hostname = socket.gethostname()
import os

from dotenv import dotenv_values
config = dotenv_values(".env")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

REDIS_HOST = "prod-saarthi-redis.1vscjj.ng.0001.aps1.cache.amazonaws.com"
REDIS_PASSWORD = ""

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
REDIS_DB = 14

REDIS_DB_CONV = "0"
red_english = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ENGLISH, password=REDIS_PASSWORD)
red_hindi = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_HINDI, password=REDIS_PASSWORD)
red_tamil = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_TAMIL, password=REDIS_PASSWORD)
red_malayalam = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_MALAYALAM, password=REDIS_PASSWORD)
red_lang = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)
audio_url = os.environ.get("audio_url")
if audio_url is None:
    # audio_url = "https://salesonboardingbot2.saarthi.ai/manappuram_tts"
    audio_url = "https://maiacollection1.saarthi.ai/creditwise_audio"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

core_logger = setup_logger('core_logger', 'logs/core_logger.log')

def find_hash(text,audio_code):
    updated_text = str(text)+audio_code
    hash_object = hashlib.md5(updated_text.encode('utf-8'))
    file_name = str(hash_object.hexdigest())
    return text, file_name


async def call_bot(url, sender_id, request_id, user_id, text):
    """Call to the bot Api"""
    bot_response = {
        "sender_id": "",
        "request_id": "",
        "user_id": "",
        "nlu_data": {
            "entities": [],
            "intent": {
                "confidence": 1,
                "name": "greet"
            },
            "intent_ranking": [],
            "text": ""
        },
        "custom": {
            "status": 701
        },
        "data": [
            {
                "text": "<speak>Server is Down. Please try after sometime</speak>",
                "buttons": [],
                "quick_replies": [],
                "hash": str(
                    hashlib.md5("<speak>Server is Down. Please try after sometime</speak>".encode('utf-8')).hexdigest())
            }
        ],
        "elements": [],
        "attachments": []
    }

    response = dict()
    try:
        data={"sender": sender_id, "request_id": request_id, "user_id": user_id,
                                            "message": str(text)}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=data) as resp:
                response = await resp.json()
                return response
        return response


    except requests.exceptions.HTTPError as errh:
        core_logger.exception("Http Error: {}".format(errh))
        return bot_response
    except requests.exceptions.ConnectionError as errc:
        core_logger.exception("HError Connecting: {}".format(errc))
        return bot_response
    except requests.exceptions.Timeout as errt:
        core_logger.exception("Timeout Error: {}".format(errt))
        return bot_response
    except requests.exceptions.RequestException as err:
        core_logger.exception("Error: {}".format(err))
        return bot_response
    return response


async def generate_response(nlg_call):
    """Mock response generator.
    Generates the responses from the bot's domain file.
    """
    print("English NLG:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    message = text
    intent_response = nlg_call.get("nlu_data", None)
    ner_data = nlg_call.get("ner_data", None)
    try:
        signal = intent_response["signal"][0]["name"]
    except:
        signal = text
    
    print("nlu",intent_response)
    print("ner_date from exotel",ner_data)

    if text == "/pre_emi" or text == "initial_message" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()
        print("text1111",text)

    if text != "/initial_message"  and intent_response != None and ner_data != None:
        if text != "/no_message":
            text = text+"<nlu_data>"+str(intent_response)+"<nlu_data>"+str(ner_data)

    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    

    session_value_hindi_old = red_english.get(str(sender_id)+"hindi")
    session_value_malayalam_old = red_english.get(str(sender_id)+"malayalam")
    session_value_tamil_old = red_english.get(str(sender_id)+"tamil")


    print("langauge_change in english code is---->",session_value_hindi_old)
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        bot_responses = await generate_response_hindi(nlg_call)
        red_english.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"english", "False", ex=300)
        return bot_responses
    if session_value_malayalam_old is not None and str(session_value_malayalam_old, 'utf-8') == "True":
        bot_responses = await generate_response_malayalam(nlg_call)
        red_english.set(str(sender_id)+"malayalam", "True", ex=300)
        red_malayalam.set(str(sender_id)+"english","False",ex = 300)
        return bot_responses
    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        bot_responses = await generate_response_tamil(nlg_call)
        red_english.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"english","False",ex = 300)
        return bot_responses
    
    try:
        any_variable = red_hindi.hget(str(sender_id),"language_change")
        any_variable = str(any_variable,'utf-8')
    except:
        any_variable = "False"

    if any_variable != "True":

        if "hindi" in message:
            print("entering here>>")
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                print("asdfghj345",intent_response)
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                # intent_response = intent_response.get("response")
                print("asdfghj345",intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                    print("Entering into language change form english to hindi after language change")
                    red_english.set(str(sender_id)+"hindi", "True", ex=300)
                    red_hindi.set(str(sender_id)+"english","False",ex = 300)
                    red_hindi.hset(str(sender_id),"language_change","True")
                    bot_responses = await generate_response_hindi(nlg_call)
                    return bot_responses


        if ("malayalam" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                print("asdfghj345",intent_response)
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print("asdfghj345",intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change form english to hindi")
                red_english.set(str(sender_id)+"malayalam", "True", ex=300)
                red_malayalam.set(str(sender_id)+"english","False", ex = 300)
                bot_responses = await generate_response_malayalam(nlg_call)
                return bot_responses

        
        if ("tamil" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                print("asdfghj345",intent_response)
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print("asdfghj345",intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change form english to hindi")
                red_english.set(str(sender_id)+"tamil", "True", ex=300)
                red_tamil.set(str(sender_id)+"english","False", ex = 300)
                bot_responses = await generate_response_tamil(nlg_call)
                return bot_responses


    url = "http://localhost:9434/webhooks/rest/webhook"
    in_time=datetime.datetime.now()
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    print("The out time in bot resonse",out_time)
    core_logger.info(out_time)
    print("The bot responses is ,",bot_response)
    temp_list = ["initial_message","ptp_reminder","no_message"]
    temp_intent_val = bot_response["nlu_data"]["intent"]["name"]
    try:
        if temp_intent_val not in temp_list:
            temp_delay = bot_response["nlu_data"]["temp_delay"]
            temp_intent = bot_response["nlu_data"]["temp_intent"]
            temp_sub_intent = bot_response["nlu_data"]["temp_sub_intent"]
            if temp_delay == "NONE" and temp_intent != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_intent["name"]
            if temp_intent == "NONE" and temp_delay != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_delay["name"]
            if temp_delay == "NONE" and temp_sub_intent!="NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_sub_intent["name"]

            del bot_response["nlu_data"]["temp_delay"]
            del bot_response["nlu_data"]["temp_intent"]
            del bot_response["nlu_data"]["temp_sub_intent"]
    except KeyError:
        pass
    # gender = bot_response["custom"]["bot_gender"]
    print("The bot response hindi*******",bot_response)
    # gender = bot_response["custom"]["bot_gender"]
    # if bot_response.get("custom", None) is None:
    #     bot_response["custom"] = {}
    if type(bot_response["custom"]) == list:
        disposition_list = []
        for i in bot_response["custom"]:
            disposition_list.append(i["disposition_id"])
            custom_response = i
            status_code = i["status"]
            lead_category_value = i["lead_category"]
        # bot_response["custom"] = bot_response["custom"][0]
        # bot_response["custom"] = custom_response
        bot_response["custom"] = bot_response["custom"][0]
        bot_response["custom"]["status"]=status_code
        bot_response["custom"]["disposition_id"] = disposition_list
        bot_response["custom"]["lead_category"]= lead_category_value
        
        
    bot_response["custom"]["tts"] = "en-IN"
    bot_response["custom"]["stt"] = "en-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "en-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    final_bot_responses = []
    print("bot_utterances",bot_utterances)
    for item in bot_utterances:

        message = item["text"].split("<template>")[0]
        a=item["text"].split("<template>")[1]
        template_name=a.split("<audio_id>")[0]
        item["temaplate_id"] = template_name
        b = a.split("<audio_id>")[1]
        audio_id = b.split("<transcript_text>")[0]
        transcript_text = b.split("<transcript_text>")[1]
        tts_text = item["text"].split("<template>")[0]
        item['text'] = transcript_text
        _,file_name = find_hash(text = message,audio_code=audio_id)
        item['hash']=file_name+"key"
        item['force']= 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language={language}&audio_server=mstts".format(message=tts_text, template_name=template_name, language="english",audio_url=audio_url) # tone = gender
        
        # split = item["text"].split("<template>")
        # item['force']=0
        # item['text']=split[0]
        # item['template_name'] = split[1]
        # item['callId'] = split[2]
        # item['audioId'] = split[3]
        # item['hash'] = split[4]
        # item['campaignId'] = split[5]
        # raw_text = split[6]
        # item["raw_text"] = raw_text
        # if "{" in raw_text:
        #     item["isDynamic"] = True
        # else:
        #     item["isDynamic"] = False
        # item["entities"] = split[7]
        # item["transcript_text"] = split[8]
        # item["gender"] = "M"
        # item["isMaia"] = "True"
        # item["language"]=split[9]
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses
    return bot_response


async def generate_response_hindi(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("Hindi NLG Call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    message = text
    intent_response = nlg_call.get("nlu_data", None)
    ner_data = nlg_call.get("ner_data", None)
    supported_languages = red_lang.get(str(sender_id+"supported_languages"))
    print("text",text)
    print("nlu",intent_response)
    print("ner",ner_data)

    print("Stored")
    if text == "/pre_emi" or text == "initial_message" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if text != "/initial_message"  and intent_response != None and ner_data != None:
        if text != "/no_message":
            text = text+"<nlu_data>"+str(intent_response)+"<nlu_data>"+str(ner_data)
    
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response
    
    session_value_english_old = red_hindi.get(str(sender_id)+"english")
    session_value_tamil_old = red_hindi.get(str(sender_id)+"tamil")
    session_value_malayalam_old = red_hindi.get(str(sender_id)+"malayalam")
    print("session_value_english_old---->hindi",session_value_english_old)


    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        bot_responses = await generate_response(nlg_call)
        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"hindi", "False", ex=300)
        return bot_responses

    if session_value_malayalam_old is not None and str(session_value_malayalam_old, 'utf-8') == "True":
        bot_responses = await generate_response_malayalam(nlg_call)
        red_hindi.set(str(sender_id)+"malayalam", "True", ex=300)
        red_malayalam.set(str(sender_id)+"hindi","False",ex = 300)
        return bot_responses

    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        bot_responses = await generate_response_tamil(nlg_call)
        red_hindi.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"hindi","False",ex = 300)
        return bot_responses
    
    try:
        any_variable = red_hindi.hget(str(sender_id),"language_change")
        any_variable = str(any_variable,'utf-8')
    except:
        any_variable = "False"
    print("any_variable------->",any_variable)
    if any_variable != "True":
        if "english" in message or "इंग्लिश" in message:
            core_logger.info(f"fentering inside {message}{session_value_english_old}")
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                    print("Entering into language change from hindi to english")
                    red_hindi.set(str(sender_id)+"english", "True", ex=300)
                    red_english.set(str(sender_id)+"hindi","False",ex = 300)
                    red_hindi.hset(str(sender_id),"language_change","True")
                    bot_responses = await generate_response(nlg_call)
                    return bot_responses

        if ("तमिल" in message) and ("tamil" in supported_languages):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_hindi.set(str(sender_id)+"tamil", "True", ex=300)
                red_tamil.set(str(sender_id)+"hindi","False",ex = 300)
                bot_responses = await generate_response_tamil(nlg_call)
                return bot_responses


        if ("मलयालम" in message) and ("malayalam" in supported_languages):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_hindi.set(str(sender_id)+"malayalam", "True", ex=300)
                red_malayalam.set(str(sender_id)+"hindi","False",ex = 300)
                bot_responses = await generate_response_malayalam(nlg_call)
                return bot_responses
    else:
        pass
    url = "http://localhost:6434/webhooks/rest/webhook"

    in_time=datetime.datetime.now()
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    print("The bot responses is ,",bot_response)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    print("The out time in bot resonse",out_time)
    core_logger.info(out_time)
    temp_list = ["initial_message","ptp_reminder","no_message"]
    temp_intent_val = bot_response["nlu_data"]["intent"]["name"]
    try:
        if temp_intent_val not in temp_list:
            temp_delay = bot_response["nlu_data"]["temp_delay"]
            temp_intent = bot_response["nlu_data"]["temp_intent"]
            temp_sub_intent = bot_response["nlu_data"]["temp_sub_intent"]
            if temp_delay == "NONE" and temp_intent != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_intent["name"]
            if temp_intent == "NONE" and temp_delay != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_delay["name"]
            if temp_delay == "NONE" and temp_sub_intent!="NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_sub_intent["name"]

            del bot_response["nlu_data"]["temp_delay"]
            del bot_response["nlu_data"]["temp_intent"]
            del bot_response["nlu_data"]["temp_sub_intent"]
    except KeyError:
        pass

    print("The bot response hindi*******",bot_response)
    # gender = bot_response["custom"]["bot_gender"]
    # if bot_response.get("custom", None) is None:
    #     bot_response["custom"] = {}
    if type(bot_response["custom"]) == list:
        disposition_list = []
        for i in bot_response["custom"]:
            disposition_list.append(i["disposition_id"])
            custom_response = i
            status_code = i["status"]
            lead_category_value = i["lead_category"]
        # bot_response["custom"] = bot_response["custom"][0]
        # bot_response["custom"] = custom_response
        bot_response["custom"] = bot_response["custom"][0]
        bot_response["custom"]["status"]=status_code
        bot_response["custom"]["disposition_id"] = disposition_list   
        bot_response["custom"]["lead_category"]= lead_category_value
    
    bot_response["custom"]["tts"] = "hi-IN"
    bot_response["custom"]["stt"] = "hi-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "hi-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    print("The bot Utterance ********",bot_utterances)
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template>")[0]
        a=item["text"].split("<template>")[1]
        template_name=a.split("<audio_id>")[0]
        item["temaplate_id"] = template_name
        b = a.split("<audio_id>")[1]
        audio_id = b.split("<transcript_text>")[0]
        transcript_text = b.split("<transcript_text>")[1]
        item['text']=transcript_text
        # tts_text = item["text"].split("<template>")[0] 
        _,file_name = find_hash(text = message,audio_code=audio_id)
        # hash_object = hashlib.md5((message+template_name).encode('utf-8'))
        # file_name = str(hash_object.hexdigest())
        item['hash']=file_name+"key"
        item['force']= 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language={language}&audio_server=mstts".format(message=message, template_name=template_name, language="hindi",audio_url=audio_url) # tone = gender

        # split = item["text"].split("<template>")
        # item['force']=0
        # item['text']=split[0]
        # item['template_name'] = split[1]
        # item['callId'] = split[2]
        # item['audioId'] = split[3]
        # item['hash'] = split[4]
        # item['campaignId'] = split[5]
        # raw_text = split[6]
        # item["raw_text"] = raw_text
        # if "{" in raw_text:
        #     item["isDynamic"] = True
        # else:
        #     item["isDynamic"] = False
        # item["entities"] = split[7]
        # item["transcript_text"] = split[8]
        # item["gender"] = "M"
        # item["isMaia"] = "True"
        # item["language"]=split[9]
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses
    return bot_response


async def generate_response_tamil(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("Hindi NLG Call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    message = text
    intent_response = nlg_call.get("nlu_data", None)
    ner_data = nlg_call.get("ner_data", None)
    print("text",text)
    print("nlu",intent_response)
    print("ner",ner_data)

    print("Stored")
    if text == "/pre_emi" or text == "initial_message" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if text != "/initial_message"  and intent_response != None and ner_data != None:
        if text != "/no_message":
            text = text+"<nlu_data>"+str(intent_response)+"<nlu_data>"+str(ner_data)
    
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response
    
    session_value_english_old = red_tamil.get(str(sender_id)+"english")
    session_value_hindi_old = red_tamil.get(str(sender_id)+"hindi")
    # session_value_telugu_old=red_tamil.get(str(sender_id)+"telugu")
    # session_value_marathi_old = red_tamil.get(str(sender_id)+"marathi")
    # session_value_bengali_old = red_tamil.get(str(sender_id)+"bengali")
    session_value_malayalam_old = red_tamil.get(str(sender_id)+"malayalam")
    # session_value_punjabi_old = red_tamil.get(str(sender_id)+"punjabi")
    # session_value_gujarati_old = red_tamil.get(str(sender_id)+"gujarati")
    print("session_value_english_old---->hindi",session_value_english_old)


    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        bot_responses = await generate_response(nlg_call)
        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"hindi", "False", ex=300)
        return bot_responses
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        bot_responses = await generate_response_hindi(nlg_call)
        red_tamil.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"tamil", "False", ex=300)
        return bot_responses
    if session_value_malayalam_old is not None and str(session_value_malayalam_old, 'utf-8') == "True":
        bot_responses = await generate_response_malayalam(nlg_call)
        red_tamil.set(str(sender_id)+"malayalam", "True", ex=300)
        red_malayalam.set(str(sender_id)+"tamil", "False", ex=300)
        return bot_responses
    
    try:
        any_variable = red_hindi.hget(str(sender_id),"language_change")
        any_variable = str(any_variable,'utf-8')
    except:
        any_variable = "False"
    print("any_variable------->",any_variable)
    if any_variable != "True":
        if "இங்கிலிஷ்" in message:
            core_logger.info(f"fentering inside {message}{session_value_english_old}")
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                    print("Entering into language change from hindi to english")
                    red_tamil.set(str(sender_id)+"english", "True", ex=300)
                    red_english.set(str(sender_id)+"tamil","False",ex = 300)
                    red_english.hset(str(sender_id),"language_change","True")
                    bot_responses = await generate_response(nlg_call)
                    return bot_responses
        

        if ("ஹிந்தி" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_tamil.set(str(sender_id)+"hindi", "True", ex=300)
                red_hindi.set(str(sender_id)+"tamil","False",ex = 300)
                bot_responses = await generate_response_hindi(nlg_call)
                return bot_responses

        if ("மலையாளம்" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")

                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_tamil.set(str(sender_id)+"malayalam", "True", ex=300)
                red_malayalam.set(str(sender_id)+"tamil","False",ex=300)
                bot_responses = await generate_response_malayalam(nlg_call)
                return bot_responses
    else:
        pass
    url = "http://localhost:6334/webhooks/rest/webhook"

    in_time=datetime.datetime.now()
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    print("The bot responses is ,",bot_response)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    print("The out time in bot resonse",out_time)
    core_logger.info(out_time)
    temp_list = ["initial_message","ptp_reminder","no_message"]
    temp_intent_val = bot_response["nlu_data"]["intent"]["name"]
    try:
        if temp_intent_val not in temp_list:
            temp_delay = bot_response["nlu_data"]["temp_delay"]
            temp_intent = bot_response["nlu_data"]["temp_intent"]
            temp_sub_intent = bot_response["nlu_data"]["temp_sub_intent"]
            if temp_delay == "NONE" and temp_intent != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_intent["name"]
            if temp_intent == "NONE" and temp_delay != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_delay["name"]
            if temp_delay == "NONE" and temp_sub_intent!="NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_sub_intent["name"]

            del bot_response["nlu_data"]["temp_delay"]
            del bot_response["nlu_data"]["temp_intent"]
            del bot_response["nlu_data"]["temp_sub_intent"]
    except KeyError:
        pass

    print("The bot response hindi*******",bot_response)
    # gender = bot_response["custom"]["bot_gender"]
    # if bot_response.get("custom", None) is None:
    #     bot_response["custom"] = {}
    if type(bot_response["custom"]) == list:
        disposition_list = []
        for i in bot_response["custom"]:
            disposition_list.append(i["disposition_id"])
            custom_response = i
            status_code = i["status"]
            lead_category_value = i["lead_category"]
        # bot_response["custom"] = bot_response["custom"][0]
        # bot_response["custom"] = custom_response
        bot_response["custom"] = bot_response["custom"][0]
        bot_response["custom"]["status"]=status_code
        bot_response["custom"]["disposition_id"] = disposition_list   
        bot_response["custom"]["lead_category"]= lead_category_value
        
    # bot_response["custom"]["tts"] = "hi-IN"
    # bot_response["custom"]["stt"] = "hi-IN"
    # bot_response["custom"]["tts_gender"] = "FEMALE"
    # bot_response["custom"]["tts_speaking_rate"] = "0.9"
    # bot_response["custom"]["tts_voice_name"] = "hi-IN-Standard-A"
    # if "time_limit" not in bot_response.get("custom"):
    #     bot_response["custom"]["time_limit"] = 8

    bot_response["custom"]["tts"] = "ta-IN"
    bot_response["custom"]["stt"] = "ta-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "ta-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    print("The bot Utterance ********",bot_utterances)
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template>")[0]
        a=item["text"].split("<template>")[1]
        template_name=a.split("<audio_id>")[0]
        item["temaplate_id"] = template_name
        b = a.split("<audio_id>")[1]
        audio_id = b.split("<transcript_text>")[0]
        transcript_text = b.split("<transcript_text>")[1]
        item['text']=transcript_text
        # tts_text = item["text"].split("<template>")[0] 
        _,file_name = find_hash(text = message,audio_code=audio_id)
        # hash_object = hashlib.md5((message+template_name).encode('utf-8'))
        # file_name = str(hash_object.hexdigest())
        item['hash']=file_name+"key"
        item['force']= 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language={language}&audio_server=mstts".format(message=message, template_name=template_name, language="tamil",audio_url=audio_url) # tone = gender
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses
    return bot_response



async def generate_response_malayalam(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("malayalam NLG Call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    message = text
    intent_response = nlg_call.get("nlu_data", None)
    ner_data = nlg_call.get("ner_data", None)
    print("text",text)
    print("nlu",intent_response)
    print("ner",ner_data)

    print("Stored")
    if text == "/pre_emi" or text == "initial_message" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if text != "/initial_message"  and intent_response != None and ner_data != None:
        if text != "/no_message":
            text = text+"<nlu_data>"+str(intent_response)+"<nlu_data>"+str(ner_data)
    
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response
    
    # session_value_kannada_old = red_malayalam.get(str(sender_id)+"kannada")
    session_value_hindi_old = red_malayalam.get(str(sender_id)+"hindi")
    session_value_tamil_old=red_malayalam.get(str(sender_id)+"tamil")
    # session_value_telugu_old=red_malayalam.get(str(sender_id)+"telugu")
    # session_value_bengali_old=red_malayalam.get(str(sender_id)+"bengali")
    # session_value_punjabi_old = red_malayalam.get(str(sender_id)+"punjabi")
    # session_value_marathi_old = red_malayalam.get(str(sender_id)+"marathi")
    session_value_english_old = red_malayalam.get(str(sender_id)+"english")
    # session_value_gujarati_old = red_malayalam.get(str(sender_id)+"gujarati")
    print("session_value_english_old---->hindi",session_value_english_old)


    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        bot_responses = await generate_response(nlg_call)
        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"hindi", "False", ex=300)
        return bot_responses
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        bot_responses = await generate_response_hindi(nlg_call)
        red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"malayalam", "False", ex=300)
        return bot_responses
    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        bot_responses = await generate_response_tamil(nlg_call)
        red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"malayalam", "False", ex=300)
        return bot_responses
    
    try:
        any_variable = red_hindi.hget(str(sender_id),"language_change")
        any_variable = str(any_variable,'utf-8')
    except:
        any_variable = "False"
    print("any_variable------->",any_variable)
    if any_variable != "True":

        if "ഇംഗ്ലിഷ്" in message or "ഇംഗ്ലീഷ്" in message or "ഇംഗ്ലീഷു" in message:
            core_logger.info(f"fentering inside {message}{session_value_english_old}")
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                    print("Entering into language change from hindi to english")
                    red_malayalam.set(str(sender_id)+"english", "True", ex=300)
                    red_english.set(str(sender_id)+"malayalam","False",ex = 300)
                    red_hindi.hset(str(sender_id),"language_change","True")
                    bot_responses = await generate_response(nlg_call)
                    return bot_responses

        if ("ഹിന്ദി" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
                red_hindi.set(str(sender_id)+"malayalam","False",ex=300)
                bot_responses = await generate_response_hindi(nlg_call)
                return bot_responses

        if ("തമിഴ്" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                print("intent_response",intent_response)
                intent_response = intent_response.get("response")
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
                print(lang_change_val)
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
                red_tamil.set(str(sender_id)+"malayalam","False",ex=300)
                bot_responses = await generate_response_tamil(nlg_call)
                return bot_responses
    else:
        pass
    url = "http://localhost:6335/webhooks/rest/webhook"

    in_time=datetime.datetime.now()
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    print("The bot responses is ,",bot_response)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    print("The out time in bot resonse",out_time)
    core_logger.info(out_time)
    temp_list = ["initial_message","ptp_reminder","no_message"]
    temp_intent_val = bot_response["nlu_data"]["intent"]["name"]
    try:
        if temp_intent_val not in temp_list:
            temp_delay = bot_response["nlu_data"]["temp_delay"]
            temp_intent = bot_response["nlu_data"]["temp_intent"]
            temp_sub_intent = bot_response["nlu_data"]["temp_sub_intent"]
            if temp_delay == "NONE" and temp_intent != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_intent["name"]
            if temp_intent == "NONE" and temp_delay != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_delay["name"]
            if temp_delay == "NONE" and temp_sub_intent!="NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_sub_intent["name"]

            del bot_response["nlu_data"]["temp_delay"]
            del bot_response["nlu_data"]["temp_intent"]
            del bot_response["nlu_data"]["temp_sub_intent"]
    except KeyError:
        pass

    print("The bot response hindi*******",bot_response)
    # gender = bot_response["custom"]["bot_gender"]
    # if bot_response.get("custom", None) is None:
    #     bot_response["custom"] = {}
    if type(bot_response["custom"]) == list:
        disposition_list = []
        for i in bot_response["custom"]:
            disposition_list.append(i["disposition_id"])
            custom_response = i
            status_code = i["status"]
            lead_category_value = i["lead_category"]
        # bot_response["custom"] = bot_response["custom"][0]
        # bot_response["custom"] = custom_response
        bot_response["custom"] = bot_response["custom"][0]
        bot_response["custom"]["status"]=status_code
        bot_response["custom"]["disposition_id"] = disposition_list   
        bot_response["custom"]["lead_category"]= lead_category_value
        

    bot_response["custom"]["tts"] = "ml-IN"
    bot_response["custom"]["stt"] = "ml-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "ml-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    print("The bot Utterance ********",bot_utterances)
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template>")[0]
        a=item["text"].split("<template>")[1]
        template_name=a.split("<audio_id>")[0]
        item["temaplate_id"] = template_name
        b = a.split("<audio_id>")[1]
        audio_id = b.split("<transcript_text>")[0]
        transcript_text = b.split("<transcript_text>")[1]
        item['text']=transcript_text
        # tts_text = item["text"].split("<template>")[0] 
        _,file_name = find_hash(text = message,audio_code=audio_id)
        # hash_object = hashlib.md5((message+template_name).encode('utf-8'))
        # file_name = str(hash_object.hexdigest())
        item['hash']=file_name+"key"
        item['force']= 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language={language}&audio_server=mstts".format(message=message, template_name=template_name, language="malayalam",audio_url=audio_url) # tone = gender
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses
    return bot_response


async def generate_response_kannada(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("malayalam NLG Call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    message = text
    intent_response = nlg_call.get("nlu_data", None)
    ner_data = nlg_call.get("ner_data", None)
    print("text",text)
    print("nlu",intent_response)
    print("ner",ner_data)

    print("Stored")
    if text == "/pre_emi" or text == "initial_message" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if text != "/initial_message"  and intent_response != None and ner_data != None:
        if text != "/no_message":
            text = text+"<nlu_data>"+str(intent_response)+"<nlu_data>"+str(ner_data)
    
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response
    
    # session_value_kannada_old = red_malayalam.get(str(sender_id)+"kannada")
    session_value_hindi_old = red_malayalam.get(str(sender_id)+"hindi")
    session_value_tamil_old=red_malayalam.get(str(sender_id)+"tamil")
    # session_value_telugu_old=red_malayalam.get(str(sender_id)+"telugu")
    # session_value_bengali_old=red_malayalam.get(str(sender_id)+"bengali")
    # session_value_punjabi_old = red_malayalam.get(str(sender_id)+"punjabi")
    # session_value_marathi_old = red_malayalam.get(str(sender_id)+"marathi")
    session_value_english_old = red_malayalam.get(str(sender_id)+"english")
    # session_value_gujarati_old = red_malayalam.get(str(sender_id)+"gujarati")
    print("session_value_english_old---->hindi",session_value_english_old)


    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        bot_responses = await generate_response(nlg_call)
        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"hindi", "False", ex=300)
        return bot_responses
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        bot_responses = await generate_response_hindi(nlg_call)
        red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"malayalam", "False", ex=300)
        return bot_responses
    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        bot_responses = await generate_response_tamil(nlg_call)
        red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"malayalam", "False", ex=300)
        return bot_responses
    
    try:
        any_variable = red_hindi.hget(str(sender_id),"language_change")
        any_variable = str(any_variable,'utf-8')
    except:
        any_variable = "False"
    print("any_variable------->",any_variable)
    if any_variable != "True":

        if "ഇംഗ്ലിഷ്" in message or "ഇംഗ്ലീഷ്" in message or "ഇംഗ്ലീഷു" in message:
            core_logger.info(f"fentering inside {message}{session_value_english_old}")
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                    print("Entering into language change from hindi to english")
                    red_malayalam.set(str(sender_id)+"english", "True", ex=300)
                    red_english.set(str(sender_id)+"malayalam","False",ex = 300)
                    red_hindi.hset(str(sender_id),"language_change","True")
                    bot_responses = await generate_response(nlg_call)
                    return bot_responses

        if ("ഹിന്ദി" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
                red_hindi.set(str(sender_id)+"malayalam","False",ex=300)
                bot_responses = await generate_response_hindi(nlg_call)
                return bot_responses

        if ("തമിഴ്" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                print("intent_response",intent_response)
                intent_response = intent_response.get("response")
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
                print(lang_change_val)
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
                red_tamil.set(str(sender_id)+"malayalam","False",ex=300)
                bot_responses = await generate_response_tamil(nlg_call)
                return bot_responses
    else:
        pass
    url = "http://localhost:6336/webhooks/rest/webhook"

    in_time=datetime.datetime.now()
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    print("The bot responses is ,",bot_response)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    print("The out time in bot resonse",out_time)
    core_logger.info(out_time)
    temp_list = ["initial_message","ptp_reminder","no_message"]
    temp_intent_val = bot_response["nlu_data"]["intent"]["name"]
    try:
        if temp_intent_val not in temp_list:
            temp_delay = bot_response["nlu_data"]["temp_delay"]
            temp_intent = bot_response["nlu_data"]["temp_intent"]
            temp_sub_intent = bot_response["nlu_data"]["temp_sub_intent"]
            if temp_delay == "NONE" and temp_intent != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_intent["name"]
            if temp_intent == "NONE" and temp_delay != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_delay["name"]
            if temp_delay == "NONE" and temp_sub_intent!="NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_sub_intent["name"]

            del bot_response["nlu_data"]["temp_delay"]
            del bot_response["nlu_data"]["temp_intent"]
            del bot_response["nlu_data"]["temp_sub_intent"]
    except KeyError:
        pass

    print("The bot response hindi*******",bot_response)
    # gender = bot_response["custom"]["bot_gender"]
    # if bot_response.get("custom", None) is None:
    #     bot_response["custom"] = {}
    if type(bot_response["custom"]) == list:
        disposition_list = []
        for i in bot_response["custom"]:
            disposition_list.append(i["disposition_id"])
            custom_response = i
            status_code = i["status"]
            lead_category_value = i["lead_category"]
        # bot_response["custom"] = bot_response["custom"][0]
        # bot_response["custom"] = custom_response
        bot_response["custom"] = bot_response["custom"][0]
        bot_response["custom"]["status"]=status_code
        bot_response["custom"]["disposition_id"] = disposition_list   
        bot_response["custom"]["lead_category"]= lead_category_value
        

    bot_response["custom"]["tts"] = "kn-IN"
    bot_response["custom"]["stt"] = "kn-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "kn-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    print("The bot Utterance ********",bot_utterances)
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template>")[0]
        a=item["text"].split("<template>")[1]
        template_name=a.split("<audio_id>")[0]
        item["temaplate_id"] = template_name
        b = a.split("<audio_id>")[1]
        audio_id = b.split("<transcript_text>")[0]
        transcript_text = b.split("<transcript_text>")[1]
        item['text']=transcript_text
        # tts_text = item["text"].split("<template>")[0] 
        _,file_name = find_hash(text = message,audio_code=audio_id)
        # hash_object = hashlib.md5((message+template_name).encode('utf-8'))
        # file_name = str(hash_object.hexdigest())
        item['hash']=file_name+"key"
        item['force']= 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language={language}&audio_server=mstts".format(message=message, template_name=template_name, language="kannada",audio_url=audio_url) # tone = gender
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses
    return bot_response


async def generate_response_telugu(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("malayalam NLG Call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    message = text
    intent_response = nlg_call.get("nlu_data", None)
    ner_data = nlg_call.get("ner_data", None)
    print("text",text)
    print("nlu",intent_response)
    print("ner",ner_data)

    print("Stored")
    if text == "/pre_emi" or text == "initial_message" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if text != "/initial_message"  and intent_response != None and ner_data != None:
        if text != "/no_message":
            text = text+"<nlu_data>"+str(intent_response)+"<nlu_data>"+str(ner_data)
    
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response
    
    # session_value_kannada_old = red_malayalam.get(str(sender_id)+"kannada")
    session_value_hindi_old = red_malayalam.get(str(sender_id)+"hindi")
    session_value_tamil_old=red_malayalam.get(str(sender_id)+"tamil")
    # session_value_telugu_old=red_malayalam.get(str(sender_id)+"telugu")
    # session_value_bengali_old=red_malayalam.get(str(sender_id)+"bengali")
    # session_value_punjabi_old = red_malayalam.get(str(sender_id)+"punjabi")
    # session_value_marathi_old = red_malayalam.get(str(sender_id)+"marathi")
    session_value_english_old = red_malayalam.get(str(sender_id)+"english")
    # session_value_gujarati_old = red_malayalam.get(str(sender_id)+"gujarati")
    print("session_value_english_old---->hindi",session_value_english_old)


    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        bot_responses = await generate_response(nlg_call)
        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"hindi", "False", ex=300)
        return bot_responses
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        bot_responses = await generate_response_hindi(nlg_call)
        red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"malayalam", "False", ex=300)
        return bot_responses
    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        bot_responses = await generate_response_tamil(nlg_call)
        red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"malayalam", "False", ex=300)
        return bot_responses
    
    try:
        any_variable = red_hindi.hget(str(sender_id),"language_change")
        any_variable = str(any_variable,'utf-8')
    except:
        any_variable = "False"
    print("any_variable------->",any_variable)
    if any_variable != "True":

        if "ഇംഗ്ലിഷ്" in message or "ഇംഗ്ലീഷ്" in message or "ഇംഗ്ലീഷു" in message:
            core_logger.info(f"fentering inside {message}{session_value_english_old}")
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                    print("Entering into language change from hindi to english")
                    red_malayalam.set(str(sender_id)+"english", "True", ex=300)
                    red_english.set(str(sender_id)+"malayalam","False",ex = 300)
                    red_hindi.hset(str(sender_id),"language_change","True")
                    bot_responses = await generate_response(nlg_call)
                    return bot_responses

        if ("ഹിന്ദി" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                intent_response = intent_response.get("response")
                print(intent_response)
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
                red_hindi.set(str(sender_id)+"malayalam","False",ex=300)
                bot_responses = await generate_response_hindi(nlg_call)
                return bot_responses

        if ("തമിഴ്" in message):
            if intent_response != None:
                lang_change_val = intent_response["signal"][0]["name"]
            else:
                intent_response = requests.post('https://prod-fullerton-nlu.saarthi.ai/predict', json={"text": str(text)}).json()
                formatted_intent_response_sub_intent = []
                formatted_intent_response_intent = []
                formatted_intent_response_signal = []
                print("intent_response",intent_response)
                intent_response = intent_response.get("response")
                for item in intent_response['response']['sub_intent']:
                    print("item in sub_intent",item)
                    formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['intent']:
                    print("item in intent",item)
                    formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
                for item in intent_response['response']['signal']:
                    print("item in signal",item)
                    formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
                print(formatted_intent_response_sub_intent)
                print(formatted_intent_response_intent)
                print(formatted_intent_response_signal)
                print("*************",formatted_intent_response_signal[0]["name"])
                lang_change_val = formatted_intent_response_signal[0]["name"]
                print(lang_change_val)
            if lang_change_val == "language_change":
                print("Entering into language change from hindi to english")
                red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
                red_tamil.set(str(sender_id)+"malayalam","False",ex=300)
                bot_responses = await generate_response_tamil(nlg_call)
                return bot_responses
    else:
        pass
    url = "http://localhost:6337/webhooks/rest/webhook"

    in_time=datetime.datetime.now()
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    print("The bot responses is ,",bot_response)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    print("The out time in bot resonse",out_time)
    core_logger.info(out_time)
    temp_list = ["initial_message","ptp_reminder","no_message"]
    temp_intent_val = bot_response["nlu_data"]["intent"]["name"]
    try:
        if temp_intent_val not in temp_list:
            temp_delay = bot_response["nlu_data"]["temp_delay"]
            temp_intent = bot_response["nlu_data"]["temp_intent"]
            temp_sub_intent = bot_response["nlu_data"]["temp_sub_intent"]
            if temp_delay == "NONE" and temp_intent != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_intent["name"]
            if temp_intent == "NONE" and temp_delay != "NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_delay["name"]
            if temp_delay == "NONE" and temp_sub_intent!="NONE":
                bot_response["nlu_data"]["intent"]["name"] = temp_sub_intent["name"]

            del bot_response["nlu_data"]["temp_delay"]
            del bot_response["nlu_data"]["temp_intent"]
            del bot_response["nlu_data"]["temp_sub_intent"]
    except KeyError:
        pass

    print("The bot response hindi*******",bot_response)
    # gender = bot_response["custom"]["bot_gender"]
    # if bot_response.get("custom", None) is None:
    #     bot_response["custom"] = {}
    if type(bot_response["custom"]) == list:
        disposition_list = []
        for i in bot_response["custom"]:
            disposition_list.append(i["disposition_id"])
            custom_response = i
            status_code = i["status"]
            lead_category_value = i["lead_category"]
        # bot_response["custom"] = bot_response["custom"][0]
        # bot_response["custom"] = custom_response
        bot_response["custom"] = bot_response["custom"][0]
        bot_response["custom"]["status"]=status_code
        bot_response["custom"]["disposition_id"] = disposition_list   
        bot_response["custom"]["lead_category"]= lead_category_value
        

    bot_response["custom"]["tts"] = "te-IN"
    bot_response["custom"]["stt"] = "te-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "te-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    print("The bot Utterance ********",bot_utterances)
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template>")[0]
        a=item["text"].split("<template>")[1]
        template_name=a.split("<audio_id>")[0]
        item["temaplate_id"] = template_name
        b = a.split("<audio_id>")[1]
        audio_id = b.split("<transcript_text>")[0]
        transcript_text = b.split("<transcript_text>")[1]
        item['text']=transcript_text
        # tts_text = item["text"].split("<template>")[0] 
        _,file_name = find_hash(text = message,audio_code=audio_id)
        # hash_object = hashlib.md5((message+template_name).encode('utf-8'))
        # file_name = str(hash_object.hexdigest())
        item['hash']=file_name+"key"
        item['force']= 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language={language}&audio_server=mstts".format(message=message, template_name=template_name, language="telugu",audio_url=audio_url) # tone = gender
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses
    return bot_response