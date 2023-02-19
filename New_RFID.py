import usb.core
import usb.util

# Set up the USB device
dev = usb.core.find(idVendor=0x0403, idProduct=0x6015)
if dev is None:
    raise ValueError('Device not found')

# Set the configuration
dev.set_configuration()

# Set up the endpoint
endpoint_out = dev[0][(0, 0)][0]

# Define the data to write to the tag
data = bytearray(b'\xE0\x00\x00\x2C\x05\x00\x01\x01\x01\x03\x00\x00\x02\xD5\x41\x43\x4D\x45\x20\x54\x45\x53\x54\x20\x54\x41\x47')

# Write the data to the tag
try:
    dev.write(endpoint_out.bEndpointAddress, data, 1000)
    print("Data written to tag successfully!")
except usb.core.USBError as e:
    print("Error writing to tag: ", e)
