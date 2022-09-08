from kafka import KafkaProducer
from datetime import datetime
from itertools import count
import time
import json
import os

ONE_METRE = 0.000009000009
START_LAT= -33.910233732832864
START_LON=  151.22707964514063

counter = count(1)

def generate_cabin_name():
    user_name = os.getlogin()
    if (user_name == "center"):
            user_name = "centre"
    return(user_name)

def serialiser(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['10.1.1.191:9094'], value_serializer=serialiser)

def gps_transaction(cabin_name, lat, lon):
    now = datetime.now()
    y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
    return {
        "cabin_name":cabin_name,
        "time_generated":str(now),
        "y_m_d_h_m_s":y_m_d_h_m_s,
        "lat":lat,
        "lon":lon,
    }


LEFT = 1
CENTRE = 2
RIGHT = 3
def main():
    while True:
        lon = START_LON + (ONE_METRE * 10) * next(counter)
        # for l in range(3):
        #     lat = START_LAT + (ONE_METRE * 5 * l * LEFT)
        #     #transaction = gps_transaction(generate_cabin_name(), lat, lon)
        #     #producer.send(f'gps_reading_{ generate_cabin_name() }', transaction)
        #     transaction = gps_transaction('left', lat, lon)
        #     producer.send(f'gps_reading_left', transaction)
        #     print(transaction)
        #     time.sleep(5)
        for c in range(45):
            lat = START_LAT + (ONE_METRE * 5 * c)
            #lat = START_LAT + (ONE_METRE * 5 * c * CENTRE) #use for all three
            #transaction = gps_transaction(generate_cabin_name(), lat, lon)
            #producer.send(f'gps_reading_{ generate_cabin_name() }', transaction)
            transaction = gps_transaction('centre', lat, lon)
            producer.send(f'gps_reading_centre', transaction)
            print(transaction)
            time.sleep(1)
        # for r in range(3):
        #     lat = START_LAT + (ONE_METRE * 5 * r * RIGHT)
        #     #transaction = gps_transaction(generate_cabin_name(), lat, lon)
        #     #producer.send(f'gps_reading_{ generate_cabin_name() }', transaction)
        #     transaction = gps_transaction('right', lat, lon)
        #     producer.send(f'gps_reading_right', transaction)
        #     print(transaction)
        #     time.sleep(5)
        time.sleep(10)


if __name__ == "__main__":
    main()
