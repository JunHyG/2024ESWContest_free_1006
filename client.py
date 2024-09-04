import socket
import json
from time import sleep
from server_util import get_car_state
from util import takePicture, createFolder, deleteFiles, consolelog_sender
from util import MODEL_DIR, CAPTURED_IMAGE_DIR, DETECTED_IMAGE_DIR, console_info, console_err, console_send, console_recv, console_debug
from led_control import led_control
host = '10.42.0.1'  
port = 12345           

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))


try:
    consolelog_sender(console_info, " Connected to server")

    while True:

        client_car_state = []

        # Get Client Car State from Function
        client_car_state = get_car_state()


        # Send client_car_state
        consolelog_sender(console_info, "Sending client_car_state to the server")
        client_json = json.dumps(client_car_state)
        client_socket.sendall(client_json.encode('utf-8'))


        # delay for 0.1s
        sleep(1)
        
    
        # Recv LED data from server
        consolelog_sender(console_info, "Waiting for the server message . . .")
        client_lights = client_socket.recv(1024).decode("UTF-8")

        
        # client_lights value into c_lights
        if client_lights == "True":
            c_lights = True
            
        else:
            c_lights = False


        # LED control
        consolelog_sender(console_info, "Client : Turning on the LED" if c_lights else "Client : Turning off the LED")
        led_control(c_lights)
        
        
        # delay for 0.1s
        sleep(0.1)


finally:

    client_socket.close()
    consolelog_sender(console_info, "Connection Lost")
