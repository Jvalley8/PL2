import pymysql
import serial
from io import BytesIO
from picamera import PiCamera
from time import sleep

power_key = 6
serRFID = serial.Serial('/dev/ttyACM0', 115200, timeout = 1) #Change PORT
serGPS = serial.Serial('/dev/ttyUSB3',115200, timeout = 1)

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
cursorGPS = db.cursor()
sqlGPS = "INSERT INTO GPS (Coordinates) VALUES (%s)"
cursor = db.cursor()
sql = "INSERT INTO Images (Photo_data) VALUES (%s)"


  
def take_picture():  
    cam = PiCamera()
    # Loop to take 3 pictures using the PiCamera and import them into the database as a BLOB
    for i in range(3):
        cam.start_preview()
        sleep(2)
        cam.capture('image.jpg')
        cam.stop_preview()
        with open("image.jpg","rb") as f:
            image_data = f.read()
        blob_data = BytesIO(image_data)
        cursor.execute(sql, (blob_data.read()))
        db.commit()
    cam.close()
    
    

def get_GPS():
    serGPS.write(b'AT+CGPS=1\r\n')
    sleep(2)
    serGPS.write(b'AT+CGPSINFO\r\n')
    Coordinates = serGPS.readline()
    ##print(Coordinates)
    if b'+CGPSINFO' in Coordinates:
        global GPSDATA
		# Gets the NMEA GPS data, and cleans it to removes the prefix from the GPS data and stores the cleaned data in the variable (Cleaned)
        GPSDATA = str(Coordinates.decode())
        Cleaned = GPSDATA[13:]

		#Extracts the first two characters from the cleaned GPS data which represents the degrees of the latitude coordinate.
        Lat = Cleaned[:2]
		#extracts the next 9 characters from the cleaned GPS data, which characters represent the minutes and seconds of the latitude coordinate.
        SmallLat = Cleaned[2:9]
		#extracts the 13th character from the cleaned GPS data, indicates whether the latitude coordinate is north or south of the equator.
        NorthOrSouth = Cleaned[10:11]
		#extracts the 15th to 17th characters from the cleaned GPS data which represent the degrees of the longitude coordinate.    
        Long = Cleaned[12:15]
		#extracts the next 9 characters from the cleaned GPS data, represents the minutes and seconds of the longitude coordinate.
        SmallLong = Cleaned[15:24]
		#extracts the 28th character from the cleaned GPS data and stores it, indicates  whether the longitude coordinate is east or west of the prime meridian.
        EastOrWest = Cleaned[25:26]

        FinalLat = float(Lat) + (float(SmallLat)/60)
        FinalLong = float(Long) + (float(SmallLong)/60)
        
        if NorthOrSouth == 'S': FinalLat = -FinalLat
        if EastOrWest == 'W': FinalLong = -FinalLong
        Final_Coordinates = str(FinalLat) +"," + str(FinalLong)
        
        if Final_Coordinates:
            print("GPS is being put in database")
            cursorGPS.execute(sqlGPS, (Final_Coordinates))
            db.commit()        


while True:
    data = serRFID.readline().decode()         
    if data:
        print("Searching for RFID Tag")
        get_GPS()
        take_picture()
        cursorRFID.execute(sqlRFID, (data))
        db.commit()
