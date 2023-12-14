import datetime
import hashlib
import json
import re
import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_PATH_1 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(CURRENT_PATH)
from pydub import AudioSegment
from SaO_oneBot_audio_generator.gtts import synthesize_text as google_tts
from SaO_oneBot_audio_generator.gtts import mstts as mstts
from SaO_oneBot_audio_generator.gtts import saarthi_tts as saarthi_tts
from SaO_oneBot_audio_generator.convert_num_to_text import convert_numbers
from SaO_oneBot_audio_generator import toll_process,languages_integrated,convert_num_to_text

def detect_leading_silence(sound, silence_threshold=-40.0, chunk_size=10):
    trim_ms = 0
    assert chunk_size > 0
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size    
    return trim_ms

def trim_audios_silence(sound):
    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())
    duration = len(sound)   
    trimmed_sound = sound[start_trim:duration-end_trim]
    return trimmed_sound

def get_formatted_response(response):
    matches = re.findall(r"\{(.*?)\}", response)
    matches = ["{" + item + "}" for item in matches]
    split_regex = ""
    for item in range(len(matches)):
        if item != len(matches) - 1:
            split_regex += matches[item] + "|"
        else:
            split_regex += matches[item]
    sub_strings = re.split(split_regex, response)
    sub_strings.extend(matches)
    positions = {}
    formatted_responses = []
    for sub_string in sub_strings:
        if sub_string == ".":
            continue
        if sub_string!="":
            positon = response.find(sub_string)
            positions[positon] = sub_string
    for item in sorted(positions):
        formatted_responses.append(positions[item])
    return formatted_responses

def loudness_normalization(sound,target_dBFS=-15):
    loudness_difference = target_dBFS - sound.dBFS
    normalized_audio = sound + loudness_difference
    return normalized_audio

json_data = CURRENT_PATH_1 + "/nlg/emi_english/json_files/"
files = os.listdir(json_data)
data = []
for f in files:
    with open(json_data + f, "r+", encoding='utf-8') as q:
        try:
            data1 = json.load(q)
            data = data +data1
        except:
            pass

def generate_tts_files_static(message,utterance_name,audio_server,language):
    audio_id = utterance_name
    final_voice = None
    if audio_id + ".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/Static_Down/"):
        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Static_Down/{audio_id}.wav")
    else:
        returnval = eval(audio_server)(language=language,text = message,fileName=audio_id,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/Static_Down/")
        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Static_Down/{audio_id}.wav")
    return final_voice

def generate_tts_files_customer(utterance,message,utterance_name,audio_id,audio_server,language):
    message_1 = message
    final_voice = None
    formatted_responses = get_formatted_response(utterance)
    _entities = []
    for _response in formatted_responses:
        if "{" in _response:
            _entities.append(_response.replace("{", "").replace("}", ""))
        else:
            message = message.replace(_response, "-",1)
    message = message.split("-")
    formatted_values = []
    for _item in message:
        if _item:
            _item = _item.replace(".", "")
            _item = _item.strip()
            formatted_values.append(_item)
    entities = dict(zip(_entities, formatted_values))
    file_name = None
    for i in entities.values():
        if file_name is None:
            file_name = i
        else:
            file_name = file_name + "_" + i
    file_name = file_name+"_"+audio_id
    if file_name + ".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/Names_generated/"):
        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Names_generated/{file_name}.wav")
    else:
        _ = eval(audio_server)(language=language,text=message_1,fileName=file_name,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/Names_generated/")
        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Names_generated/{file_name}.wav")
    return final_voice
def trim_audio(sound):
    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())
    duration = len(sound)    
    final_voice = sound[start_trim:duration-end_trim]
    return final_voice

def generate_tts_files_dynamic(utterance, message,audio_id,utterance_name,audio_server,language):
    final_voice = None
    formatted_responses = get_formatted_response(utterance)
    _entities = []
    for _response in formatted_responses:
        if "{" in _response:
            _entities.append(_response.replace("{", "").replace("}", ""))
        else:
            message = message.replace(_response, "-",1)
    message = message.split("-")
    formatted_values = []
    for _item in message:
        if _item:
            _item = _item.replace(".", "")
            _item = _item.strip()
            formatted_values.append(_item)
    entities = dict(zip(_entities, formatted_values))
    count = 0
    for response in formatted_responses:
        print("response",response)
        print("entities",entities)
        if "{" in response:
            response = response.replace("{", "").replace("}", "")
            if response.lower() ==  "intrest_rate" or response.lower() == "loan_remaining_amount" or response.lower() == "no_of_EMIs_pending" or response.lower() == "late_fee_percentage" or response.lower() == "principal_amount" or response.lower() == "callback_time" or response.lower() == "emi_amount" or response.lower() == "monthly_emi" or response.lower()== "loan_amount" or \
                response.lower()== "partial_payment_amount" or response.lower()== "ptp_partial_amount" or response.lower()=="total_emi" or response.lower()=="no_of_loans" or response.lower()=="total_amount" or response.lower() == "no_of_emis_pending" or response.lower() == "min_amount_percentage" or response.lower() == "dpd_days" or response.lower() == "interest_rate" or response.lower()=="time_span" or response.lower()=="upside_percentage" or response.lower() == "loan_tenure" or response.lower() == "emi_period":
                eng_num = convert_numbers(entities[response],language)
                if eng_num+".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/number/"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/number/{eng_num}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/number/{eng_num}.wav")
                else:
                    _ = eval(audio_server)(language=language,text=eng_num,fileName=eng_num,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/number/")
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/number/{eng_num}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/number/{eng_num}.wav")
                sound = final_voice
                final_voice = trim_audio(sound)

            if response.lower() == "due_date" or response.lower() == "loan_start_date" or response.lower() == "loan_end_date" or response.lower() == "given_date" or response.lower() == "ptp_day" or response.lower() == "monthly_emi_date" or \
                response.lower()== "emi_date" or response.lower()== "ptp_date" or response.lower()== "monthly_emi_date" or response.lower() == "day_given":
                value = datetime.datetime.strptime(entities[response], "%d %B %Y").strftime("%d %B")
                if value+".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/date/"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/date/{value}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/date/{value}.wav")
                else:
                    _ = eval(audio_server)(language=language,text =value,fileName=value,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/date/")
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/date/{value}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/date/{value}.wav")
                sound = final_voice
                final_voice = trim_audio(sound)

            if response.lower() == "toll_free_number" or response.lower() == "customer_care_number" or response.lower()== "account_number":
                print("entities",entities)
                value = entities[response]
                toll_audio = toll_process.get_audios(value,audio_server,language)
                if final_voice is None:
                    final_voice = toll_audio 
                else:
                    final_voice += toll_audio
                sound = final_voice
                final_voice = trim_audio(sound)

            if response.lower()=="customer_care_email":
                file_name = entities[response]
                if file_name + ".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/email_generated/"):
                    voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/email_generated/{file_name}.wav")
                else:
                    _ = eval(audio_server)(language=language,text=file_name,fileName=file_name,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/email_generated/")
                    voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/email_generated/{file_name}.wav")
                if final_voice is None:
                    final_voice = voice
                else:
                    final_voice += voice

            if response.lower() == "languages_integrated" or response.lower() == "language_name" or response.lower() == "product_type" or response.lower() == "languages_supported":
                print("coming here")
                temp = entities[response].split(",")
                print(temp)
                for key in temp:
                    language_voice = languages_integrated.get_recorded_voice_for_languages_integrated(key,audio_server,language)
                    if final_voice is None:
                        final_voice = language_voice
                    else:
                        final_voice += language_voice
                    sound = final_voice
                    final_voice = trim_audio(sound)
            
            if response.lower()=="client_name" or response.lower()=="agent_name":
                if entities[response] + ".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/client_agent/"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/client_agent/{entities[response]}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/client_agent/{entities[response]}.wav")
                else:
                    _ = eval(audio_server)(language=language,text=entities[response],fileName=entities[response],path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/client_agent/")
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/client_agent/{entities[response]}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/client_agent/{entities[response]}.wav")
                sound = final_voice
                final_voice = trim_audio(sound)
        else:
            count +=1
            if len(response.strip())>0 and response.strip()!="." and response.strip()!="?" and response.strip()!=",":
                if audio_id+"_"+str(count)+".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/Entity_Down/"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Entity_Down/{audio_id}_{str(count)}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Entity_Down/{audio_id}_{str(count)}.wav")
                    # sound = final_voice
                    # final_voice = trim_audio(sound)
                else:
                    returnval = eval(audio_server)(language=language,text = response,fileName=f"{audio_id}_{str(count)}",path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/Entity_Down/")
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Entity_Down/{audio_id}_{str(count)}.wav")
                    else:
                        final_voice += AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Entity_Down/{audio_id}_{str(count)}.wav")
                    # sound = final_voice
                    # final_voice = trim_audio(sound)
    return final_voice



def classify_static_dynamic_template(message, utterance_name,audio_server,language):
    language_respones_mapping = {
        "english":{
            "tts response":"English TTS",
            "audio_id":"English_Audio_ID",
            },
        "hindi":{
            "tts response":"Hindi TTS",
            "audio_id":"Hindi_Audio_ID",
            }
        }
    for item in data:
        if item['Response_ID'] == utterance_name:
            if item[language_respones_mapping[language]["tts response"]]!="":
                utterance=item[language_respones_mapping[language]["tts response"]]
                audio_id = item[language_respones_mapping[language]["audio_id"]]
            if '{' in utterance and '}' in utterance:
                if '{customer_name}' in utterance:
                    return generate_tts_files_customer(utterance,message,utterance_name,audio_id,audio_server,language)
                else:
                    return generate_tts_files_dynamic(utterance,message,audio_id,utterance_name,audio_server,language)
            else:
                return generate_tts_files_static(message,audio_id,audio_server,language)