import usb.core
import usb.util
import time

# Constants for USB communication
VENDOR_ID = 0x16c0
PRODUCT_ID = 0x27db
TIMEOUT = 1000

# Define the USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise ValueError('Device not found')

# Detach the kernel driver
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Get the first interface and claim it
interface = dev.get_interface(0)
usb.util.claim_interface(dev, interface)

# Write data to the device
endpoint_out = interface.endpoints()[0]
data = [0x05, 0x00, 0x01, 0x00, 0x01, 0x00, 0x0b, 0x4a, 0x42, 0x3f, 0x3e, 0x3c, 0x3a, 0x32, 0x2c, 0x01]
dev.write(endpoint_out.bEndpointAddress, data, TIMEOUT)

# Wait for 100ms before reading data
time.sleep(0.1)

# Read data from the device
endpoint_in = interface.endpoints()[1]
data = dev.read(endpoint_in.bEndpointAddress, endpoint_in.wMaxPacketSize, TIMEOUT)

# Print the data received
print(data)

# Release the interface and reattach the kernel driver
usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(0)

# Detach the USB device
usb.util.dispose_resources(dev)
