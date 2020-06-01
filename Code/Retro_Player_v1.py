import cv2
import board
import digitalio
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
import random

# set up button
from gpiozero import Button
button = Button(21)

# set up oled 
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
oled_reset = digitalio.DigitalInOut(board.D4)
retro_screen = sh1106(serial_interface=0, width=128, height=64, rotate=0, reset=oled_reset)
WIDTH = 132
HEIGHT = 64 # Change to 32 depending on your screen resolution

image = Image.new('1', (retro_screen.width, retro_screen.height))
draw = ImageDraw.Draw(image)

# video settings adjust to play smooth
frameCounter = 0
frameSkip = 1 # Change to adjust frame rate
lowerThresh = 0 # Adjust threshold according to video

time.sleep(3)

while True:
    if button.is_pressed:
        film = "/home/pi/Retro_Player/" + str(random.randrange(0,11)) +".mp4" # select a random video to display
        print (film)
        #break
        ''' if the button is pressed then change the video '''

        cap = cv2.VideoCapture(film) #Enter the name of your video in here
        print (cap)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print( length )
        #break
        time.sleep (0.2) 
    
        while(cap.isOpened()):
            ret, frame = cap.read()
            frameStart = time.time()
            if ret==True:
                if frameCounter%frameSkip == 0:
                    resized = cv2.resize(frame, (retro_screen.width, retro_screen.height))
                    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

                    # Threshold it to B&W
                    (thresh, bw) = cv2.threshold(gray, lowerThresh, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                    # Clear screen for next frame
                    draw.rectangle((0, 0, retro_screen.width, retro_screen.height),outline=0, fill=0)

                    screenframe = Image.fromarray(bw).convert("1")
                    retro_screen.display(screenframe)
                    retro_screen.show()
                    frameEnd = time.time()
                    #print(1/(frameEnd-frameStart))
                frameCounter=frameCounter+1

                # check for end of video - last frame
                length = length - 1
                if length == 0:
                    break
                else:
                    pass
    else:
        # print("Ready") only for testing but works

        # display press the ready button
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((15, 10), "  R3tr0 Pl@yer ", fill="white")
            draw.text((15, 35), "Press the button", fill="white")
            draw.text((15, 45), "to play a video", fill="white")
