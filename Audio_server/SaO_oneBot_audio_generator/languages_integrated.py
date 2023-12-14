import datetime
import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This is your Project Root
from SaO_oneBot_audio_generator.gtts import synthesize_text as google_tts
from SaO_oneBot_audio_generator.gtts import mstts as mstts
from SaO_oneBot_audio_generator.gtts import saarthi_tts as saarthi_tts
sys.path.append(CURRENT_PATH)
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment

def save_audios_mstts(language,text,fileName,path_to_write):
    speech_config = speechsdk.SpeechConfig(subscription="5ee9cd2e2bbd400ea0912c59598cfe42", region="centralindia")
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    english_TTS = "en-IN-NeerjaNeural"
    save_path = path_to_write+fileName+".wav"
    print(save_path)
    speech_config.speech_synthesis_voice_name=english_TTS
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(speech_synthesis_result)
    stream.save_to_wav_file_async(save_path)
    return "File saved sucessfully"

def get_recorded_voice_for_languages_integrated(company_address,audio_server,language):
    final = None
    if str(company_address)+".wav" in  os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/Languages/"):
        final = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Languages/{company_address}.wav")
    else:
        _ = eval(audio_server)(language=language,text=company_address,fileName=company_address,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/Languages/")
        final = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/Languages/{company_address}.wav")
    return final