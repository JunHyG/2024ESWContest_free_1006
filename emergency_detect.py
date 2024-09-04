import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import os

from util import MODEL_DIR, DETECTED_IMAGE_DIR

model1_path = os.path.join(MODEL_DIR + 'h5/ambulance_classifier.h5')
model2_path = os.path.join(MODEL_DIR + 'h5/police_car_classifier.h5')

model_amb = tf.keras.models.load_model(model1_path)
model_pol = tf.keras.models.load_model(model2_path)


def emergency_car_detection():

    img_files = [f for f in os.listdir(DETECTED_IMAGE_DIR) if f.endswith('.jpg')]

    prd = []

    for i in img_files:
        img_path = os.path.join(DETECTED_IMAGE_DIR, i)

        img = image.load_img(img_path, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        img_array /= 255.0

        pred_1 = model_amb.predict(img_array)
        pred_2 = model_pol.predict(img_array)
        
        prd.append([float(pred_1.item()), float(pred_2.item())])

    return prd


def check_emergency(em_res):

    emergency = []
    
    for p in em_res:
        amb, pol = p
        emergency.append("normal" if amb > 0.5 or pol > 0.5 else "emergency")
    
    return emergency


def update_car_state(car_state, em):

    new_car_state = [state + [result] for state, result in zip(car_state, em)]
    return new_car_state
