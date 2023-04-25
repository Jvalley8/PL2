import pymysql
import serial
from io import BytesIO
from picamera import PiCamera
from time import sleep

power_key = 6
serRFID = serial.Serial('/dev/ttyACM0', 115200, timeout = 1) #Change PORT
serGPS = serial.Serial('/dev/ttyUSB3',115200, timeout = 1)

def Cam_TakePic():
    cam = PiCamera()
    for i in (i<=3):
        cam.start_preview()
        





try:
    db = pymysql.connect(host='172.20.10.11',
                         user='jevin',
                         password='password',
                         database='GarbageDB')
except Exception as e:
    print("error",e)

print("Connection Successful")

cursorRFID = db.cursor()
sqlRFID = "INSERT INTO RFID (EPC) VALUES (%s)"
print("Put Tag Near Reader")

cursorGPS = db.cursor()
sqlGPS = "INSERT INTO GPS (Coordinates) VALUES (%s)"
print("GPS is being put in database")






while True:
    data = serRFID.readline().decode()          ##.decode().rstrip()
    if data:

        cursorRFID.execute(sqlRFID, (data))
        db.commit()
