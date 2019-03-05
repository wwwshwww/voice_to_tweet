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

KEY, URL, LANG = getter.getSpeechToTextAPIConsumer()
CONT_TYPE = "audio/wav"

RECORD_LIMIT = 20
RECORD_LIMIT_GLOBAL = RATE / CHUNK * RECORD_LIMIT

THRESHOULD = 0.015 # 録音開始閾値
SILENT_LIMIT = 1.0 # 無音時間
SILENT_LIMIT_GLOBAL = RATE / CHUNK * SILENT_LIMIT

now_record = 0
now_silent = 0

t_api_key, t_api_secret, _ = getter.getTwitterAPIConsumer()
token, token_secret, _, _ = getter.getTwitterAccess()

audio = pyaudio.PyAudio() #pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        frames_per_buffer=CHUNK)
frames = []

# 取得したキーとアクセストークンを設定する
auth = twitter.OAuth(consumer_key=t_api_key,
                     consumer_secret=t_api_secret,
                     token=token,
                     token_secret=token_secret)

t = twitter.Twitter(auth=auth)

def sendToSTT():
    audio_file = open("sample.wav", "rb")
    stt = SpeechToTextV1(iam_apikey=KEY, url=URL)
    result = stt.recognize(audio=audio_file,
            content_type=CONT_TYPE, model=LANG)
    result_dict = result.get_result()
    text = ""
    for i in range(len(result_dict["results"])):
        text += result_dict["results"][i]["alternatives"][0]["transcript"]
    return text

def setupRecording():
    global frames, audio, stream, now_record, now_silent
    frames = []
    audio = pyaudio.PyAudio() # pyaudio.PyAudio()
 
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            frames_per_buffer=CHUNK)

    now_record = 0
    now_silent = 0

def record(data):
    global now_record
    frames.append(data)
    now_record += 1

def getData():
    return stream.read(CHUNK, exception_on_overflow=False)

def recordComplete():
    closeAll()
    waveFile = wave.open(WAVE_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def closeAll():
    stream.stop_stream()
    stream.close()
    audio.terminate()

def checkLevel(s):
    level = np.frombuffer(s, dtype='int16') / 32768.0
    return level.max() > THRESHOULD

def checkStart():
    while 1:
        data = getData()
        if checkLevel(data):
            print("recording now...")
            record(data)
            break

def checkStop():
    global now_silent, now_record
    while 1:
        data = getData()
        if checkLevel(data):
            now_silent = 0
        else:
            now_silent += 1
            if now_silent > SILENT_LIMIT_GLOBAL:
                recordComplete()
                print("Successful recording!")
                break
        record(data)
        if now_record > RECORD_LIMIT_GLOBAL:
            recordComplete()
            print("Stop and Success recording because spent 30 seconds.")
            break

def tweet(tweet_text):
    t.statuses.update(status=tweet_text)

if __name__ == "__main__":
    while 1:  
        print("\n<<=========== Voice To Tweet -Auto mode- ===========>>\n")
        setupRecording()
        checkStart()
        checkStop()
        print("converting...")
        te = sendToSTT()
        print("\""+te+"\"")
        if len(te) > 0:
            tweet(tweet_text=te)
            print("Tweeted!")
        else:
            print("Cancelled because it's empty text.\n")
        os.remove(WAVE_FILENAME)