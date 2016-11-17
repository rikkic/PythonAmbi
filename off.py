import serial
ser = serial.Serial('COM3', 57600)
time.sleep(5)
pixels = ""
for x in range(0,30):
	pixels += "000000000"
ser.write(pixels + ";")