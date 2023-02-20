import serial

ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)

# Reset and Set Region to FCC
ser.write(b'\xA0\x03\x01\x00\xA2')
ser.read(7)

print("Place tag within range to write EPC")
input("Press Enter to continue...")

# Write EPC to Tag
tag_id = b'\x30\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
ser.write(b'\xA0\x04\x03\x01\x02\xE0' + tag_id)
ser.read(7)

print("Place tag within range to read EPC")
input("Press Enter to continue...")

# Read EPC from Tag
ser.write(b'\xA0\x03\x01\x00\xA2')
epc = ser.read(20)

print("EPC read from tag: ", epc.hex())
