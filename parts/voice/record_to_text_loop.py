import fcntl
import termios
import sys
import os
import pyaudio
import wave
from watson_developer_cloud import SpeechToTextV1
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tool import getter

SWITCH_KEY = 10 # ASCIIコード（Enter）
FNO = sys.stdin.fileno()
ATTR_OLD = termios.tcgetattr(FNO) # stdinの端末属性を取得
FCNTL_OLD = fcntl.fcntl(FNO, fcntl.F_GETFL)

WAVE_FILENAME = "sample.wav" # 音声を保存するファイル名
iDeviceIndex = 0 # 録音デバイスのインデックス番号

FORMAT = pyaudio.paInt16 # 音声のフォーマット
CHANNELS = 1             # モノラル
RATE = 44100             # サンプルレート
CHUNK = 2**11            # データ点数

USER, PSWD, LANG = getter.getSpeechToTextAPIConsumer()

CONT_TYPE = "audio/wav"
# LANG = "en-US_BroadbandModel"

audio = pyaudio.PyAudio() #pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex, 
        frames_per_buffer=CHUNK)
frames = []

def send_to_watson():
    audio_file = open("sample.wav", "rb")
    stt = SpeechToTextV1(username=USER, password=PSWD)
    result = stt.recognize(audio=audio_file,
            content_type=CONT_TYPE, model=LANG)

    text = ""
    result_dict = result.get_result()
    for i in range(len(result_dict['results'])):
        text += result_dict['results'][i]['alternatives'][0]['transcript']

    return text

def setup_recording():
    global frames
    global audio
    global stream
    frames = []
    audio = pyaudio.PyAudio() # pyaudio.PyAudio()
 
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex,
            frames_per_buffer=CHUNK)

def record():
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)

def record_complete():
    close_all()
    waveFile = wave.open(WAVE_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def close_all():
    stream.stop_stream()
    stream.close()
    audio.terminate()

def getkey():
    # stdinのエコー無効、カノニカルモード無効
    attr = termios.tcgetattr(FNO)
    attr[3] = attr[3] & ~termios.ECHO & ~termios.ICANON
    termios.tcsetattr(FNO, termios.TCSADRAIN, attr)

    # stdinをNONBLOCKに設定
    fcntl.fcntl(FNO, fcntl.F_SETFL, FCNTL_OLD | os.O_NONBLOCK)

    chr = 0

    try:
        # キーを取得
        c = sys.stdin.read(1)
        if len(c):
            while len(c):
                chr = (chr << 8) + ord(c)
                c = sys.stdin.read(1)
    finally:
        # stdinを元に戻す
        fcntl.fcntl(FNO, fcntl.F_SETFL, FCNTL_OLD)
        termios.tcsetattr(FNO, termios.TCSANOW, ATTR_OLD)

    return chr

def check_start():
    try:   
        while 1:
            key = getkey()
            if key == SWITCH_KEY:
                setup_recording()
                print("recording now...")
                break
    finally:
        # stdinを元に戻す
        fcntl.fcntl(FNO, fcntl.F_SETFL, FCNTL_OLD)
        termios.tcsetattr(FNO, termios.TCSANOW, ATTR_OLD)

def check_stop():
    while 1:
        record()
        key = getkey()
        if key == SWITCH_KEY:
            record_complete()
            print("Successful recording!")
            break

if __name__ == "__main__":
    while True:  
        print("\n<<=========== Voice To Tweet ===========>>\n")
        print("Press ENTER to start or stop recording.\n"+
            "Do you want to exit? Then type Ctrl+C!")
        check_start()
        check_stop()
        print("converting...")
        print("\n\""+send_to_watson()+"\"")
        os.remove(WAVE_FILENAME)
