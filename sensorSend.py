from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import requests
# URL of the cloud server where the data will be pushed to

# IP Addresses and Port numbers of the UDP servers running 
# on two RRi's which have the LEDs connected.
RPI_1_IP = '10.20.0.20'
CLOUD_SERVER_URL = 'http://127.0.0.1:5001'


# Setting up a simple UDP server, used to receive data from
# the RPi having the sensor connected.
PORT_NUMBER = 8090
SIZE = 1024
hostName = gethostbyname('0.0.0.0')
mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))
print("Edge computer listening for input on port {}".format(PORT_NUMBER))

# Infinite loop to continuously look for data being sent
while True:
    # Receiving data from the Sensor RPi.
    # (data,addr) = mySocket.recvfrom(SIZE)
    # print('Received data: "{}". This will be sent to the server.'.data)
    # print('Received data: "{}". This will be sent to the server.'.format(data))
    (data, addr) = mySocket.recvfrom(SIZE)
    received_data = data.decode()
    # Print the received data
    print(f'Received data: "{received_data}". This will be sent to the cloud server.')
    requests.post('{}/resv_dht_data'.format(CLOUD_SERVER_URL), params={'temperatureAndHumidity': received_data})