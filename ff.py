import os
from datetime import datetime

if __name__ == '__main__smt':
    current_now = datetime.now()
    begin_time_utc_string = current_now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    print(str(begin_time_utc_string))
    isSmt = False
    if isSmt:
        os.system("ffmpeg1000/ffmpeg -re -stream_loop -1 -i /home/mahongyin/media/videos/OlyL20210414183400000CH00000001PGMhd.ts -begintime {0} -c copy -smtbitrate 4800 -f mpu smt://182.182.0.81:16666".format(str(begin_time_utc_string)))
    else:
        os.system("ffmpeg1000/ffmpeg  -re -stream_loop -1 -i /home/mahongyin/media/videos/OlyL20210414183400000CH00000001PGMhd.ts -c copy -f mpegts udp://182.182.0.81:16666")
# 金老师的ffmpeg 输出smt 实际udp    10.3.3.100代理？
# ./ffmpeg -i "udp://10.3.3.255:12301?overrun_nonfatal=1&fifo_size=5000000" -begintime 2022-07-15T10:48:40.462836 -c copy -smtbitrate 45000 -f mpu smt://10.3.3.100:61234 -port 12345
# ./ffmpeg -re -stream_loop -1 -i /home/mahongyin/media/videos/OlyL20210414183400000CH00000001PGMhd.ts -begintime 2022-07-15T10:48:40.462836 -c copy -smtbitrate 4800 -f mpu smt://10.3.3.100:61234 -port 12345
# 中转到组播
# ./TSReplay -i udp://127.0.0.1:61234 -o udp://239.3.3.3:21000 -d 1 -p 120
#
# smt_ijkplayer  smt://239.3.3.3:21000
if __name__ == '__main__':
    current_now = datetime.now()
    begin_time_utc_string = current_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    print("打印smt需要的 begintime "+str(begin_time_utc_string))
    os.system('adb {0}'.format("--version"))