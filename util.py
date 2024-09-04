# Utility Library
import cv2
from picamera2 import Picamera2
from PIL import Image
import os
import shutil
from time import time

start_time = time()

# 디렉토리 설정
MODEL_DIR = "models/"
CAPTURED_IMAGE_DIR = "images/captured/"
DETECTED_IMAGE_DIR = "images/detected/"


# 콘솔 로그 출력 설정
console_info = "[ Info ]"
console_err = "[ Error ]"
console_send = "[ SEND ]"
console_recv = "[ RECV ]"
console_debug = "[ Debug ]"


# 카메라 미리 설정
cam = Picamera2()
cam.start_preview()
config = cam.create_still_configuration()
cam.configure(config)
cam.start()


# 사진 촬영
def takePicture(name):
    
    cam.capture_file(os.path.join(CAPTURED_IMAGE_DIR, name+".jpg"))
    

# 콘솔 타이머
def consolelog_timer():
    global start_time
    end_time = time()

    return f"[ {end_time - start_time:.2f}s ]"


# 콘솔 로그 출력
def consolelog_sender(type, message):

    print(f"{type} {consolelog_timer()} {message}.")


# 폴더 생성 함수
def createFolder(path):

    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder created: {path}")
    else:
        print(f"Folder already exists: {path}")


# 폴더 내 파일 삭제 함수
def deleteFiles(path):

    if os.path.exists(path):

        for filename in os.listdir(path):
            
            file_path = os.path.join(path, filename)
            
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                consolelog_sender(console_err, f"Failed to delete file(s) : {e}")

        consolelog_sender(console_info, f"File deleted")
        
    else:
        consolelog_sender(console_err, f"Folder does not exist: {path}")
