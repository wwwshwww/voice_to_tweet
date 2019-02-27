import sys
import os
import pyaudio
import wave
import numpy as np
from watson_developer_cloud import SpeechToTextV1
import json
import twitter

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parts.tool import getter

WAVE_FILENAME = "sample.wav" # 音声を保存するファイル名
iDeviceIndex = 0 # 録音デバイスのインデックス番号

FORMAT = pyaudio.paInt16 # 音声のフォーマット
CHANNELS = 1             # モノラル
RATE = 44100             # サンプルレート
CHUNK = 2**11            # データ点数

USER, PSWD, LANG = getter.getSpeechToTextAPIConsumer()
CONT_TYPE = "audio/wav"

THRESHOULD = 0.01 # 録音開始閾値
TIME = 1.5 # 無音時間
TIME_GLOBAL = RATE / CHUNK * TIME

now = 0

t_api_key, t_api_secret, _ = getter.getTwitterAPIConsumer()
token, token_secret, _, _ = getter.getTwitterAccess()

audio = pyaudio.PyAudio() #pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex, 
        frames_per_buffer=CHUNK)
frames = []

# 取得したキーとアクセストークンを設定する
auth = twitter.OAuth(consumer_key=t_api_key,
                     consumer_secret=t_api_secret,
                     token=token,
                     token_secret=token_secret)

t = twitter.Twitter(auth=auth)

def send_to_watson():
    audio_file = open("sample.wav", "rb")
    stt = SpeechToTextV1(username=USER, password=PSWD)
    result = stt.recognize(audio=audio_file,
            content_type=CONT_TYPE, model=LANG)
    result_dict = result.get_result()
    text = ""
    for i in range(len(result_dict["results"])):
        text += result_dict["results"][i]["alternatives"][0]["transcript"]
    return text

def setup_recording():
    global frames
    global audio
    global stream
    global now
    frames = []
    audio = pyaudio.PyAudio() # pyaudio.PyAudio()
 
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex,
            frames_per_buffer=CHUNK)

    now = 0

def record(data):
    frames.append(data)

def get_data():
    return stream.read(CHUNK, exception_on_overflow=False)

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

def check_level(s):
    level = np.frombuffer(s, dtype='int16') / 32768.0
    return level.max() > THRESHOULD

def check_start():
    while 1:
        data = get_data()
        if check_level(data):
            print("recording now...")
            record(data)
            break

def check_stop():
    global now
    while 1:
        data = get_data()
        if check_level(data):
            now = 0
        else:
            now += 1
            if now > TIME_GLOBAL:
                record_complete()
                print("Successful recording!")
                break
        record(data)
            

def tweet(tweet_text):
    t.statuses.update(status=tweet_text)

if __name__ == "__main__":
    while 1:  
        print("\n<<=========== Voice To Tweet -Auto mode- ===========>>\n")
        setup_recording()
        check_start()
        check_stop()
        print("converting...")
        te = send_to_watson()
        print("\""+te+"\"")
        if len(te) > 0:
            tweet(tweet_text=te)
            print("Tweeted!")
        else:
            print("Cancelled because it's empty text.\n")
        os.remove(WAVE_FILENAME)