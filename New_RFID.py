import usb.core
import usb.util
import time

# find the J4210U RFID reader device
dev = usb.core.find(idVendor=0x16c0, idProduct=0x27db)
if dev is None:
    raise ValueError('Device not found')

# detach the kernel driver from the interface
for cfg in dev:
    for intf in cfg:
        if dev.is_kernel_driver_active(intf.bInterfaceNumber):
            try:
                dev.detach_kernel_driver(intf.bInterfaceNumber)
            except usb.core.USBError as e:
                sys.exit("Could not detach kernel driver: %s" % str(e))

# claim the device interface
usb.util.claim_interface(dev, 0)

# write data to the tag
tag_id = b'\x01\x02\x03\x04'
tag_data = b'Hello, world!'
write_data = tag_id + tag_data
packet_size = 64
num_packets = len(write_data) // packet_size + 1
for i in range(num_packets):
    packet_data = write_data[i*packet_size:(i+1)*packet_size]
    packet_data += b'\x00' * (packet_size - len(packet_data))
    dev.write(0x01, packet_data, 1000)
    time.sleep(0.05)

# release the device interface
usb.util.release_interface(dev, 0)

