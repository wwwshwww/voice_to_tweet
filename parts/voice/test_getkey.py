import sys
import time
import termios

# 標準入力のファイルディスクリプタを取得
fd = sys.stdin.fileno()

# fdの端末属性をゲットする
# oldとnewには同じものが入る。
# newに変更を加えて、適応する
# oldは、後で元に戻すため
old = termios.tcgetattr(fd)
new = termios.tcgetattr(fd)

# new[3]はlflags
# ICANON(カノニカルモードのフラグ)を外す
new[3] &= ~termios.ICANON
# ECHO(入力された文字を表示するか否かのフラグ)を外す
new[3] &= ~termios.ECHO

space_started = False
space_stopped = True

ch = ""

def check_first_press():
    try:
        print("<<Voice To Tweet>> Press SPACE to start recoding")
        # 書き換えたnewをfdに適応する
        termios.tcsetattr(fd, termios.TCSANOW, new)
        # キーボードから入力を受ける。
        # lfalgsが書き換えられているので、エンターを押さなくても次に進む。echoもしない
        ch = sys.stdin.read(1)

    finally:
        # fdの属性を元に戻す
        # 具体的にはICANONとECHOが元に戻る
        termios.tcsetattr(fd, termios.TCSANOW, old)

while True:
    check_first_press()
    if(ch == " "):
        time.sleep(1)
        print("Yeah space!")
    else:
        print("Don't press spacekey!!")
