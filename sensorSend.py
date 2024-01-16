from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import requests

PRI_IP_1 = '10.20.0.20'
CLOUD_SERVER_URL = 'http://127.0.0.1:5001'

PORT_NUMBER = 8090
SIZE = 1024
hostName = gethostbyname('0.0.0.0')
mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))
# print("Edge computer listening for input on port {}".format(PORT_NUMBER))

while True:
    # Receiving data from the Sensor DHT11.
    (data, addr) = mySocket.recvfrom(SIZE)
    # Decoding the byte[] from the socket
    received_data = data.decode()
    # Print the received data
    print(f'Received data: "{received_data}". This will be sent to the cloud server.')
    try:
        temperature, humidity = received_data.split('+')
        temperature = float(temperature)
        humidity = float(humidity)
    except ValueError:
        print("Received data is not in the expected format.")
        continue
        # create a dictionary to send to cloud server
    data_to_send = {
        'temperature': temperature,
        'humidity': humidity
    }
    # send a request to cloud server
    requests.post('{}/resv_dht_data'.format(CLOUD_SERVER_URL), json=data_to_send)