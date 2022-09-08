import pywinauto
import os
import time
import sys
from pywinauto.application import Application
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
date_time = now.strftime("%Y%m%d%H%M%S")
user_name = os.getlogin()

if (user_name == "center"):
        user_name = "centre"

#logging_path = os.path.join("generator_logs", str(year), str(month), str(day))
#os.makedirs(logging_path, exist_ok = True)
#logging.basicConfig(filename=f'{logging_path}\\{date_time}.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8', level=logging.DEBUG)
logging_path = f'smb:\\nifi\sts_{user_name}_logs/automator.log'
logging.basicConfig(filename=logging_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8', level=logging.DEBUG)

def main():
    application_path = os.path.join("C:", "\Program Files (x86)", "Turf Trax", "Going Stick")
    full_path = f'{application_path}\\GoingStickXP.exe'
    try:
        app = Application(backend="uia").connect(path = full_path)
        print("application loaded")
    except Exception as e1:
        logging.error(f'application not open - { e1 }' )
    try:
        dlg = app.window(title_re="TurfTrax 1.11.5", class_name="WindowsForms10.Window.8.app.0.141b42a_r6_ad1")
        app.dlg["Start Download"].click()
        logging.info(f'button activated -  { app.dlg["Start Download"] }')
    except Exception as e2:
        logging.error(f'button not activated - { e2 }')

if __name__ == "__main__":
    main()
