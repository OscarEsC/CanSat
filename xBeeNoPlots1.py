import serial, time
import msvcrt
import matplotlib.pyplot as plt
import math

def columnNames(file):
	#File's head
	file.write("Presión(kPa)\tTemperatura(°C)\torientación X(gps)\torientación Y(gps)\t")
	file.write("orientación Z(gps)\tAceleracion(m/s^2)\tAltura(m)\tVelocidad(m/s)\tTiempo(s)")
	file.write("\n")

def getData(xBee):
	#Read the binary data from the xBee, transform into a string
	#and split into a list
	#Delete the data in the input buffer
	xBee.flushInput()
	lecture = xBee.readline().decode('utf-8');
	lecture = lecture[:-2]
	lecture = lecture.split(',')
	return lecture

def writeFile(file):
	#Write the input data into the file	
	for i in range(0,len(pressList)):
		file.write(str(pressList[i])+"\t\t\t"+str(tempList[i])+"\t\t"+str(Xorient[i])+"\t\t\t")
		file.write(str(Yorient[i])+"\t\t\t"+str(Zorient[i])+"\t\t\t"+str(speed[i])+"\t\t  ")
		file.write(str(altitude[i])+"\t\t"+str(velList[i])+"\t\t"+str(timeList[i] - timeList[0]))
		file.write("\n")

def updateList(lecture, t, p, a):
	#Append the last lecture of the xBee
	try:
		if len(lecture) == 9 and float(lecture[0]) > 70000 and float(lecture[0]) < 100000:
			timeList.append(round(time.clock(), 2))
			pressList.append(round(float(lecture[0])/1000,2))
			tempList.append(round(float(lecture[1]),1))
			Xorient.append(float(lecture[2]))
			Yorient.append(float(lecture[3]))
			Zorient.append(float(lecture[4]))
			sp = math.sqrt(pow(float(lecture[5]),2) + pow(float(lecture[6]),2) + pow(float(lecture[7]),2))
			speed.append(round(sp,2))
			altitude.append(float(lecture[8]))
			

			if pressList[-1] > p:
				p = pressList[-1]
			if tempList[-1] > t:
				t = tempList[-1]
			if altitude[-1] > a:
				a = altitude[-1]
		
		return [p,t,a]

	except ValueError:
		return [p,t,a]

def getVelocity(aMax):
	#sqrt(2*g*h) -> rising
	#sqrt(2*g*(hmax-h)) -> falling
	for i in range(0,len(speed)):
		if altitude[i] < aMax:
			if altitude[i] < altitude[0]:
				d = 0
			else:
				d = 2*speed[i]*(altitude[i]-altitude[0])
			
		else:
			d = 2*speed[i]*(aMax - altitude[i])
		velList.append(round(float(math.sqrt(d)),2))

def plots():
	plt.figure(1)
	#Pressure plot
	plt.subplot(321)
	plt.plot(timeList, pressList)
	plt.title('Presión')
	plt.ylabel('Presión (kPa)')
	plt.xlabel('Tiempo (s)')

	#Temperature plot
	plt.subplot(322)
	plt.plot(timeList, tempList)
	plt.title('Temperatura')
	plt.ylabel('Temperatura (°C)')
	plt.xlabel('Tiempo (s)')

	#Speed plot
	plt.subplot(323)
	plt.plot(timeList, speed)
	plt.title('Aceleracion')
	plt.ylabel('Aceleración (m/s^2)')
	plt.xlabel('Tiempo (s)')

	#Velocity plot
	plt.subplot(324)
	plt.plot(timeList, velList)
	plt.title('Velocidad')
	plt.ylabel('Velocidad (m/s)')
	plt.xlabel('Tiempo (s)')

	#Altitude plot
	plt.subplot(325)
	plt.plot(timeList, altitude)
	plt.title('Altura')
	plt.ylabel('Altura (m)')
	plt.xlabel('Tiempo (s)')

	plt.subplots_adjust(bottom=0.10	,left= 0.15, top=0.93, wspace=0.32,hspace=0.82)

def main():
	tMax = 0
	pMax = 0
	aMax = 0
	#Connect with the Xbee and wait for the conection
	xBee = serial.Serial('COM4', 9600)
	#To get the time in order to fill timeList. The next time.clock() give us
	#the time after excecute the next line
	time.clock()
	c = 0
	print("Conexión establecida.")
	file = open("datosleidosCanSat.txt", "w")
	columnNames(file)
	#It'll stop when a keyboard key is pressed
	while not (msvcrt.kbhit()):
		data = getData(xBee)
		c += 1
		#Get the maximum values
		maxi = updateList(data, tMax, pMax, aMax)
		pMax = maxi[0]
		tMax = maxi[1]
		aMax = maxi[2]
		#writeFile(data, file)

		if c%5 == 0:
			print("\nPresión máxima: ", pMax)
			print("Temperatura máxima: ", tMax)
			print("Altura máxima: ", aMax)
			print("Orientacion: "+ str(Xorient[-1])+", "+ str(Yorient[-1])+", "+ str(Zorient[-1])+ " dps")

	print("c: ", c)
	print("t: ", time.clock())
	getVelocity(aMax)
	print("len: ", len(velList))
	writeFile(file)
	file.write("\nTotal de datos leídos: "+ str(len(pressList)))
	file.close()
	xBee.close()
	print("\n\nSe ha cerrado la conexión con el xBee.")
	print("Graficando los datos obtenidos...")	
	plots()
	plt.show()



#Declare the list where the data will be stored
tempList = []
pressList = []
Xorient = []
Yorient = []
Zorient = []
speed = []
altitude = []
velList = []
timeList = []

main()