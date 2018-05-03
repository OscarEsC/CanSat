import serial, time
import matplotlib.pyplot as plt

def columnNames(file):
	#File's head
	file.write("Presión(kPa)\tTemperatura(°C)\torientación X(gps)\torientación Y(gps)\t")
	file.write("orientación Z(gps)\tRapidez(m/s^2)\tAltura(m)\tVelocidad(m/s)\tTiempo(s)")
	file.write("\n")

def getData():
	#Read the binary data from the xBee, transform into a string
	#and split into a list
	lecture = xBee.readline().decode('utf-8');
	lecture = lecture[:-2]
	lecture = lecture.split(',')
	return lecture

def writeFile(data, file):
	#if len(pressList) != 0:
	file.write(str(pressList[-1])+"\t\t\t"+str(tempList[-1])+"\t\t"+str(Xorient[-1])+"\t\t\t")
	file.write(str(Yorient[-1])+"\t\t\t"+str(Zorient[-1])+"\t\t"+str(speed[-1])+"\t\t")
	file.write(str(altitude[-1])+"\t\t"+str(velList[-1])+"\t\t"+str(timeList[-1]))
	file.write("\n")

def updateList(lecture):
	#Append the last lecture of the xBee
	if len(lecture) == 7:
		pressList.append(round(float(lecture[0])/1000,2))
		tempList.append(round(float(lecture[1]),1))
		Xorient.append(float(lecture[2]))
		Yorient.append(float(lecture[3]))
		Zorient.append(float(lecture[4]))
		speed.append(float(lecture[5]))
		altitude.append(float(lecture[6]))
		timeList.append(round(time.clock(), 2))

		#Getting the velocity
		if len(speed) == 0:
			velList.append(0)
		else:
			velList.append(speed[-1]*timeList[-1])


def plots():
	#Pressure plot
	plt.subplot(221)
	plt.plot(timeList, pressList)
	plt.title('Presión')
	plt.ylabel('Presión (kPa)')
	plt.xlabel('Tiempo (s)')

	#Temperature plot
	plt.subplot(222)
	plt.plot(timeList, tempList)
	plt.title('Temperatura')
	plt.ylabel('Temperatura (°C)')
	plt.xlabel('Tiempo (s)')

	#Speed and Velocity plot
	plt.subplot(223)
	plt.plot(timeList, speed)
	plt.title('Rapidez')
	plt.ylabel('Rapidez (m/s^2) y Vel (m/s)')
	plt.xlabel('Tiempo (s)')

	#Altitude plot
	plt.subplot(224)
	plt.plot(timeList, altitude)
	plt.title('Altura')
	plt.ylabel('Altura (m)')
	plt.xlabel('Tiempo (s)')

	plt.subplots_adjust(bottom=0.15,left= 0.15, top=0.93, wspace=0.42,hspace=0.42)
	plt.pause(0.05) # esto pausará el gráfico
	plt.cla()

def main():
	file = open("datosleidosCanSat.txt", "w")
	columnNames(file)
	while (1):
		data = getData()
		try:
			updateList(data)
			writeFile(data, file)
			plots()
		except:
			break
	print("No hay grafica\n")
	file.close()
	print("Se ha cerrado la conexión con el xBee.")

#Connect with the Xbee and wait for the conection
xBee = serial.Serial('COM4', 9600)
time.sleep(.500)
print("Conexión establecida.")
#To get the time in order to fill timeList. The next time.clock() give us
#the time after excecute the next line
time.clock()
#Indicate that the graphs will be interactive
plt.ion()

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