import os
import subprocess
from pathlib import Path

import os
import subprocess
import soundfile as sf
import pyloudnorm as pyln
import sys
import time

rnn = "/Users/debadityamandal/Desktop/rnnoise/examples/rnnoise_demo"

root_path = "/home/azureuser/Fullerton_bot/fullerton_tts/welcom/"
out_path = "/home/azureuser/Fullerton_bot/fullerton_tts/Fullerton_Audios/Hindi_Entity_Down_new/"
# print(os.walk(root_path))
dirs = []


def process_audio(file_name, out_file_name):
    filepath = file_name
    target_filepath = out_file_name
    print(os.path.isfile(target_filepath))
    # if not os.path.isfile(target_filepath):
    #     return

    # Stereo to Mono; upsample to 48000Hz
    subprocess.run(["sox", filepath, "48k.wav", "remix", "-", "rate", "48000"])
    subprocess.run(["sox", "48k.wav", "-c", "1", "-r", "48000", "-b", "16", "-e", "signed-integer", "-t", "raw",
                    "temp.raw"])  # convert wav to raw
    t = time.time()
    subprocess.run([rnn, "temp.raw", "rnn.raw"])  # apply rnnoise
    subprocess.run(["sox", "-r", "48k", "-b", "16", "-e", "signed-integer", "rnn.raw", "-t", "wav",
                    "rnn.wav"])  # convert raw back to wav
    print(time.time() - t)
    subprocess.run(["sox", "rnn.wav", str(target_filepath), "remix", "-", "highpass", "100", "lowpass", "7000", "rate",
                    "8000"])  # apply high/low pass filter and change sr to 22050Hz

    data, rate = sf.read(target_filepath)

    # peak normalize audio to -1 dB
    peak_normalized_audio = pyln.normalize.peak(data, -1.0)

    # measure the loudness first
    meter = pyln.Meter(rate)  # create BS.1770 meter
    loudness = meter.integrated_loudness(data)

    # loudness normalize audio to -25 dB LUFS
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -25.0)

    sf.write(target_filepath, data=loudness_normalized_audio, samplerate=8000)


for root, dirs, files in os.walk(root_path):
    if root != ".DS_Store" or dirs != ".DS_Store":
        print(root)
        path = root.replace(root_path, out_path)
        print(path, os.path.isdir(path))
        if not os.path.isdir(path):
            os.mkdir(path)

        for f in files:
            if f != ".DS_Store" and f.endswith(".wav"):
                source_path = root + "/" + f
                dest_path = path + "/" + f
                print(source_path, dest_path)
                if not os.path.isfile(dest_path):
                    try:
                        process_audio(source_path, dest_path)
                    except Exception as e:
                        print("------------------------------------------------------",e)

