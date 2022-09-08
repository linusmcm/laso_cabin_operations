from serial import Serial
from pyubx2 import UBXReader, UBXMessage, GET, SET, POLL, VALCKSUM

COM_PORT = 'COM4'

stream = Serial(COM_PORT, 9600, timeout=3)
ubr = UBXReader(stream, protfilter=7)
(raw_data, parsed_data) = ubr.read()
print(parsed_data)
if parsed_data.identity == "GNRMC":
    print(parsed_data.lat)
    print(parsed_data.lon)
