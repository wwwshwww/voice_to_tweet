import fcntl
import termios
import sys
import os
import pyaudio
import wave

SWITCH_KEY = 10 # ASCIIコード（Enter）

WAVE_OUTPUT_FILENAME = "sample.wav" #音声を保存するファイル名
iDeviceIndex = 0 #録音デバイスのインデックス番号

FORMAT = pyaudio.paInt16 #音声のフォーマット
CHANNELS = 1             #モノラル
RATE = 44100             #サンプルレート
CHUNK = 2**11            #データ点数

audio = pyaudio.PyAudio() #pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
        frames_per_buffer=CHUNK)
frames = []

def setup_recording():
    global frames
    global audio
    global stream
    frames = []
    audio = pyaudio.PyAudio() #pyaudio.PyAudio()
 
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex,
            frames_per_buffer=CHUNK)

def record():
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)

def record_complete():
    close_all()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
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
    fno = sys.stdin.fileno()

    #stdinの端末属性を取得
    attr_old = termios.tcgetattr(fno)

    # stdinのエコー無効、カノニカルモード無効
    attr = termios.tcgetattr(fno)
    attr[3] = attr[3] & ~termios.ECHO & ~termios.ICANON
    termios.tcsetattr(fno, termios.TCSADRAIN, attr)

    # stdinをNONBLOCKに設定
    fcntl_old = fcntl.fcntl(fno, fcntl.F_GETFL)
    fcntl.fcntl(fno, fcntl.F_SETFL, fcntl_old | os.O_NONBLOCK)

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
        fcntl.fcntl(fno, fcntl.F_SETFL, fcntl_old)
        termios.tcsetattr(fno, termios.TCSANOW, attr_old)

    return chr

def check_start():
    while 1:
        key = getkey()
        if key == SWITCH_KEY:
            setup_recording()
            print("recoding now...")
            break

def check_stop():
    while 1:
        record()
        key = getkey()
        if key == SWITCH_KEY:
            record_complete()
            print("Successful recoding!")
            break

if __name__ == "__main__":
    while 1:  
        print("<<Voice To Tweet>>\nPress ENTER to start recoding")
        check_start()
        check_stop()
        print("Bye")
