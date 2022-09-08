import json
from datetime import datetime
from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import random
import time
import os
from kafka import KafkaProducer
from datetime import datetime
from itertools import count

counter = count(1)
now = datetime.now()
output_filename = 'C:\\sts\\raw_gs_data\\json_data.json'

def serialiser(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['10.1.1.191:9094'], value_serializer=serialiser)

def get_last_entry(filename):
    with open(filename,'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data, record_path =['stickReadings'])
    df = df.loc[df['waypoint'].idxmax()]
    df = pd.DataFrame(df).transpose()
    return(df)

def gen_stick_reading():
    return {
        "going": "HEAVY"
        , "index_value": random.uniform(0, 10)
        , "penetrate": random.uniform(0, 10)
        , "shear": random.uniform(0, 10)
        , "waypoint": next(counter)
    }

def write_transaction(cabin_name, the_list) -> dict:
    now = datetime.now()
    y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
    return {
        "cabin_name":cabin_name,
        "time_generated":str(now),
        "y_m_d_h_m_s":y_m_d_h_m_s,
        "stickReadings":the_list
    }

def read_transaction(cabin_name, file_name) -> dict:
    now = datetime.now()
    y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
    df = get_last_entry(file_name)
    return {
        "cabin_name":cabin_name,
        "time_generated":str(now),
        "y_m_d_h_m_s":y_m_d_h_m_s,
        "going": df.iloc[0]['going'],
        "index_value": float(df.iloc[-1]['index_value']),
        "penetrate": float(df.iloc[-1]['penetrate']),
        "shear": float(df.iloc[-1]['shear']),
        "waypoint": int(df.iloc[-1]['waypoint'])
    }


outer_list = []
while True:
    i = 0
    old_size = os.path.getsize(output_filename)
    for i in range(1):
        data = gen_stick_reading()
        outer_list.append(data)
        print(len(outer_list))
    with open(output_filename, 'w') as f:
        json.dump(write_transaction("centre", outer_list), f)
    new_size = os.path.getsize(output_filename)
    if(old_size != new_size):
        transaction = read_transaction("centre", output_filename)
        producer.send('data_transfer', transaction)
        print(transaction)
    time.sleep(1)
