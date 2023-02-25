import serial

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # replace '/dev/ttyS0' with your serial port

# command to write to tag
cmd = bytearray([0xBB, 0x08, 0x00, 0x00, 0x00, 0x01, 0x01, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x01, 0xE0, 0x04, 0x0E])

ser.write(cmd)

response = ser.read(20)

# check response for success/failure
if response[2] == 0x00:
    print("Tag write successful")
else:
    print("Tag write failed")

ser.close()
