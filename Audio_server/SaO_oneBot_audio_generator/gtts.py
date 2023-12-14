import datetime
from google.cloud import texttospeech
import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_PATH_1 = os.path.dirname(os.path.abspath(__file__))
import azure.cognitiveservices.speech as speechsdk
def synthesize_text(language,text,fileName,path_to_write):
    language_mapping = {
        "english":{
            "language_code":"en-IN",
            "name":"en-IN-Standard-A"
        },
        "hindi":{
            "language_code":"hi-IN",
            "name":"hi-IN-Standard-A"
        }

    }
    CURRENT_PATH = os.path.dirname((__file__))
    """Synthesizes speech from the input string of text."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='GoogleTTSCredential.json'
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_mapping[language]["language_code"],
        name=language_mapping[language]["name"],
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000
    )
    response = client.synthesize_speech(
        request={"input": input_text, 
                 "voice": voice, 
                 "audio_config": audio_config}
    )
    with open(path_to_write + fileName + ".wav", "wb") as out:
        out.write(response.audio_content)
    return "Successful"


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

def saarthi_tts(language,text,fileName,path_to_write):
    pass
