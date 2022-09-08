import os
import time
from pywinauto.application import Application
from kafka import KafkaProducer
from laso_utilities.utilities import (
    generate_transaction
    , generate_log_message
    , generate_cabin_name
    , laso_serializer)

#test file
filename = 'C:\\sts\\raw_gs_data\\json_data.json'
# real generated file
#filename = 'C:\\sts\\raw_gs_data\\postData.json'
producer = KafkaProducer(bootstrap_servers=['10.1.1.191:9094'], value_serializer=laso_serializer) #TODO - windows env variable for IP address

def main():
    application_path = os.path.join("C:", "\Program Files (x86)", "Turf Trax", "Going Stick")
    full_path = f'{application_path}\\GoingStickXP.exe'
    while True:
        try:
            try:
                app = Application(backend="uia").connect(path = full_path)
                message = f'Application Running - CABIN: { generate_cabin_name() }'
                log_message = generate_log_message(generate_cabin_name(), "SUCCESS", "application", message)
                producer.send(f'log_tranfer_{ generate_cabin_name() }', log_message)
                print(log_message)
            except Exception as e1:
                message = f'Application Load Issue  - CABIN: { generate_cabin_name() }'
                log_message = generate_log_message(generate_cabin_name(), "ERROR", "application", message)
                producer.send(f'log_tranfer_{ generate_cabin_name() }', log_message)
                print(log_message)
                time.sleep(5)
                continue
            try:
                old_size = os.path.getsize(filename)
                dlg = app.window(title_re="TurfTrax 1.11.5", class_name="WindowsForms10.Window.8.app.0.141b42a_r6_ad1")
                app.dlg["Start Download"].click()
                message = f'Button Activated -  { generate_cabin_name() }'
                log_message = generate_log_message(generate_cabin_name(), "SUCCESS", "button", message)
                producer.send(f'log_tranfer_{ generate_cabin_name() }', log_message)
                print(log_message)
                time.sleep(10)
                new_size = os.path.getsize(filename)
                if(old_size != new_size):
                    transaction = generate_transaction(generate_cabin_name(), filename)
                    producer.send('data_transfer', transaction)
                    print(transaction)
            except Exception as e2:
                message = f'Button NOT Activated - CABIN: { generate_cabin_name() }'
                log_message = generate_log_message(generate_cabin_name(), "ERROR", "button", message)
                producer.send(f'log_tranfer_{ generate_cabin_name() }', log_message)
                print(log_message)
                time.sleep(1)
                continue
        except Exception as e:
            message = f'Application has NOT started - CABIN: { generate_cabin_name() }'
            log_message = generate_log_message(generate_cabin_name(), "ERROR", "application", message)
            producer.send(f'log_tranfer_{ generate_cabin_name() }', log_message)
            print(log_message)
            continue
        time.sleep(15)

if __name__ == "__main__":
    main()
