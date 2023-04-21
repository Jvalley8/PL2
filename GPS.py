
import RPi.GPIO as GPIO
import serial
import time

# Get the right baudrate and serial port.
ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
rec_buff = ''


def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			
			
			global GPSDATA
			# Gets the NMEA GPS data, and cleans it to removes the prefix from the GPS data and stores the cleaned data in the variable (Cleaned)
			GPSDATA = str(rec_buff.decode())
			Cleaned = GPSDATA[13:]
			
			#Extracts the first two characters from the cleaned GPS data which represents the degrees of the latitude coordinate.
			Lat = Cleaned[:2]

			
			#extracts the next 9 characters from the cleaned GPS data, which characters represent the minutes and seconds of the latitude coordinate.
			SmallLat = Cleaned[2:11]
			#extracts the 13th character from the cleaned GPS data, indicates whether the latitude coordinate is north or south of the equator.
			NorthOrSouth = Cleaned[12]
			
			#extracts the 15th to 17th characters from the cleaned GPS data which represent the degrees of the longitude coordinate.
			Long = Cleaned[14:17]
			#extracts the next 9 characters from the cleaned GPS data, represents the minutes and seconds of the longitude coordinate.
			SmallLong = Cleaned[17:26]
			#extracts the 28th character from the cleaned GPS data and stores it, indicates  whether the longitude coordinate is east or west of the prime meridian.
			EastOrWest = Cleaned[27]
			
			#Calculates the final latitude and longitude coordinate. The division by 60 is necessary to convert minutes to decimal degrees.
			FinalLat = float(Lat) + (float(SmallLat)/60)
			FinalLong = float(Long) + (float(SmallLong)/60)
			
			#If the latitude coordinate is south of the equator, this line of code negates the final latitude coordinate and Vice versa.
			if NorthOrSouth == 'S': FinalLat = -FinalLat
			if EastOrWest == 'W': FinalLong = -FinalLong
			
			Final_Coordinates = str(FinalLat) +"," + str(FinalLong)
			print(Final_Coordinates)
			#print(FinalLat, FinalLong)
			
			
			return 1
	else:
		print('GPS is not ready')
		return 0

def get_gps_position():
	rec_null = True
	answer = 0
	print('Start GPS session...')
	rec_buff = ''
	send_at('AT+CGPS=1,1','OK',1)
	time.sleep(2)
	while rec_null:
		answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
		if 1 == answer:
			answer = 0
			if ',,,,,,,,' in rec_buff:
				print('GPS is not ready')
				rec_null = False
				time.sleep(1)
		else:
			print('error %d'%answer)
			rec_buff = ''
			send_at('AT+CGPS=0','OK',1)
			return False
		time.sleep(1.5)


def power_on(power_key):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(power_key):
	print('SIM7600X is loging off:')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18)
	print('Good bye')

#Additions to Demo GPS.py Code Added by Tim // Simplfing the GPS Start up process

def main():
    power_on(power_key)
    while True:
        get_gps_position()
        
try:
    main()
except:
    print("An error has occured")

