import pyautogui

for x in pyautogui.getAllWindows():  
    print(x.title)