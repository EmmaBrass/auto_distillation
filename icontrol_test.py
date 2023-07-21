import pywinauto
from pywinauto import findwindows
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import time
import pyautogui

path = r'C:\Program Files\METTLER TOLEDO\iControl 6.1\iControl64.exe'

app = Application(backend="uia").connect(path=path)

for x in pyautogui.getAllWindows():  
            if 'iControl 6.1' in x.title:
                window_name = x.title
print(f"current window name is:", window_name)
current_window = app.window(best_match=window_name)
current_window.set_focus()

current_window['Dose at Rate'].click_input(button='left', double=True)


volume = 54
# current_window.AmountComboBox.click()
current_window.AmountComboBox.click_input(button='left', double=False)
send_keys('56 ml')
duration_min = round(volume/50,1)
current_window.DurationEdit.set_text(f'{duration_min} min')