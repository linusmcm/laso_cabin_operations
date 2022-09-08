import os
import sys
import win32com.shell.shell as shell
ASADMIN = 'asadmin'

the_path = os.path.join("C:", "\Program Files (x86)", "Turf Trax", "Going Stick")
print(f'{the_path}\GoingStickXP.exe')

if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(f'{the_path}\GoingStickXP.exe')
    print("script: ", script)
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    print("params: ", params)
    print(shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params))
    sys.exit(0)
