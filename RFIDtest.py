import serial
import binascii

# Configure the serial port
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# Send the Inventory command to the reader
ser.write(bytes([0xA0, 0x04, 0x03, 0x22, 0x00, 0x01, 0x60, 0x00]))

# Read and decode tag data packets
while True:
    # Read a data packet from the serial port
    data_packet = ser.read(1024)
    if not data_packet:
        continue

    # Parse the data packet and extract the EPC value
    if data_packet[0] == 0xA0 and data_packet[2] == 0x09 and data_packet[3] == 0x66:
        epc_length = data_packet[7]
        epc = data_packet[8:(epc_length + 8)]
        epc_hex = binascii.hexlify(epc).decode('latin-1')
        epc_str = epc_hex.upper()

        # Print the EPC value of the detected tag
        print("Detected tag with EPC:", epc_str)
