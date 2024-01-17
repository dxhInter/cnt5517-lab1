from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import requests

PRI_IP_1 = '10.20.0.20'
PRI_IP_2 = '10.20.0.22'
CLOUD_SERVER_URL = 'http://10.20.0.9:5001'

PORT_NUMBER = 8090
SIZE = 1024
hostName = gethostbyname('0.0.0.0')
mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))


# print("Edge computer listening for input on port {}".format(PORT_NUMBER))

def judge_code(code):
    # send ok or fail to led
    if code == 200:
        mySocket.sendto("ok".encode(), PRI_IP_1)
    else:
        mySocket.sendto("fail".encode(), PRI_IP_2)


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
    code = requests.get('{}/show_data'.format(CLOUD_SERVER_URL))
    judge_code(code)
