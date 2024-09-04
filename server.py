import socket
import json
from time import sleep
from server_util import get_car_state
from util import takePicture, createFolder, deleteFiles, consolelog_sender
from util import MODEL_DIR, CAPTURED_IMAGE_DIR, DETECTED_IMAGE_DIR, console_info, console_err, console_send, console_recv, console_debug
from traffic_algorithm import trafficlights_algorithm
from led_control import led_control


host = '0.0.0.0'  
port = 12345      

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(1)

client_socket, client_address = server_socket.accept()


try:
    consolelog_sender(console_info, " Client Connected")

    while True:
        
        server_car_state = []
       
        # Get Server Car State from Function
        server_car_state = get_car_state()


        # Recv client_car_state from client
        consolelog_sender(console_info, "Waiting for the client message . . .")
        client_data = client_socket.recv(1024)
        client_car_state = json.loads(client_data.decode('utf-8'))
        consolelog_sender(console_info, f"client car state - {client_car_state}")

    
        # Traffic Algorithm
        consolelog_sender(console_info, "Finished Traffic Lights Algorithm")
        server_lights, client_lights = trafficlights_algorithm(server_car_state, client_car_state)
        
        
        # Delay for 0.1s
        sleep(0.1)
        
            
        # Send LED info
        consolelog_sender(console_info, "Sending LED_info to the client")
        client_socket.send(str(client_lights).encode("UTF-8"))


        # LED control
        consolelog_sender(console_info, "Server : Turning on the LED" if server_lights else "Server : Turning off the LED")
        consolelog_sender(console_info, "Client : Turning on the LED" if client_lights else "Client : Turning off the LED")

        led_control(server_lights)
        
        sleep(0.1)

finally:

    client_socket.close()
    server_socket.close()
    consolelog_sender(console_info, "Connection Lost")

