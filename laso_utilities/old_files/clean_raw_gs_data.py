import pandas as pd
import json
import glob
import os
from datetime import datetime

# search all files inside a specific folder
# *.* means file name with any extension
dir_path = r'C:\sts\raw_gs_data\*.*'
file_list = glob.glob(dir_path)

# import os
# res = os.listdir(dir_path)
for file_name in file_list:
    print(file_name)
    
    #base = os.path.basename(file_name)
    #date_stamp = os.path.splitext(base)[0]
    #date_stamp = datetime.strptime(date_stamp, '%Y%m%d%H%M%S%f')
    with open(file_name) as fh:
        while True:
            line = fh.readline()
            print(line)
            if line.startswith('JSON'):
                break
        line = line.replace('JSON Output: ','')
    stud_obj = json.loads(line)
    #print(json.dump(date_stamp))
    print(stud_obj)
