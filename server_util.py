from vehicle_detect import vehicle_detection
from car_status import check_car_state
from emergency_detect import emergency_car_detection, check_emergency, update_car_state
from util import takePicture, createFolder, deleteFiles, consolelog_sender
from util import MODEL_DIR, CAPTURED_IMAGE_DIR, DETECTED_IMAGE_DIR, console_info, console_err, console_send, console_recv, console_debug

from time import sleep

def get_car_state():

    # Take Pictures
    consolelog_sender(console_info, "server_util - Take Pictures")

    takePicture("image1")
    sleep(0.1)
    takePicture("image2")


    # Detecting Car(s)
    consolelog_sender(console_info, "server_util - Detecting Car(s)")

    data1 = vehicle_detection("image1.jpg")
    deleteFiles(DETECTED_IMAGE_DIR)
    data2 = vehicle_detection("image2.jpg")


    # Check Car Status
    consolelog_sender(console_info, "server_util - Check Car Status")

    car_state = check_car_state(data1, data2, image_width=4000) # image width, need it to find middle of image


    # Detecting Emergency Car(s)
    consolelog_sender(console_info, "server_util - Detecting Emergency Car(s)")

    final_car_state = update_car_state(car_state, check_emergency(emergency_car_detection()))
    deleteFiles(DETECTED_IMAGE_DIR)


    # return
    consolelog_sender(console_info, f"server_util - state = {final_car_state}")
    return final_car_state 
