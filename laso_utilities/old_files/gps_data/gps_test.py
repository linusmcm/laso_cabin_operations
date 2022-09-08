import io
import pynmea2
import serial
import pandas as pd
import time
from datetime import datetime

def degrees_minutes(x):
    degrees = float(x) // 100
    minutes = float(x) - 100 * degrees
    return(float(degrees), float(minutes))

def decimal_degrees(degrees, minutes):
    return(degrees + minutes/60)

def north_south(n_or_s, decimaldegrees):
    if(n_or_s == "S"):
        return(decimaldegrees * -1)
    else:
        return(decimaldegrees)

def gps_signal_fix(indicator):
    match indicator:
        case '0':
            return("FAILURE") # - Fix Not Available
        case '1':
            return("FIX - GPS")
        case '2':
            return("FIX - Differential GPS")
        case '3':
            return("FIX - PPS")
        case '4':
            return("FIX - Real Time Kinematic")
        case '5':
            return("FIX - Float RTK")
        case '6':
            return("FAILURE") # - Estimated (Dead Reckoning)
        case '7':
            return("FAILURE") # - Manual Input Mode
        case '8':
            return("FAILURE") # - Simulation Mode

def hdop_dilution_interpretation(reading):
    if(0 <= float(reading) <= 0.9999999):
        return("optimal")
    if(1 <= float(reading) <= 4.9999999):
        return("acceptable")
    if(float(reading) >= 5):
        return("FAILURE")

ser = serial.Serial('COM4', 9600, timeout=1.0)
base_list = []

t_end = time.time() + 10 * 1
while time.time() < t_end:
    read_bytes = ser.readline()
    decoded_bytes = read_bytes.decode("utf-8")
    data_list = decoded_bytes.split(",")
    if(data_list[0] == '$GNGGA'):
        now = datetime.now()
        y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
        utc = data_list[1]
        lat = decimal_degrees(*degrees_minutes(data_list[2]))
        n_s = data_list[3]
        lon = north_south(data_list[3], decimal_degrees(*degrees_minutes(data_list[4])))
        e_w = data_list[5]
        gps_signal_fix = gps_signal_fix(data_list[6])
        no_satellites = data_list[7]
        horizontal_dilution = data_list[8]
        hdi = hdop_dilution_interpretation(data_list[8])
        altitude = data_list[9]
        station_id = data_list[14]
        base_list.append([y_m_d_h_m_s, lat, n_s, lon, e_w, gps_signal_fix, no_satellites, horizontal_dilution, hdi, altitude, station_id])
        print(time.time(), t_end)

df = pd.DataFrame(base_list ,columns=['y_m_d_h_m_s', 'lat','n_s', 'lon', 'e_w', 'gps_signal_fix_type', 'no_satellites', 'horizontal_dilution', 'hdi', 'altitude', 'station_id'])
print(df)
