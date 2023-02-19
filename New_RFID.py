import usb.core
import usb.util
import sys

# Check Python version compatibility
if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 4):
    raise Exception("PyUSB requires at least Python 3.4")

# Find J4210U device
dev = usb.core.find(idVendor=0x1c34, idProduct=0x724e)

# Check if device is found
if dev is None:
    raise Exception("J4210U device not found")

# Set configuration
dev.set_configuration()

# Write to tag
ep_out = dev[0][(0, 0)][0]
ep_out.write(b'\x00\x00\x00\x00\x02\x05\x00\x00\x00')

# Read tag response
ep_in = dev[0][(0, 0)][1]
response = ep_in.read(8)

# Print response
print(response)
