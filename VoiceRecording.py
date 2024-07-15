import sounddevice as sd
from scipy.io.wavfile import write
import os

fs = 16000

def getRecordpath():
    path = os.getcwd() + '\\Audio_waterMark_simulator\\Sound\\sound.wav'
    return path

def recording(sec):
    print("Start recording")
    recording = sd.rec(int(sec * fs), samplerate=fs, channels=1)
    sd.wait()  # 녹음 완료까지 대기
    print("recording ended")

    file = getRecordpath()
    write(file, fs, recording)
    print(f"file saved : {file}")

if __name__ == '__main__':
    recording(3)