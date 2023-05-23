import pyautogui
import time
from selenium.webdriver.common.keys import Keys
import os
# os.system("C:\\Windows\\notepad.exe")
time.sleep(5)
pyautogui.write("TEST START")
time.sleep(5)

a = 0
while a <= 40:
    tm = time.localtime()
    # chr1 = Keys.LEFT_CONTROL
    # chr1 = time.strftime('%Y-%m-%d %I:%M %p' + '      ', tm)
    # chr1 = str(cnt +  tmTEST START.tm_year + tm.tm_mon + tm.tm_mday + tm.tm_hour + tm.tm_min)
    chr1 = str(a) + " "
    pyautogui.write(chr1, interval= 1)
    time.sleep(300)

    a += 1