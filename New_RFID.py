import serial
import time

# Open serial port
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Reset the module
ser.write(b'\xA0\x03\x01\x00\xA2')
response = ser.read(7)

if response != b'\xA0\x03\x00\x00\xA3\xF7\xC0':
    print('Error resetting module')
    ser.close()
    exit()

# Set the region to North America
ser.write(b'\xA0\x04\x01\x01\x01\xA8')
response = ser.read(7)

if response != b'\xA0\x04\x00\x00\xA4\xD4\x38':
    print('Error setting region')
    ser.close()
    exit()

# Write the EPC to tag
epc = 'E280110B0064015017DC93E0'
ser.write(bytes.fromhex('A0 23 03 01 00 ' + '{:02X}'.format(len(epc) // 2) + ' ' + epc))
response = ser.read(7)

if response != b'\xA0\x23\x00\x00\xA3\x13\x60':
    print('Error writing EPC')
    ser.close()
    exit()

print('Tag written successfully')

# Close serial port
ser.close()
