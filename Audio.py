import sounddevice as sd
from scipy.io import wavfile

fs = 16000

def recording(sec, path):
    print(f'Audio.recording:: Start recording, sec : {sec}, path : {path}')
    recording = sd.rec(int(sec * fs), samplerate=fs, channels=1)
    sd.wait()  # 녹음 완료까지 대기

    wavfile.write(path, fs, recording)
    print('Audio.recording:: end recording ')

def getAudioDetail(path):
    try:
        fs, length = wavfile.read(path)
        return fs, len(length) / fs
    except:
        return '-', '-'



if __name__ == '__main__':
    fs, length = getAudioDetail()
    print(f'{fs} {length}')