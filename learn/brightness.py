# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 19:06:18 2018

@author: gin
"""

# evaluate the the  of videos'brightness   in AFEW dataset  and increase the darks

import cv2 
import numpy as np
import os


#test_video_path = '/static/afew/AFEW_DATA/Angry/Angry000046280.mp4'

test_video_path = r'C:\Users\gin\OneDrive\HCCWORK\Experiment web app\hcc workshop\learn\static\afew\AFEW_DATA\Angry\Angry000046280.mp4'


#videos_path = 'C:/Users/gin/Desktop/EmotiW_2018/Train_AFEW'
videos_path = 'C:/Users/gin/Desktop/AFEW/EmotiW_2018/Train_AFEW'
all_videos = []
for a ,b ,c in os.walk(videos_path):
    for each_file in c:
        x = os.path.join(a, each_file)
        all_videos.append(x)
        
        

def bright_evaluate_average (video_path):        
    ave_threshold = 15 * 720 * 576 * 3
    cap = cv2.VideoCapture(video_path)
    
    while(cap.isOpened()):  
        ret , frame = cap.read()         
        if frame is None:
            break    
        s = frame.sum()
        if s < ave_threshold:
            return (False, s)
        
    return (True ,s)

def bright_evaluate_topxx (video_path):  
    top_threshold = 20 * 720 * 576 * 3 / 2 
    cap = cv2.VideoCapture(video_path)
    
    while(cap.isOpened()):  
        ret , frame = cap.read()         
        if frame is None:
            break    
        frame = np.reshape(frame,(1244160))
        s = sum(frame[int(len(frame)/2):])
        if s < top_threshold:
            return (False, s)    
    return (True , s)

print(len(all_videos))


bright_top = []
dark_top = [] 
count = 1
for i in all_videos:
    if '.avi' in i:
        print(count)
        count +=1
        is_bright , value = bright_evaluate_topxx(i)
        if is_bright:
            bright_top.append((i,value))
        else:
            dark_top.append((i,value))
    else:
        print(i)
        

bright = []
dark = [] 

count = 1
for i in all_videos:
    if '.avi' in i:
        print(count)
        count +=1
        is_bright , value = bright_evaluate_topxx(i)
        if bright_evaluate_average(i)[0]:
            bright.append((i,value))
        else:
            dark.append((i,value))
    else:
        print(i)
        
#find the top xx darkest for each methods
top = 20

value = [i[1] for i in dark ]
value.sort()
value = value[:top]
x = { str(i) : j for j , i in dark }
top20_dark = [ x[str(i)]for i in value]

value = [i[1] for i in dark_top ]
value.sort()
value = value[:top]
x = { str(i) : j for j , i in dark_top }
top20_dark_top = [ x[str(i)]for i in value]   
    