import asyncio
from distutils.log import debug
import logging
from datetime import datetime
from calendar import monthrange
import re
from dateutil import relativedelta
from aiohttp import ClientSession, ClientConnectorError
from flask import Flask, request, jsonify
import requests
import datetime

#logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

nlu_logger = setup_logger('nlu_logger', 'logs/nlu_logger.log')


URLS = [
    # 'https://stage-fullertonnlu.saarthi.ai/predict',
    'https://prod-fullerton-nlu.saarthi.ai/predict'
]

hindi_to_english = {
    "नेक्सट": "अगला",
    "दिस": "यह",
    "फर्स्ट": "प्रथम",
    "सैकंड": "दूसरा",
    "लास्ट": "पिछले",
    "बिफोर": "पहले",
    "प्रीवियस": "पिछला",
    "मंडे": "सोमवार",
    "ट्यूसडे": "मंगलवार",
    "वेडनेसडे": "बुधवार",
    "थर्सडे": "गुरूवार",
    "फ्राइडे": "शुक्रवार",
    "सैटरडे": "शनिवार",
    "संडे": "रविवार",
    "जनुअरी": "जनवरी",
    "फेब्रुअरी": "फ़रवरी",
    "मार्च": "जुलूस",
    "अप्रैल": "अप्रैल",
    "मई": "मई",
    "जून": "जून",
    "जुलाई": "जुलाई",
    "अगस्त": "अगस्त",
    "सितम्बर": "सितंबर",
    "अक्टूबर": "अक्टूबर",
    "नवंबर": "नवंबर",
    "दिसंबर": "दिसंबर"
}

other_dates = {
    "दिन": "day",
    "दिनों": "days",
    "हफ्ता": "week",
    "हफ्ते": "weeks",
    "सप्ताह": "week",
    "अगले": "next",
    "डे": "day"
}
app = Flask(__name__)
loop = asyncio.new_event_loop()


def handle_other_dates(message):
    day_flag = False
    week_flag = False
    numeric_value = None
    if "दिन" in message or "दिनों" in message or "डे" in message:
        day_flag = True
    if "हफ्ता" in message or "हफ्ते" in message or "सप्ताह" in message:
        week_flag = True
    for item in message:
        if item.isdigit():
            numeric_value = item
            break
    if numeric_value and day_flag:
        return get_duckling_entities("call me after {} {}".format(numeric_value, "days"))
    if week_flag:
        return get_duckling_entities("call me next week")
    if day_flag and numeric_value is None:
        return get_duckling_entities("call me in a day")


async def fetch_html(url: str, session: ClientSession, **kwargs):
    msg = kwargs['msg']
    try:
        resp = await session.request(method="POST", url=url, json={"text": str(msg)})
    except ClientConnectorError:
        return (url, 404)
    return await resp.json()


async def make_requests(urls, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                fetch_html(url=url, session=session, **kwargs)
            )
        results = await asyncio.gather(*tasks)

    return results


def extract_date_time(duckling_response):
    entity = {}
    if duckling_response:
        try:
            if duckling_response[0]['dim'] == 'time':

                if 'value' in duckling_response[0]['value']:
                    str_date_time = duckling_response[0]['value']['value']
                    date_time_obj = datetime.datetime.strptime(str_date_time[:16], '%Y-%m-%dT%H:%M')
                    user_time_diff = datetime.datetime.strptime(str_date_time[:19], '%Y-%m-%dT%H:%M:%S')
                    curr_time = datetime.datetime.now()
                    print(curr_time, user_time_diff)
                    time_diff = (curr_time - user_time_diff).total_seconds()
                    print("TIME DIFF: ", time_diff)
                    if time_diff <= 5 and time_diff >= -10:
                        return entity
                    else:
                        entity['time'] = date_time_obj.strftime('%I %M %p')
                        entity['date'] = date_time_obj.strftime('%d/%m/%Y')
                        entity['start'] = duckling_response[0]['start']
                        entity['end'] = duckling_response[0]['end']
                    return entity

                elif 'values' in duckling_response[0]['value']:
                    print("IN VALUES")
                    str_date_time = duckling_response[0]['value']['from']['value']
                    print("STR: ", str_date_time)
                    date_time_obj = datetime.datetime.strptime(str_date_time[:16], '%Y-%m-%dT%H:%M')
                    user_time_diff = datetime.datetime.strptime(str_date_time[:19], '%Y-%m-%dT%H:%M:%S')
                    curr_time = datetime.datetime.now()
                    print(curr_time, user_time_diff)
                    time_diff = (curr_time - user_time_diff).total_seconds()
                    print("TIME DIFF: ", time_diff)
                    if time_diff <= 5 and time_diff >= -10:
                        return entity
                    else:
                        entity['time'] = date_time_obj.strftime('%I %M %p')
                        entity['date'] = date_time_obj.strftime('%d/%m/%Y')
                        entity['start'] = duckling_response[0]['start']
                        entity['end'] = duckling_response[0]['end']
                    return entity
                else:
                    return entity


        except:
            return entity
    else:
        return entity

def get_date(message):
    match=re.search(r"[0-9]+",message)
    entity_details=[]
    if match:
        given_number=int(match.group(0))
        print("Given number:",given_number)
        if given_number>0:
            current_day=datetime.datetime.now().day
            current_month=datetime.datetime.now().month
            current_year=datetime.datetime.now().year
            predict_month=current_month
            predict_year=current_year
            if given_number<current_day:
                if current_month==12:
                    predict_month=1
                    predict_year=current_year+1
                else:
                    predict_month=current_month+1
                num_days=monthrange(predict_year,predict_month)
                if len(str(predict_month))==1:
                    predict_month="0"+str(predict_month)
                if given_number<=num_days[1]:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'date',
                        'extractor': 'own',
                        'start': match.span()[0],
                        'value': str(given_number)+"/"+str(predict_month)+"/"+str(predict_year)[2:]
                    })
                else:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'number',
                        'extractor': 'own',
                        'start': match.span()[0],
                        'value': str(given_number)
                    })
            else:
                num_days=monthrange(predict_year,predict_month)
                if len(str(predict_month))==1:
                    predict_month="0"+str(predict_month)
                if given_number<=num_days[1]:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'date',
                        'extractor': 'own',
                        'start': match.span()[0],
                        'value': str(given_number)+"/"+str(predict_month)+"/"+str(predict_year)[2:]
                    })
                else:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'number',
                        'extractor': 'own',
                        'start': match.span()[0],
                        'value': str(given_number)
                    })
        else:
            entity_details.append({
                'confidence': 1.0,
                'end': match.span()[1],
                'entity': 'number',
                'extractor': 'own',
                'start': match.span()[0],
                'value': str(given_number)
            })
    if "नेक्स्ट मंथ" in message or "अगले महीने" in message:
        next_month=datetime.date.today()+relativedelta.relativedelta(months=1)
        date=str(next_month.day)+"/"+str(next_month.month)+"/"+str(next_month.year)[2:]
        entity_details.append({
                'confidence': 1.0,
                'end': len(message),
                'entity': 'date',
                'extractor': 'own',
                'start': 0,
                'value': date
            })
    return entity_details
def get_duckling_entities(message):
    try:
        data = [('locale', 'en_IN'), ('text', message), ('tz', 'localtime')]
        duckling_response = requests.post('http://168.62.57.226/duckling', data=data).json()

        print("DUCKLING UNFORMATTED: ", duckling_response)

        time_date_entity = extract_date_time(duckling_response)
        duckling_entity = []

        if time_date_entity:

            if time_date_entity['date']:
                duckling_entity.append({
                    "confidence": 1.0,
                    "end": time_date_entity['end'],
                    "entity": "date",
                    "extractor": "duckling",
                    "start": time_date_entity['start'],
                    "value": time_date_entity['date']
                })

            if time_date_entity['time'] and time_date_entity['time'] != '12 00 AM':
                duckling_entity.append({
                    "confidence": 1.0,
                    "end": time_date_entity['end'],
                    "entity": "time",
                    "extractor": "duckling",
                    "start": time_date_entity['start'],
                    "value": time_date_entity['time']
                })
        return duckling_entity, duckling_response
    except:
        return []


def replace_english_words_in_english_utterance(text):
    for item in hindi_to_english:
        if item in text:
            text.replace(item, hindi_to_english[item])
    return text

# list_of_signals_to_intent = ["language_change","offers","interest_rate","tenure","document_required","emi_amount","who_are_you"
#                              ,"information","processing_time","credit_limit","location","change","income_proof"
#                              ,"send_executive","visit","exchange_scheme","vehicle_purchase","client_name","credit_score"]

list_of_signals_to_intent = ["language_change","offers","tenure","document_required","emi_amount","who_are_you"
                             ,"information","processing_time","credit_limit","location","change","income_proof"
                             ,"send_executive","visit","exchange_scheme","vehicle_purchase","client_name",
                             "due_date","bounce_charges","penalty_charges","talk_to_human_agent","processing_fees",
                             "credit_score","interest_rate","processing_time","preclosure_period","autodebit","insurance_info","health_insurance","settlement","validity","offer","documents","premium_amount","benefits","out_of_context"]
                             
# list_of_signals_to_intent = ["language_change","balance_transfer","topup","benefits","tax_benefits","floating_interest_rate",
# "document_required","foreclosure_charges","partial_payment_charges","processing_fees","charges","who_are_you","client_name","interest_rate","credit_limit","processing_time","another","documents_required","foreclosure_charges_partial_payment_charges","information"]
list_of_delay_reason_to_intent = ["no_aware"]

list_of_sub_intent_to_intent = ["greet","wait","repeat","gibberish","sorry","bye"]

list_of_context_to_intent = ["two_wheeler_loan","three_wheeler_loan","four_wheeler_loan","personal_loan","property_loan","travel_loan","wedding_loan","gold_loan","business_loan","insurance"]


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/model/parse', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.json
    in_time=datetime.datetime.now()
    msg = str(data["text"])
    print(msg)

    nlu = dict()
    if str(msg).lower() == "hello" or str(msg).lower() == "hey":

        nlu['intent'] = {'name': 'greet', 'confidence': 1.0}
        nlu['entities'] = []
        nlu['intent_ranking'] = [{'name': 'greet', 'confidence': 1.0},
                                 {'name': 'affirm', 'confidence': 0.00000003},
                                 {'name': 'deny', 'confidence': 0.0000000001}]
        nlu['text'] = str(msg)
    else:
        print("entering inside nlu lnk",msg)
        if "<nlu_data>" not in msg:
            formatted_intent_response_sub_intent = []
            formatted_intent_response_Humiliate = []
            formatted_intent_response_sub_context = []
            formatted_intent_response_delay_reason = []
            formatted_intent_response_sentiment = []
            formatted_intent_response_context = []
            formatted_intent_response_third_person = []
            formatted_intent_response_signal = []
            formatted_intent_response_intent = []
            val = "normal"
            print("The value of msg",msg)
            intent_response_1 = loop.run_until_complete(make_requests(urls=URLS, msg=msg))
            print("The value of msg qwe",intent_response_1)
            intent_response = [intent_response_1[0]["response"]]
            print("The value of msg",intent_response)

            msg = replace_english_words_in_english_utterance(str(msg))
            msg = msg.lower()
            try:
                entity_response = requests.post('http://20.204.204.228:8000/predict',json={"text": str(msg),"lang":"malayalam"}).json()
            except:
                logging.error("Hindi NER link error")

            for item in intent_response[0]['sub_intent']:
                formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['humiliate']:
                formatted_intent_response_Humiliate.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['sub_context']:
                formatted_intent_response_sub_context.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['delay_reason']:
                formatted_intent_response_delay_reason.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['sentiment']:
                formatted_intent_response_sentiment.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['context']:
                formatted_intent_response_context.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['intent']:
                formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response[0]['third_person']:
                formatted_intent_response_third_person.append({"name": item["name"], "confidence": float(item["confidence"])}) 
            for item in intent_response[0]['signal']:
                formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})
        else:
            formatted_intent_response_sub_intent = []
            formatted_intent_response_Humiliate = []
            formatted_intent_response_sub_context = []
            formatted_intent_response_delay_reason = []
            formatted_intent_response_sentiment = []
            formatted_intent_response_context = []
            formatted_intent_response_third_person = []
            formatted_intent_response_signal = []
            formatted_intent_response_intent = []

            val = "exotel"
            intent_response_temp = msg.split("<nlu_data>")
            msg = str(intent_response_temp[0])
            print("Intent response 555555********",intent_response_temp)
            print(len(intent_response_temp))
            intent_response = eval(intent_response_temp[1])
            entity_response = eval(intent_response_temp[2])
            print("entuty resesssssssss",entity_response)
            print("intent_response *******", intent_response)
       
            # keys_intent=intent_response[0].keys()
            for item in intent_response['sub_intent']:
                formatted_intent_response_sub_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['humiliate']:
                formatted_intent_response_Humiliate.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['sub_context']:
                formatted_intent_response_sub_context.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['delay_reason']:
                formatted_intent_response_delay_reason.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['sentiment']:
                formatted_intent_response_sentiment.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['context']:
                formatted_intent_response_context.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['intent']:
                formatted_intent_response_intent.append({"name": item["name"], "confidence": float(item["confidence"])})
            for item in intent_response['third_person']:
                formatted_intent_response_third_person.append({"name": item["name"], "confidence": float(item["confidence"])}) 
            for item in intent_response['signal']:
                formatted_intent_response_signal.append({"name": item["name"], "confidence": float(item["confidence"])})

        print("formatted_intent_response_sub_intent",formatted_intent_response_sub_intent)
        print("formatted_intent_response_Humiliate",formatted_intent_response_Humiliate)
        print("formatted_intent_response_sub_context",formatted_intent_response_sub_context)
        print("formatted_intent_response_delay_reason",formatted_intent_response_delay_reason)
        print("formatted_intent_response_sentiment",formatted_intent_response_sentiment)
        print("formatted_intent_response_context",formatted_intent_response_context)
        print("formatted_intent_response_intent",formatted_intent_response_intent)
        print("formatted_intent_response_third_person",formatted_intent_response_third_person)
        print("formatted_intent_response_signal",formatted_intent_response_signal)
        print("intent_response", intent_response)

        # msg = replace_english_words_in_english_utterance(str(msg))
        # try:
        #     entity_response = requests.post('http://52.147.223.178:80/api/v1/service/production-ner/score',json={"data": str(msg),"lang":"english"}).json()
        # except:
        #     logging.error("English NER link error")
        #     entity_response={"entities":[]}
        print("The entity response is *************",entity_response)
        # entity_response={"entities":[]}
        if val == "normal":
            entity_response = entity_response["entities"]
        if val == "exotel":
            entity_response = entity_response
        for item in entity_response:
            if item["entity"] == "time" and "DF" in item["value"]:
                value = item["value"].replace("DF", "").replace(" 00", "")
                value = "call me after {} hours".format(value)
                duckling_response, _duckling_response = get_duckling_entities(value)
                for entity in duckling_response:
                    if entity["entity"] == "time":
                        item["value"] = entity["value"]
                    date_flag = False
                    if entity["entity"] == "date":
                        for date_entity in entity_response:
                            if date_entity["entity"] == "date":
                                date_flag = True
                        if not date_flag:
                            entity_response.append(entity)
        print("entity response", entity_response)
        print("The valu *****",formatted_intent_response_signal[0]["name"])
        if formatted_intent_response_signal[0]["name"] in list_of_signals_to_intent:
            print("Entering into conversion of signals to intents")
            nlu['sub_intent'] = formatted_intent_response_sub_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_intent
            nlu['Humiliate'] = formatted_intent_response_Humiliate[0]
            nlu['intent_ranking'] = formatted_intent_response_Humiliate
            nlu['sub_context'] = formatted_intent_response_sub_context[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_context
            nlu['delay_reason'] = formatted_intent_response_delay_reason[0]
            nlu['intent_ranking'] = formatted_intent_response_delay_reason
            nlu['sentiment'] = formatted_intent_response_sentiment[0]
            nlu['intent_ranking'] = formatted_intent_response_sentiment
            nlu['context'] = formatted_intent_response_context[0]
            nlu['intent_ranking'] = formatted_intent_response_context
            nlu['third_person'] = formatted_intent_response_third_person[0]
            nlu['intent_ranking'] = formatted_intent_response_third_person
            nlu['signal'] = formatted_intent_response_signal[0]
            nlu['intent_ranking'] = formatted_intent_response_signal
            nlu['intent'] = formatted_intent_response_signal[0]
            nlu['intent_ranking'] = formatted_intent_response_signal
            nlu["temp_intent"] = formatted_intent_response_intent[0]
            nlu["temp_delay"] = "NONE"
            nlu["temp_sub_intent"] = "NONE"
        elif formatted_intent_response_delay_reason[0]["name"] in list_of_delay_reason_to_intent:
            print("Entering into conversion of delay reason to intents")
            nlu['sub_intent'] = formatted_intent_response_sub_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_intent
            nlu['Humiliate'] = formatted_intent_response_Humiliate[0]
            nlu['intent_ranking'] = formatted_intent_response_Humiliate
            nlu['sub_context'] = formatted_intent_response_sub_context[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_context
            nlu['delay_reason'] = formatted_intent_response_delay_reason[0]
            nlu['intent_ranking'] = formatted_intent_response_delay_reason
            nlu['sentiment'] = formatted_intent_response_sentiment[0]
            nlu['intent_ranking'] = formatted_intent_response_sentiment
            nlu['context'] = formatted_intent_response_context[0]
            nlu['intent_ranking'] = formatted_intent_response_context
            nlu['third_person'] = formatted_intent_response_third_person[0]
            nlu['intent_ranking'] = formatted_intent_response_third_person
            nlu['signal'] = formatted_intent_response_signal[0]
            nlu['intent_ranking'] = formatted_intent_response_signal
            nlu['intent'] = formatted_intent_response_delay_reason[0]
            nlu['intent_ranking'] = formatted_intent_response_delay_reason
            nlu["temp_intent"] = "NONE"
            nlu["temp_delay"] = formatted_intent_response_intent[0]
            nlu["temp_sub_intent"] = "NONE"
            print("The NLU value is",nlu)
        elif formatted_intent_response_sub_intent[0]["name"] in list_of_sub_intent_to_intent:
            print("Entering into conversion of sub_intent to intents")
            nlu['sub_intent'] = formatted_intent_response_sub_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_intent
            nlu['Humiliate'] = formatted_intent_response_Humiliate[0]
            nlu['intent_ranking'] = formatted_intent_response_Humiliate
            nlu['sub_context'] = formatted_intent_response_sub_context[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_context
            nlu['delay_reason'] = formatted_intent_response_delay_reason[0]
            nlu['intent_ranking'] = formatted_intent_response_delay_reason
            nlu['sentiment'] = formatted_intent_response_sentiment[0]
            nlu['intent_ranking'] = formatted_intent_response_sentiment
            nlu['context'] = formatted_intent_response_context[0]
            nlu['intent_ranking'] = formatted_intent_response_context
            nlu['third_person'] = formatted_intent_response_third_person[0]
            nlu['intent_ranking'] = formatted_intent_response_third_person
            nlu['signal'] = formatted_intent_response_signal[0]
            nlu['intent_ranking'] = formatted_intent_response_signal
            nlu['intent'] = formatted_intent_response_sub_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_intent
            nlu["temp_intent"] = "NONE"
            nlu["temp_delay"] = "NONE"
            nlu["temp_sub_intent"] = formatted_intent_response_intent[0]

        elif formatted_intent_response_context[0]["name"] in list_of_context_to_intent:
            print("Entering into conversion of sub_intent to intents")
            nlu['sub_intent'] = formatted_intent_response_sub_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_intent
            nlu['Humiliate'] = formatted_intent_response_Humiliate[0]
            nlu['intent_ranking'] = formatted_intent_response_Humiliate
            nlu['sub_context'] = formatted_intent_response_sub_context[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_context
            nlu['delay_reason'] = formatted_intent_response_delay_reason[0]
            nlu['intent_ranking'] = formatted_intent_response_delay_reason
            nlu['sentiment'] = formatted_intent_response_sentiment[0]
            nlu['intent_ranking'] = formatted_intent_response_sentiment
            nlu['context'] = formatted_intent_response_context[0]
            nlu['intent_ranking'] = formatted_intent_response_context
            nlu['third_person'] = formatted_intent_response_third_person[0]
            nlu['intent_ranking'] = formatted_intent_response_third_person
            nlu['signal'] = formatted_intent_response_signal[0]
            nlu['intent_ranking'] = formatted_intent_response_signal
            nlu['intent'] = formatted_intent_response_context[0]
            nlu['intent_ranking'] = formatted_intent_response_context
            nlu["temp_intent"] = "NONE"
            nlu["temp_delay"] = "NONE"
            nlu["temp_sub_intent"] = formatted_intent_response_intent[0]
        else:
            nlu['sub_intent'] = formatted_intent_response_sub_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_intent
            nlu['Humiliate'] = formatted_intent_response_Humiliate[0]
            nlu['intent_ranking'] = formatted_intent_response_Humiliate
            nlu['sub_context'] = formatted_intent_response_sub_context[0]
            nlu['intent_ranking'] = formatted_intent_response_sub_context
            nlu['delay_reason'] = formatted_intent_response_delay_reason[0]
            nlu['intent_ranking'] = formatted_intent_response_delay_reason
            nlu['sentiment'] = formatted_intent_response_sentiment[0]
            nlu['intent_ranking'] = formatted_intent_response_sentiment
            nlu['context'] = formatted_intent_response_context[0]
            nlu['intent_ranking'] = formatted_intent_response_context
            nlu['third_person'] = formatted_intent_response_third_person[0]
            nlu['intent_ranking'] = formatted_intent_response_third_person
            nlu['signal'] = formatted_intent_response_signal[0]
            nlu['intent_ranking'] = formatted_intent_response_signal
            nlu['intent'] = formatted_intent_response_intent[0]
            nlu['intent_ranking'] = formatted_intent_response_intent
            nlu["temp_intent"] = "NONE"
            nlu["temp_delay"] = "NONE"
            nlu["temp_sub_intent"] = "NONE"
        nlu['text'] = msg
        entities = []
        date_value = None
        time_value = None
        relation_value = None
        list_val = ["person","relation","location"]

        print("The value of NLU *******",nlu)
        if "entities" in entity_response and len(entity_response["entities"]) == 0:
            entity_response["entities"] = handle_other_dates(msg)
        if "entities" in entity_response and len(entity_response["entities"]) == 0:
            entity_response['entities']= get_date(msg)

        if entity_response and 'entities' in entity_response and entity_response is not None:
            for entity in entity_response['entities']:
                if date_value is None and entity["entity"] == "date":
                    try:
                        formatted_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except ValueError:
                        formatted_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                    date_value = formatted_date.strftime("%d/%m/%y")
                    entity["value"] = formatted_date.strftime("%d/%m/%y")
                    entities.append(entity)
                if time_value is None and entity["entity"] == "time":
                    time_value = entity["value"]
                    entities.append(entity)
                if relation_value is None and entity["entity"] in list_val:
                    pass
        print("The final entity response ",entity_response)
        nlu['entities'] = entity_response
        message = msg

        def isint(text):
            try:
                value = int(text)
                return True
            except:
                return False

        entity = dict()

        # for item in message.split(" "):
        #     print(item)
        #     if "₹" in item:
        #         item = item.replace("₹", "")
        #     if isint(item):
        #         entity['entity'] = 'number'
        #         entity['value'] = str(item)
        #         entity['start'] = message.index(item)
        #         entity['end'] = message.index(item) + len(item)

        if entity:
            nlu["entities"].append(entity)

        print(nlu)
    end_time=datetime.datetime.now()
    delay=end_time-in_time
    print("The nlu dart",data)
    # sender_id = data["sender_id"]
    out_time = "session_id %s"+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
    nlu_logger.info(out_time)
    return jsonify(nlu)


if __name__ == '__main__':
    app.run(debug = True,port=12525)
