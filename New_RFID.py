import pymysql
import serial

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

try:
    db = pymysql.connect(host='172.20.10.11',
                         user='jevin',
                         password='password',
                         database='GarbageDB')
except Exception as e:
    print ("Error:",e)

print("Connection Successful")

cursor = db.cursor()
sql = "INSERT INTO RFID (EPC) VALUES (%s)"
print("Put Tag Near Reader")

while True:
    data = ser.readline().decode()          ##.decode().rstrip()
    if data:
        cursor.execute(sql, (data))
        db.commit()
