import os
import sys

import cv2 as cv

from rpiasgige.client_api import Device, Performance_Counter

camera = Device("192.168.2.2", 4001)

keep_alive = True

def printf(format, *args):
    sys.stdout.write(format % args)

if not camera.ping(keep_alive):
    print("Ping camera failed.")
    os._exit(0)
else:
    print("ping worked")

if camera.isOpened(keep_alive):
    print("Camera is opened already!")
else:
    print("Camera is not opened. Trying to open now.")
    if camera.open(keep_alive):
        print("Successfully opened the camera")
    else:
        print("Failed to open the camera", file=sys.stderr)
        os._exit(0)

WIDTH = 1280
HEIGHT = 720

if not camera.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH, keep_alive):
    print("Failed to set width resolution to " + str(WIDTH), file=sys.stderr)
    os._exit(0)
else:
    print("Successfully set width resolution to " + str(WIDTH))

if not camera.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT, keep_alive):
    print("Failed to set height resolution to " + str(HEIGHT), file=sys.stderr)
    os._exit(0)
else:
    print("Successfully set height resolution to " + str(HEIGHT))

performance_counter = Performance_Counter(120)

for i in range(1000):
    ret, frame = camera.read(keep_alive)
    if not ret:
        print("failed to grab frame", file=sys.stderr)
        break
    image_size = frame.size
    if performance_counter.loop(image_size):
        printf("fps: %.1f, mean data read size: %.1f\n" , performance_counter.get_fps(), performance_counter.get_mean_data_size())

    cv.imshow("frame", frame)

    k = cv.waitKey(1)
    if k % 256 == 27:
        break

if camera.release(False):
    print("Successfully released the camera")
else:
    print("Failed to release the camera", file=sys.stderr)

