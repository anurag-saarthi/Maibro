import SaO_oneBot_audio_generator.automatic_tts_generate_new as audio_generator
from fastapi import FastAPI,Request,Response
from fastapi.encoders import jsonable_encoder
import uvicorn
import io
import os 
import json
import re
import hashlib
from re import template
import time
import datetime
app = FastAPI()

@app.get("/wav")
async def audio(message:str,language:str,template_name:str,audio_server:str):
    async def generate(template_name=None, message=None, language=None,session_id=None,audio_server=None): # ,tone=None
        data = audio_generator.classify_static_dynamic_template(message, template_name,audio_server,language)
        buf = io.BytesIO()
        data.export(buf, bitrate="128k", format="wav") 
        return buf.getvalue()
    start_time=datetime.datetime.now()
    audio = await generate(message=message, template_name=template_name,language=language,audio_server=audio_server)
    hash_object = hashlib.md5(message.encode('utf-8'))
    file_name = str(hash_object.hexdigest())              
    response = Response(audio)
    response.headers['media_type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename={}.wav'.format(file_name)
    end_time=datetime.datetime.now()
    with open("log.txt","a") as f:
        f.write(f"message -----> {message} start_time>>>{start_time} end_time >>>>{end_time} delay >>> {end_time-start_time}\n")
    return response

if __name__ == "__main__":
    uvicorn.run("streaming_api:app",port = 7020,host="0.0.0.0",workers=1)

# sudo kill -9 $(sudo lsof -t -i:7020)