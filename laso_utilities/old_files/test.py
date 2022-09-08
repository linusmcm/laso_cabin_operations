from subprocess import check_output
import subprocess
import os
import sys

the_path = os.path.join("C:", "\Program Files (x86)", "Turf Trax", "Going Stick")
print(f'{the_path}\GoingStickXP.exe')
full_path = f'{the_path}\\GoingStickXP.exe'
print("full_path: ", full_path)
#print(check_output("dir C:", shell=True).decode())



#subprocess.call(['C:\Program Files\Mozilla Firefox\\firefox.exe'])
#subprocess.Popen(f'{the_path}\GoingStickXP.exe')
#print(subprocess.Popen(f'{the_path}\GoingStickXP.exe'))



os.system(f'start {full_path}') 
