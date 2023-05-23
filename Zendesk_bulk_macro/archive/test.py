import pyautogui
import time

i = 1
while i <= 25:
    time.sleep(4)
    locate = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page=' + str(i) + '&per_page=1000'
    pyautogui.write(locate+'\n')
    time.sleep(20)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)
    save_name = 'macro_list_'+ str(i) +'.json'
    pyautogui.write(save_name+'\n')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(2)
    i += 1
