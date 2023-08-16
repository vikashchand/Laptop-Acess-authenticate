import cv2
import time
import os
from pushbullet import PushBullet

# Your PushBullet API key
API_KEY = ""

def intruder_pic():
    cam = cv2.VideoCapture(0)
    s, im = cam.read()
    cam.release()  # Release the camera resource
    if s:
        cv2.imwrite("Intruder.bmp", im)

def image_send(pb):
    with open("Intruder.bmp", "rb") as pic:
        file_data = pb.upload_file(pic, "Intruder.bmp")
    pb.push_file(**file_data)

def log_off():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def control(pb):
    while True:
        pushes = pb.get_pushes()
        if pushes:
            action = pushes[0]['body'].lower()  # Convert to lowercase for case-insensitive comparison
            if action == 'no':
                intruder_pic()
                image_send(pb)
                time.sleep(10)
                log_off()
            elif action == 'yes':
                print("Closing the program.")
                break
        time.sleep(1)  # Avoid continuous polling, wait for a second

def main():
    pb = PushBullet(API_KEY)
    push_msg = pb.push_note("PYTHON:", "Found Internet Connectivity, is this you? If not, reply with 'No'")
    control(pb)

if __name__ == "__main__":
    main()
