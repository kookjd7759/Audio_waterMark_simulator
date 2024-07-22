import sounddevice as sd
from scipy.io import wavfile
import os

fs = 16000

def recording(sec, path):
    print("Start recording")
    recording = sd.rec(int(sec * fs), samplerate=fs, channels=1)
    sd.wait()  # 녹음 완료까지 대기
    print("recording ended")

    wavfile.write(path, fs, recording)
    print(f"file saved : {path}")

def getAudioDetail(path):
    try:
        fs, length = wavfile.read(path)
        return fs, len(length) / fs
    except:
        return '-', '-'

def isSoundFileEnable(path):
    try:
        wavfile.read(path)
        return True
    except:
        return False



if __name__ == '__main__':
    fs, length = getAudioDetail()
    print(f'{fs} {length}')