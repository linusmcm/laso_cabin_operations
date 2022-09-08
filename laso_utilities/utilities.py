import os
import json
from datetime import datetime
import pandas as pd

ONE_GPS_METRE = 0.000009000009

def get_last_entry(filename):
    with open(filename,'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data, record_path =['stickReadings'])
    df = df.loc[df['waypoint'].idxmax()]
    df = pd.DataFrame(df).transpose()
    return(df)

def generate_log_message(cabin_id, error_type, processor, message):
    now = datetime.now()
    y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
    return {
        'log_type': error_type,
        'cabin_name': cabin_id,
        'processor': processor,
        'time_generated': str(now),
        'y_m_d_h_m_s': y_m_d_h_m_s,
        'log_message': message
    }

def generate_transaction(cabin_name, filename) -> dict:
    now = datetime.now()
    y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
    df = get_last_entry(filename)
    return {
        "cabin_name":cabin_name,
        "time_generated":str(now),
        "y_m_d_h_m_s":y_m_d_h_m_s,
        "going": df.iloc[-1]['going'],
        "index_value": float(df.iloc[-1]['index_value']),
        "penetrate": float(df.iloc[-1]['penetrate']),
        "shear": float(df.iloc[-1]['shear']),
        "waypoint": int(df.iloc[-1]['waypoint'])
    }

def generate_cabin_name():
    user_name = os.getlogin()
    if (user_name == "center"):
            user_name = "centre"
    return(user_name)

def laso_serializer(message):
    return json.dumps(message).encode('utf-8')

def degrees_minutes(x):
    degrees = float(x) // 100
    minutes = float(x) - 100 * degrees
    return(float(degrees), float(minutes))

def decimal_degrees(degrees, minutes):
    return(degrees + minutes/60)

def north_south(n_or_s, decimaldegrees):
    if(n_or_s == "S"):
        return(round(decimaldegrees * -1, 12))
    else:
        return(round(decimaldegrees,12))

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

def generate_gps_message(_cabin_name, _base_list):
    now = datetime.now()
    y_m_d_h_m_s = now.strftime("%Y%m%d%H%M%S")
    return {
        "cabin_name":_cabin_name,
        "y_m_d_h_m_s":y_m_d_h_m_s,
        "lat":_base_list[0],
        "n_s":_base_list[1],
        "lon":_base_list[2],
        "e_w":_base_list[3],
        "gps_fix":_base_list[4],
        "number_satellites":_base_list[5],
        "horizontal_dilution":_base_list[6],
        "hdi":_base_list[7],
        "altitude":_base_list[8],
        "station_id":_base_list[9]
    }
