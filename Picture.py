import pymysql
from io import BytesIO
from picamera import PiCamera
from time import sleep

try:
    db = pymysql.connect(host='172.20.10.11',
                         user='jevin',
                         password='password',
                         database='GarbageDB')
except Exception as e:
    print("error",e)

print("Connection Successful")

cam = PiCamera()
cam.start_preview()
sleep(2)
cam.capture('image.jpg')
cam.stop_preview()

with open("image.jpg","rb") as f:
    image_data = f.read()

blob_data = BytesIO(image_data)


cursor = db.cursor()
sql = "INSERT INTO Images (Photo_data) VALUES (%s)"

cursor.execute(sql, (blob_data.read()))
db.commit()
