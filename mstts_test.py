import datetime
from google.cloud import texttospeech
import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_PATH_1 = os.path.dirname(os.path.abspath(__file__))
import azure.cognitiveservices.speech as speechsdk
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
language = "hindi"
response = "हीरो हाउसिंग फाइनेंस परिवार में आपका स्वागत है! हमारे साथ एक"
audio_id = "HH_WC_MT_HF74"
count = 1
audio_server = "mstts"
_=mstts(language=language,text = response,fileName=f"{audio_id}_{str(count)}",path_to_write=f"/home/ubuntu/Hero/")