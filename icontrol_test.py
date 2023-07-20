import pywinauto
import time
from pywinauto.keyboard import send_keys

time.sleep(5)
print("attempting live stirrer speed setting")
pywinauto.mouse.click(button='left', coords= (930, 375))
send_keys('222')
send_keys('{ENTER}')