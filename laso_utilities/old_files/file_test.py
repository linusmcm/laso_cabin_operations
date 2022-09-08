import os
import json
from datetime import datetime

filename = 'C:\\sts\\raw_gs_data\\postData.json'

def generate_transaction(cabin_id, filename) -> dict:
    now = datetime.now()
    #h_m_s = "%s%s%s" % (now.hour, now.minute, now.microsecond)
    h_m_s = now.strftime("%H%M%S%f")
    y_m_d = now.strftime("%Y%m%d")
    with open(filename, 'r') as f:
        data = json.load(f)
    return {
        'cabin_id': cabin_id,
        'time_stamp': str(now),
        'y_m_d': y_m_d,
        'h_m_s': h_m_s,
        'message': str(data['stickReadings']).replace('index', 'index_value').replace('\\\\', '\\')
    }

print(generate_transaction("centre", filename))


# old_path = os.fspath(filename)
# old_mtime = os.path.getmtime(filename)
# while True:
#     new_mtime = os.path.getmtime(filename)
#     if(old_mtime != new_mtime):
#         print(generate_transaction(filename))
#     else:
#         print("altered")


