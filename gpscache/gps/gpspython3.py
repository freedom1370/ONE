
import serial
import time
from pynmea import nmea
import socket


lat = 0
lon = 0
time = 0
n_time = 0
n_lat = 0
n_lon = 0
tll = 0
data = 0



# Подключение к последовательному порту 
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'com8'
ser.timeout = 10

#Открываем если получаем ошибку то нужно перестартовать
ser.open()




while 1:
        line = ser.readline()


        #t = line

        line = line.decode('utf8')

        if(line.startswith('$GPGGA')):
              gpgga = nmea.GPGGA()
              gpgga.parse(line)

              time = (gpgga.timestamp)
              lat = (gpgga.latitude)
              lon = (gpgga.longitude)




#convert degrees,decimal minutes to decimal degrees -Нужно конвертить минуты иначе попадаем в район Славянки
              lat1 = (float(lat[2]+lat[3]+lat[4]+lat[5]+lat[6]+lat[7]+lat[8]))/60
              lat = (float(lat[0]+lat[1])+lat1)
              long1 = (float(lon[3]+lon[4]+lon[5]+lon[6]+lon[7]+lon[8]+lon[9]))/60
              lon = (float(lon[0]+lon[1]+lon[2])+long1)
              #calc position
	  #    pos_y = lat
      #   pos_x = long #longitude is negaitve


              
#Преобразовываем в стринг
              n_time = str(time)
              n_lat = str(lat)
              n_lon = str(lon)

              data = (host+","+n_time+","+n_lat+","+n_lon)
            # В байты  
              n_time = n_time.encode()
              n_lat = n_lat.encode()
              n_lon = n_lon.encode()
              data = data.encode()
              
              
        tll = (n_time,n_lat,n_lon)
       # print  ("TIME", time)
       # print ("Lat", lat)
       # print ("Long", lon)
        print (data)



# Передача данных через сокет в cache >>

        

         # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        

        # get local machine name
        host = socket.gethostname()                           

        port = 8089

        # connection to hostname on the port.
        s.connect((host, port))                               


        # Receive no more than 1024 bytes
        
        s.send(bytes(data))
        #s.send(bytes(n_time))
        #s.send(bytes(n_lat))
        #s.send(bytes(n_lon))
        


        

      
