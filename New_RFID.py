import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Reset the reader
ser.write(b'\x02\x00\x00\x03\x00\x01\xB5\xCD')
response = ser.read(10)
print(response)

# Set the region to North America
ser.write(b'\x02\x01\x07\x03\x01\x6A\xBB\xB5')
response = ser.read(10)
print(response)

# Set the protocol to EPC Gen2
ser.write(b'\x02\x01\x08\x03\x01\x6B\xDA\x5E')
response = ser.read(10)
print(response)

# Enable the antenna
ser.write(b'\x02\x01\x0A\x03\x01\x00\xCE\xCF')
response = ser.read(10)
print(response)

# Write to tag
ser.write(b'\x02\x01\x21\x07\x01\x00\x01\x03\xE8\x00\x01\xD0\x13')
response = ser.read(10)
print(response)

ser.close()
