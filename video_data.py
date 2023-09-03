#!/usr/bin/python
import os
import pydub
import time
from shutil import move 
from pytube import YouTube

BAD_APPLE = 'https://youtu.be/FtutLA63Cp8?si=DipiIyUFHv7mnHo4'
DATA_FOLDER = 'data'
INPUTS_NAME = 'bad_apple'
FOLDER_PATH = os.path.join(os.getcwd(), DATA_FOLDER)
FINAL_VIDEO_PATH = os.path.join(FOLDER_PATH, "{}.mp4".format(INPUTS_NAME) )
FINAL_AUDIO_PATH = os.path.join(FOLDER_PATH, "{}_audio.wav".format(INPUTS_NAME))
TEMPORAL_AUDIO_PATH = FINAL_AUDIO_PATH.replace('.wav', '.mp4')


def generate_input_data():
    
    if not os.path.exists(FOLDER_PATH):
        try:
            os.mkdir(DATA_FOLDER)
        except Exception as error:
            print(str(error))
            raise ValueError('Cant create {} because {}'.format(DATA_FOLDER, str(error)))
    

    if not os.path.exists(FINAL_VIDEO_PATH):
        try:
            yt_video = YouTube(BAD_APPLE).streams.filter(progressive=True,mime_type='video/mp4').order_by('resolution')
            if len(yt_video):
                yt_video = yt_video[-1]
            print('Downloading... {}  Video'.format(yt_video.title))

            yt_video.download(FOLDER_PATH, filename="{}.mp4".format(INPUTS_NAME))        

            print('Video Download Complete')
        except Exception as error:
            print(str(error))
            raise ValueError('Cant download {} video {}'.format(INPUTS_NAME, str(error)))
        
    
    # print(TEMPORAL_AUDIO_PATH)
    if not os.path.exists(FINAL_AUDIO_PATH):
        try:
            yt_audio = YouTube(BAD_APPLE).streams.filter(mime_type='audio/mp4').order_by('abr')
            print('Downloading... {} Audio'.format(INPUTS_NAME))
            if len(yt_audio):
                yt_audio = yt_audio[-1]
            yt_audio.download(FOLDER_PATH, filename="{}_audio.mp4".format(INPUTS_NAME))
            print('Audio Download Complete')
           
        except Exception as error:
            print(str(error))
            raise ValueError('Cant download {} audio {}'.format(INPUTS_NAME, str(error)))
    # time.sleep(1)
    if os.path.exists(TEMPORAL_AUDIO_PATH):
            print('Converting Audio to WAV...')
            sound = pydub.AudioSegment.from_file(TEMPORAL_AUDIO_PATH, format='mp4')
            sound.export(FINAL_AUDIO_PATH, format="wav")
            if os.path.exists(FINAL_AUDIO_PATH):
                try:
                    os.remove(TEMPORAL_AUDIO_PATH)
                except:
                    print('Cant delete {}'.format(TEMPORAL_AUDIO_PATH))
                print('Audio Conversion Finished')

# def get_freame_list():
#     return [
#     str(frame) 
#     for frame in os.listdir(FOLDER_PATH)
#     if '.jpg' in frame
#     ]

# def extract_frames():
#     generate_input_data()
#     if not get_freame_list():
#         print('Extracting Frames...')
#         video = cv2.VideoCapture(FINAL_VIDEO_PATH)
#         fps = video.get(cv2.CAP_PROP_FPS)
#         success = True
#         index = 0
#         while success:
#             success, frame = video.read()
#             try:
#                 print('Extracting frame #{}'.format(index))
#                 cv2.imwrite(os.path.join(FOLDER_PATH, '{}.jpg'.format(index)), frame)
#                 index += 1
#             except:
#                 print('the frame{}.jpg cant be writed'.format(index))



