#!/usr/bin/python
import os
import cv2
import sys
import time
import wave
import pyaudio
import threading
import PIL.Image as Image
from .video_data import FOLDER_PATH, FINAL_AUDIO_PATH, FINAL_VIDEO_PATH, generate_input_data


ASCII_SCALE = "@%#*+=-:. "
ASCII_SCALE = ASCII_SCALE[::-1]
DEFAULT_TERMINAL_SIZE = (os.get_terminal_size().columns, os.get_terminal_size().lines)



def resize_image(frame:Image, reduce=3):
    weight = frame.width
    height = frame.height
    weight //= (reduce  - 2)
    height //= reduce
    return frame.resize((int(weight), int(height)))

def is_unix():
    platform = str(sys.platform).lower()
    return 'linux' in platform or 'darwin' in platform 

def pixel_to_ascii(frame):
    pixels = frame.getdata()
    ascii = ""
    for pixel in pixels:
        ascii += ASCII_SCALE[(pixel // 28) % len(ASCII_SCALE)]
    return ascii


def convertImage(image):
    ascii_image = pixel_to_ascii(image)

    image_width = image.width
    image_length = len(ascii_image)
    
    final_image = ""
    for pixel in range(0, image_length, image_width):
        final_image += ascii_image[pixel:pixel+image_width].ljust(10) + '\n'
    
    return final_image


def start_bad_apple():
    wf = wave.open(FINAL_AUDIO_PATH, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    frames_per_buffer=4096,
                    output = True)
   
    succes = True
    video = cv2.VideoCapture(FINAL_VIDEO_PATH)
    fps = video.get(cv2.CAP_PROP_FPS)
    fps = fps or 30
    timeDelta = 1./fps
    chunk = int(wf.getframerate() / fps)
    data = wf.readframes(chunk)
    while succes and data != '':
        timeProces0 = time.process_time()
        succes, frame = video.read()
        if not succes:
            break
        stream.write(data)
        data = wf.readframes(chunk)
        if is_unix():   
            sys.stdout.write('\u001b[0;0H')
        else:
            sys.stdout.write('"\x1b[0;0H")')
        
        current_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        current_frame = resize_image(current_frame, 5)
        final_image = convertImage(current_frame)
        timeProces1 = time.process_time()

        timeFrame = timeDelta - (timeProces1 - timeProces0)
        if timeFrame > 0:
            time.sleep(timeFrame)
        sys.stdout.write(final_image + '\n')

    stream.close()
    p.terminate()
    sys.stdout.write('bad apple finished')



