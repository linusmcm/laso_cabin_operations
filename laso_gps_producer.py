from kafka import KafkaProducer
import serial

from laso_utilities.utilities import (
    hdop_dilution_interpretation
    , generate_cabin_name
    , laso_serializer
    , gps_signal_fix
    , north_south
    , decimal_degrees
    , degrees_minutes
    , generate_gps_message
)

producer = KafkaProducer(bootstrap_servers=['10.1.1.191:9094'], value_serializer=laso_serializer) #TODO - windows env variable for IP address
ser = serial.Serial('COM4', 9600, timeout=1.0)

while True:
    read_bytes = ser.readline()
    decoded_bytes = read_bytes.decode("utf-8")
    data_list = decoded_bytes.split(",")
    if(data_list[0] == '$GNGGA'):
        lat = decimal_degrees(*degrees_minutes(data_list[2]))
        n_s = data_list[3]
        lon = north_south(data_list[3], decimal_degrees(*degrees_minutes(data_list[4])))
        e_w = data_list[5]
        gps_fix = gps_signal_fix(data_list[6])
        no_satellites = data_list[7]
        horizontal_dilution = data_list[8]
        hdi = hdop_dilution_interpretation(data_list[8])
        altitude = data_list[9]
        station_id = data_list[14]
        base_list = [lat, n_s, lon, e_w, gps_fix, no_satellites, horizontal_dilution, hdi, altitude, station_id]
        gps_message = generate_gps_message(generate_cabin_name(), base_list)
        print(gps_message)
        producer.send(f'gps_data_{ generate_cabin_name() }', gps_message)
