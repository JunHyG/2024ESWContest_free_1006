import cv2
import numpy as np
import time

def calculate_center(rect):
    _, x1, y1, x2, y2 = rect
    return (x1 + x2) // 2, (y1 + y2) // 2

def check_car_state(data1, data2, image_width):

    def determine_car_state(current_rects, previous_rects, mid_x):
        
        threshold = 50
        states = []

        for idx, rect in enumerate(current_rects):
            center_x, center_y = calculate_center(rect)
            direction = "right" if center_x > mid_x else "left"

            if idx < len(previous_rects):
                prev_center_x, prev_center_y = calculate_center(previous_rects[idx])
                movement = np.hypot(center_x - prev_center_x, center_y - prev_center_y)

                state_status = "moving" if movement > threshold else "stopped"
            else:

                state_status = "unknown"

            states.append([direction, state_status])

        return states

    mid_x = image_width // 2
    car_state = determine_car_state(data2, data1, mid_x)

    return car_state
    

