import os, sys
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
from fastapi import FastAPI,Request,Response
app = FastAPI()
import azure.cognitiveservices.speech as speechsdk
import uvicorn
import hashlib
import io
from pydub import AudioSegment
def mstts(language,text,fileName,path_to_write):
    language_tts_mapping = {
        "english":"en-IN-NeerjaNeural",
        "hindi":"hi-IN-SwaraNeural"
    }
    speech_config = speechsdk.SpeechConfig(subscription="5ee9cd2e2bbd400ea0912c59598cfe42", region="centralindia")
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    language_tts = language_tts_mapping[language]
    save_path = path_to_write+fileName+".wav"
    speech_config.speech_synthesis_voice_name=language_tts
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(speech_synthesis_result)
    stream.save_to_wav_file_async(save_path)
    return "File saved sucessfully"



@app.get("/mstts_api")
async def audio(message:str,language:str,template_name:str):
    print("<><>",message,language)
    _ = mstts(language=language,text=message,fileName=template_name,path_to_write=f"{CURRENT_PATH}/mstts_audios/")
    final_voice = AudioSegment.from_wav(f"{CURRENT_PATH}/mstts_audios/{template_name}.wav")
    buf = io.BytesIO()
    final_voice.export(buf, bitrate="128k", format="wav") 
    response = Response(buf.getvalue())
    hash_object = hashlib.md5(message.encode('utf-8'))
    file_name = str(hash_object.hexdigest())   
    response.headers['media_type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename={}.wav'.format(template_name)
    return response



if __name__ == "__main__":
    uvicorn.run("mstts_api:app",port = 7030,host="0.0.0.0",workers=1)
