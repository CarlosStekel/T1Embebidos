import serial
import time
from struct import pack, unpack, calcsize
import matplotlib.pyplot as plt

# Set the COM port and baud rate
COM_PORT = 'COM4'  # Replace with your COM port
BAUD_RATE = 115200  # Match the baud rate used by your ESP32s2

# Open the serial connection
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 1)

# Functions 
def graficar(listas_mediciones, titulos, xlabels, ylabels):  
    num_listas = len(listas_mediciones)
    
    # Crear un gráfico con subplots
    fig, axes = plt.subplots(num_listas, 1, figsize=(10, 6*num_listas))
    
    for idx, (mediciones, ax) in enumerate(zip(listas_mediciones, axes)):
        ax.plot(mediciones, linestyle='-')
        ax.set_title(titulos[idx])
        ax.set_xlabel(xlabels[idx])
        ax.set_ylabel(ylabels[idx])
        ax.set_ylim(-20, 20)
        ax.grid(True)
    
    # Ajustar layout
    plt.tight_layout()
    plt.show()



def send_message(message):
    ser.write(message)

def receive_response():
    response = ser.read_until(b'\x00')  # Reading until \0
    return response[:-1]

def receive_data():
    data = receive_response()
    data = unpack("ffffff", data)
    print(f'Received: {data}')
    return data

def send_end_message():
    end_message = pack('4s', 'END\0'.encode())
    ser.write(end_message)

# Send "BEGIN" message
message = pack('6s','BEGIN\0'.encode())
ser.write(message)
ok = receive_response()
ok = ok.decode('utf-8')
if ok == "OK":
    print("Received OK message")

while True:
    print("------------------------------------------------------------------------")
    print("¿Que quiere hacer? (ingrese el numero con su decision)")
    print("1. Tomar Datos")
    print("2. Configurar el Sensor")
    print("3. Cambiar Modo de Poder")
    print("4. Cerrar Interfaz")
    print("------------------------------------------------------------------------")
    accion = input("=> ")
    if accion == "1":
        message = pack('6s','START\0'.encode())
        ser.write(message)
        message = pack('10s','DATASTART\0'.encode())
        ser.write(message)
        AccX = []
        AccY = []
        AccZ = []
        GyrX = []
        GyrY = []
        GyrZ = []
        FFTAccX = []
        FFTAccY = []
        FFTAccZ = []
        FFTGyrX = []
        FFTGyrY = []
        FFTGyrZ = []
        
        titulos = [f"" for i in range(12)]
        xLabels = [f"" for i in range(12)]
        yLabels= ['AccX','AccY','AccZ','GyrX','GyrY','GyrZ','FFTAccX','FFTAccY','FFTAccZ','FFTGyrX','FFTGyrY','FFTGyrZ']
        mediciones = [AccX,AccY,AccZ,GyrX,GyrY,GyrZ,FFTAccX,FFTAccY,FFTAccZ,FFTGyrX,FFTGyrY,FFTGyrZ]
        for i in range(100):
            response = receive_response()
            while(response == b''):
                response = receive_response()
            arr = [float(i) for i in response.decode('utf-8').split()]
            AccX.append(arr[0])
            AccY.append(arr[1])
            AccZ.append(arr[2])
            GyrX.append(arr[3])
            GyrY.append(arr[4])
            GyrZ.append(arr[5])
            FFTAccX.append(arr[6])
            FFTAccY.append(arr[7])
            FFTAccZ.append(arr[8])
            FFTGyrX.append(arr[9])
            FFTGyrY.append(arr[10])
            FFTGyrZ.append(arr[11])
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("peaks aceleracion X: " + response.decode('utf-8'))
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("peaks aceleracion Y: " + response.decode('utf-8'))
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("peaks aceleracion Z: " + response.decode('utf-8'))
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("peaks giroscopio X: " + response.decode('utf-8'))
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("peaks giroscopio Y: " + response.decode('utf-8'))
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("peaks giroscopio Z: " + response.decode('utf-8'))
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print("RMS's: " + response.decode('utf-8'))
        graficar(mediciones, titulos, xLabels, yLabels)       
            
    elif accion == "2":
        message = pack('6s','CONFI\0'.encode())
        ser.write(message)
        response = receive_response()
        print(response.decode('utf-8'))
        if response.decode('utf-8') == "LLEGO CONFIG":
            estabien = True
            while (estabien):
                acc_odr = int(input("Selecciona un valor de odr para la aceleración [0x01 a 0x0c] (ver datasheet):"), 16)
                acc_range = int(input("Selecciona un valor de rango para la aceleración [0x00 a 0x03] (ver datasheet):"), 16)
                gyr_odr = int(input("Selecciona un valor de odr para el giroscopio [0x06 a 0x0d] (ver datasheet):"), 16)
                gyr_range = int(input("Selecciona un valor de rango para el giroscopio [0x00 a 0x04] (ver datasheet):"), 16)
                
                if "si"==input("Esta bien? (si/no):"):
                    estabien=False
            config = str(acc_odr).zfill(2)+str(acc_range).zfill(2)+str(gyr_odr).zfill(2)+str(gyr_range).zfill(2)+'\0'
            print(config)
            conf_mes = pack('9s',config.encode())
            ser.write(conf_mes)
            print(receive_response().decode('utf-8'))

    elif accion == "3":
        message = pack('6s', 'POWER\0'.encode())
        ser.write(message)
        response = receive_response()
        print(response.decode('utf-8'))
        print("Elige modo de poder")
        print("1. Low Power Mode")
        print("2. Performance Power Mode")
        print("3. Normal Power Mode")
        print("4. Suspend")    
        accion2 = input("=> ")
        if accion2 == "1":
            message = pack('6s', 'LOWER\0'.encode())
            ser.write(message)
        if accion2 == "2":
            message = pack('6s', 'PERFO\0'.encode())
            ser.write(message)
        if accion2 == "3":
            message = pack('6s', 'NORML\0'.encode())
            ser.write(message)
        if accion2 == "4":
            message = pack('6s', 'SUSPE\0'.encode())
            ser.write(message)
        response = receive_response()
        while(response == b''):
            response = receive_response()
        print(response.decode('utf-8'))

    elif accion == "4":
        message = pack('6s','BREAK\0'.encode())
        ser.write(message)
        response = receive_response()
        print(response.decode('utf-8'))
        break

# Read data from the serial port, waiting for the data
# counter = 0
# while True:
#     if ser.in_waiting > 0:
#         try:
#             #datos_serializados = ser.read(calcsize('3f3f3f15f600f'))
#             #print(f'Received: {unpack("3f3f3f15f600f", datos_serializados)}')
            
#             message = receive_response()
#             print(message)
#             print(f'Received: {unpack("cc", message)}')
#         except Exception as e:
#             print(e)
#             continue
#         else: 
#             counter += 1
#             print(counter)

# # Sending message to end data sending
# send_end_message()

# # Waiting for message OK to end communications
# while True:
#     if ser.in_waiting > 0:
#         try:
#             message = receive_response()
#             msg = message.decode('utf-8')
#         except:
#             print('Error en leer mensaje')
#             continue
#         else: 
#             if msg == 'OK':
#                 print('Cerrando conexión...')
#                 break
# ser.close()
        