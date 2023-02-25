import serial

# Set up the serial connection
ser = serial.Serial(
    port='/dev/serial0', # serial port connected to the M6E Nano reader
    baudrate=115200,     # baud rate for the serial connection
    timeout=1            # timeout for the serial read
)

# Enable write mode
ser.write(bytes.fromhex('B001800000')) # EPC Gen2 Set Write Mode Command

# Write the tag data (replace '11223344' with the desired tag data)
ser.write(bytes.fromhex('B304' + '11223344')) # EPC Gen2 Write Tag Command

# Read the response from the M6E Nano
response = ser.read(128)

# Print the response
print(response)
