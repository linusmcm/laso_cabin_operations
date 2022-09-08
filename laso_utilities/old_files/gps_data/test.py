from serial import Serial
from pyubx2 import UBXReader, UBXMessage, GET, SET, POLL, VALCKSUM
import json
from google.protobuf.json_format import MessageToJson, MessageToDict
import pynmea2

stream = Serial('COM4', 9600, timeout=1)
# ubr = UBXReader(stream,protfilter=1)#3
# (raw_data, parsed_output) = ubr.read()
# print(parsed_output)




ubr = UBXReader(stream, protfilter=3, parsebitfield = 0)
(raw_data, parsed_output) = ubr.read()
#print(parsed_output)
for (raw_data, parsed_data) in ubr:
    if parsed_data.identity == "GNGGA":
        print(parsed_data.lon)
        print(parsed_data.lat)
        print(parsed_data.alt)

# parsed_data = UBXReader.parse(parsed_output)
# print(parsed_data)
# msg = pynmea2.parse(raw_data, check=False)
# print(msg)

#msg = UBXReader.parse(raw_data)
#print(msg.lon)
#data = parsed_data.split(',')
#print(data)
# while True:
#     ubr = UBXReader(stream)
#     (raw_data, parsed_data) = ubr.read()
#     # parsed_data = stream.readline()
#     print(parsed_data)
#     # decoded_bytes = parsed_data.decode("utf-8")
#     # data = decoded_bytes.split(',')
#     # print(data)


    # pos1 = x.find("$GPRMC")
    # pos2 = x.find("\n", pos1)
    # loc  = x[pos1:pos2]
    # data = loc.split(',')
    # if data[2] == 'V':
    #     print('No location found')
    # else:
    #     print("Latitude =" + data[3])
    #     print("Longitude =" + data[5])
    #print(parsed_data)

# ubr = UBXReader(stream, protfilter=7)
# for (raw_data, x) in ubr.iterate():
#     pos1 = x.find("$GPRMC")
#     pos2 = x.find("\n", pos1)
#     loc  = x[pos1:pos2]
#     data = loc.split(',')
#     if data[2] == 'V':
#         print('No location found')
#     else:
#         print("Latitude =" + data[3])
#         print("Longitude =" + data[5])
#     #print(parsed_data)


# stream = Serial('COM4', 9600, timeout=3)
# ubr = UBXReader(stream, protfilter=7)
# (raw_data, parsed_data) = ubr.read()
# print(parsed_data)
# if parsed_data.identity == "GNRMC":
#     print(parsed_data.lat)
#     print(parsed_data.lon)


#(raw_data, parsed_output) = ubr.read()
# print(raw_data)
# print("------------------------------")
# print(parsed_output)
# msg1 = UBXMessage(raw_data, validate=VALCKSUM, msgmode=GET, parsebitfield=True)
# print(msg1)
