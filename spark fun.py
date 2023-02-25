stringEPC = "Hello!"
byteList = [ord(char) for char in stringEPC]  # Convert the string to a list of bytes
responseType = nano.writeTagEPC(byteList, len(byteList))
