# Traffic Algorithm for Traffic Lights
import time


def is_opposite_left_car_stopped(opposite_car_state): # is opposite left car is all stopped?

    for car in opposite_car_state:
        if car[0] == "left" and car[1] == "moving":
            return False

    return True


def is_emergency_vehicle(server_car_state, client_car_state): # is emergency vehicle on left side?
    
    for car in server_car_state:
        if car[0] == "left" and car[2] == "emergency":
            return "server"
    
    for car in client_car_state:
        if car[0] == "left" and car[2] == "emergency":
            return "client"
    
    return "nothing"


def is_left_car_not_exist(server_car_state, client_car_state): # is car not exist? return value is "to be on"

    if server_car_state != [] and all(car[0] != "left" for car in server_car_state):
        return "client" # server has no left car, so returns client
    
    if client_car_state != [] and all(car[0] != "left" for car in client_car_state):
        return "server"
    
    return "nothing"


to_be_on = None
last_to_be_on = None
is_check_algorithm = True
start_time = time.time()
LIMIT_TIME_PER_TFL = 30

def trafficlights_algorithm(server_car_state, client_car_state):
    global to_be_on, last_to_be_on, is_check_algorithm, start_time, LIMIT_TIME_PER_TFL
    
    if is_check_algorithm:

        em_side = is_emergency_vehicle(server_car_state, client_car_state) # emergency state checker

        if em_side != "nothing":
            
            to_be_on = em_side
        
        else :

            ex_side = is_left_car_not_exist(server_car_state, client_car_state) # no car state checker 

            if ex_side != "nothing":
            
                to_be_on = ex_side

            else :

                end_time = time.time()

                if (end_time-start_time) > LIMIT_TIME_PER_TFL: # time checker

                    to_be_on = "client" if to_be_on == "server" else "server"
        
        # if last to be on is same as now, just return current state
        if last_to_be_on == to_be_on:
            last_to_be_on = to_be_on
            return True if to_be_on == "server" else False, False if to_be_on == "server" else True

        last_to_be_on = to_be_on
        is_check_algorithm = False


    # not using if-else cause this one should run next to above
    if not is_check_algorithm :
        
        oppo_to_be_on_car_state = client_car_state if to_be_on == "server" else server_car_state
        
        if is_opposite_left_car_stopped(oppo_to_be_on_car_state):
            is_check_algorithm = True
            start_time = time.time()
            return True if to_be_on == "server" else False, False if to_be_on == "server" else True
        
        else:
            return False, False









