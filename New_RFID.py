import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Send the "set protocol" command
ser.write(b'\xA0\x03\x03\x03\xD9')

# Wait for the reader to respond
response = ser.read(4)
if response != b'\xA0\x03\x00\xF7':
    print('Error setting protocol')
    exit()

# Send the "write tag" command
ser.write(b'\xA0\x07\x02\xEB\x03\x01\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF')

# Wait for the reader to respond
response = ser.read(4)
if response != b'\xA0\x07\x00\xE5':
    print('Error writing tag')
    exit()

print('Tag written successfully')
