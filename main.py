import playsound3

def main():
    music = './music/一班名字之歌-四十九颗星.mp3'
    sound = playsound3.playsound(music, block=False)
    print('开始播放...')
    while True:
        ans = input('输入命令（S:停止, 非S:继续）：')
        if ans == 'S' or ans == 'Stop':
            sound.stop()
            break

if __name__ == "__main__":
    main()
