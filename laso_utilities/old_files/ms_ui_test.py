import os
import pywinauto
import sys
#from pywinauto import Desktop, Application
from pywinauto.application import Application
from pywinauto.uia_defines import get_elem_interface
from pywinauto.uia_defines import IUIA
from pywinauto.controls.uia_controls import ButtonWrapper
from pywinauto.timings import Timings

Timings.window_find_timeout = 10

the_path = os.path.join("C:", "\Program Files (x86)", "Turf Trax", "Going Stick")
full_path = f'{the_path}\\GoingStickXP.exe'
print("full_path: ", full_path)

app = Application(backend="uia").connect(path = full_path)
print("app: ", app)
start_download = IUIA().build_condition(process=7684, class_name="WindowsForms10.BUTTON.app.0.141b42a_r6_ad1", control_type='Pane')
print("start_download: ", start_download)
print(app.start_download)



#common_files = app.ProgramFiles.ItemsView.get_item('Start Download')
#common_files.click()
#app.ContextMenu.Properties.invoke()
