from subprocess import Popen, PIPE, run
import os
import re

if __name__ == '__main__':
    wininfo = Popen("xwininfo", stdout = PIPE)
    win_num = wininfo.communicate()[0].decode('utf-8').split('\n')[5]
    win_num = re.search(r"0x\d+", win_num).group()

    KEY = "Control_L"
    xev = os.system("xev -id " + win_num + " | grep " + KEY)
