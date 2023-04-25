import serial
import time
import pymysql

power_key = 6
ser = serial.Serial('/dev/ttyUSB3',115200, timeout = 1)

try:
    db = pymysql.connect(host='172.20.10.11',
                         user='jevin',
                         password='password',
                         database='GarbageDB')
except Exception as e:
    print ("Error:",e)

print("Connection Successful")

cursor = db.cursor()
sql = "INSERT INTO GPS (Coordinates) VALUES (%s)"
print("GPS is being put in database")


while True:
    ser.write(b'AT+CGPS=1\r\n')
    time.sleep(2)
    ser.write(b'AT+CGPSINFO\r\n')
    Coordinates = ser.readline()
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
            cursor.execute(sql, (Final_Coordinates))
            db.commit()





	
    

    
