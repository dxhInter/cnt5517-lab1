import json
import socket

# Get IP address of the RaspberryPi
IP = "10.20.0.58"
# The port where Atlas IoT is running
PORT = 6668


# This function generates a json message as per the provided service name,
# entity ID and inputs, if any. Returns a stringified JSON message.
def generate_message(service_name: str, entity_id: str, inputs=()):
    message = {
        "Tweet Type": "Service call",
        "Service Name": '{}'.format(service_name),
        "Thing ID": "g6",
        "Entity ID": '{}'.format(entity_id),
        "Space ID": "g6Space",
    }

    if inputs is not None:
        message["Service Inputs"] = '{}'.format(inputs).replace(', ', ',')

    return json.dumps(message)


# Sends the service call to the Atlas IoT socket. Creates a TCP socket,
# gets the generated message, sends and waits for the response.
def send_service_call(service_name: str, entity_id: str, inputs=None, ):
    # Get the message
    message = generate_message(service_name, entity_id, inputs)
    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    s.connect((IP, PORT))
    # Send data through the socket
    s.sendall(bytes(message, 'utf-8'))
    # Receive the response
    data = s.recv(1024)
    # Close the socket
    s.close()

    # Return the decoded JSON response
    return True, json.loads(data.decode())