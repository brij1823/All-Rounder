import json
import math
import pickle

import cv2
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import subprocess, re
from django.conf import settings
import os



#Custom Libs
import os
from moviepy.editor import *
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS 
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.editor as mpe
import pytube
from pytube import YouTube




r = sr.Recognizer()
translator = Translator()
hindi_text = ""


# Create your views here.
init_Dict = dict()
exec_Dict = dict()
exec_Dict_cricket = dict()


class Home(TemplateView):
    template_name = 'home.html'


class Temp(TemplateView):
    template_name = 'temp.html'


class Image(TemplateView):
    template_name = 'image.html'


class uploadCustom(TemplateView):
    template_name = 'videoUploadPage.html'

class videoUploadPageGym(TemplateView):
    template_name = 'videoUploadPage.html'

class videoUploadPageCricket(TemplateView):
    template_name = 'videoUploadPageBatting.html'

class ListOfActivities(TemplateView):
    template_name = 'activities.html'
class Translator(TemplateView):
    template_name = 'education.html'


    context = {'file': file_url, 'img_frag': i}
    # os.remove('media/tempy.mp4')
    return render(request,'sampleVideoGym.html', context)



@csrf_exempt
def uploadCricketVideoCustom(request):
    file = request.FILES['video']
    name = file.name.split(".")
    extension = name[-1]
    fs = FileSystemStorage()
    filename = fs.save('tempy.' + extension, file)
    file_url = fs.url(filename)
    cap = cv2.VideoCapture("media/tempy.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    total_frame = cv2.CAP_PROP_FRAME_COUNT
    length = total_frame / fps

    s_t = 0
    s_e = 10

    i = 0
     points['rightWrist']]]
    if 'leftHip' in keys and 'leftShoulder' in keys:
        graph += [[points['leftHip'], points['leftShoulder']]]
    if 'rightHip' in keys and 'rightShoulder' in keys:
        graph += [[points['rightHip'], points['rightShoulder']]]
    if 'leftHip' in keys and 'leftKnee' in keys:
        graph += [[points['leftHip'], points['leftKnee']]]
    if 'rightHip' in keys and 'rightKnee' in keys:
        graph += [[points['rightHip'], points['rightKnee']]]
    if 'leftAnkle' in keys and 'leftKnee' in keys:
        graph += [[points['leftAnkle'], points['leftKnee']]]
    if 'rightAnkle' in keys and 'rightKnee' in keys:
        graph += [[points['rightAnkle'], points['rightKnee']]]
    return graph


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calculateSlope(x1, y1, x2, y2):
    dist = (y2 - y1) / (x2 - x1)
    return dist


@csrf_exempt
def sendLooperDataGym(request):
    if request.method == 'POST':
        poses = json.loads(request.POST['upPoses'])
        no = request.POST['imageNo']
        print("-----------------------------------------------------------------")
        print("NO: " + no)
        # print("Left Ankle Co-ordinates : (" + poses.pose.keypoints[15].position.x + "," + poses[0].pose.keypoints[15].position.y+")")
        # print("Right Ankle Co-ordinates : (" + poses.pose.keypoints[16].position.x + "," + poses[0].pose.keypoints[16].position.y+")")
        p = poses[0]['pose']['keypoints']
        l = len(p)
        points = dict()
        for i in range(l):
            d = p[i]
            if d['score'] > 0:
                x, y, c = d['position']['x'], -d['position']['y'], d['score']
                points[p[i]['part']] = [x, y, c]

        user_slopes = user_slope(points)
        with open('ideal_init.pickle', 'rb') as input:
            ideal_init_slopes = pickle.load(input)
        with open('ideal_exec.pickle', 'rb') as input:
            ideal_exec_slopes = pickle.load(input)
            #  print(user_slopes,ideal_init_slopes,ideal_exec_slopes,'\n\n\n')

        sum_init = 0
        for a in ['RES', 'RHS', 'LES', 'LHS']:
            sum_init += abs(ideal_init_slopes[a] - user_slopes[a])

        sum_exec = 0
        for a in ['RES', 'RHS', 'LES', 'LHS']:
            sum_exec += abs(ideal_exec_slopes[a] - user_slopes[a])

        if (sum_exec < sum_init):
            exec_Dict[no] = dict()
            exec_Dict[no]["dist"] = sum_exec
            exec_Dict[no]["Dict"] = user_slopes
            exec_Dict[no]["Point_Dict"] = points
        else:
            init_Dict[no] = dict()
            init_Dict[no]["dist"] = sum_init
            init_Dict[no]["Dict"] = user_slopes
            init_Dict[no]["Point_Dict"] = points

        # print("------------" + "exec_Dict" + " -----------------  ")
        # print(exec_Dict)

        # print("------------" + "init_Dict" + " -----------------  ")
        # print(init_Dict)

        # plt.show()
        return HttpResponse("Working !!")
    else:
        return HttpResponse("Error")


def return_frames(request):
    ans = dict()

    global exec_Dict, init_Dict
    min_Dist = 999999
    min_exec_frame_no = -1

    ftShoulder"][1] - Temp_Dict["rightWrist"][1]) / (
            Temp_Dict["rightShoulder"][0] - Temp_Dict["rightWrist"][0])

    if (slope > 0.35):
        feedbacks.append(["Keep your right hand upward as the straight line with the shoulder"])
    elif (slope < -0.35):
        feedbacks.append(["Keep your right hand downward as the straight line with the shoulder"])

    slope = (Temp_Dict["leftShoulder"][1] - Temp_Dict["leftWrist"][1]) / (
            Temp_Dict["leftShoulder"][0] - Temp_Dict["leftWrist"][0])

    if (slope > 0.35):
        feedbacks.append(["Keep your left hand downward as the straight line with the shoulder"])
    elif (slope < -0.35):
        feedbacks.append(["Keep your left hand upward as the straight line with the shoulder"])

    return feedbacks


def gym_init_feedback(number):
    global init_Dict

    feedbacks = []
    Temp_Dict = init_Dict[number]["Point_Dict"]

    dist = math.sqrt((Temp_Dict["leftWrist"][0] - Temp_Dict["rightWrist"][0]) ** 2 + (
            Temp_Dict["leftWrist"][1] - Temp_Dict["rightWrist"][1]) ** 2)

    if (dist < 150):
        feedbacks.append(["Keep little bit more distance between wrists"])
    elif (dist > 152):
        feedbacks.append(["Keep little bit less distance between wrists"])

    return feedbacks


def user_slope(user_Dict):
    FS
        if (i != '0'):
            print("exec dict")
            print(i, exec_Dict_cricket[i]["dist"])
            if (exec_Dict_cricket[i]["dist"] < min_Dist):
                min_Dist = exec_Dict_cricket[i]["dist"]
                print(type(i) , "type")
                min_exec_frame_no = i

    # min_exec_frame_no = int(len(exec_Dict_cricket)/2)*3
    # print(exec_Dict_cricket)  # , min_exec_frame_no)
    # exec_Dict_cricket  = dict()
    return render(request,"FeedbackCricket.html", context={"exec": min_exec_frame_no, "feedback": cricket_feedback(min_exec_frame_no)})




def cricket_feedback(number):
    feedbacks = []
    # print(exec_Dict_cricket.keys())
    Temp_Dict = exec_Dict_cricket[number]['Dict']

    if (Temp_Dict['RES'] < -0.544):
        feedbacks.append(["Keep right elbow little bit downward"])
    elif (Temp_Dict['RES'] > -0.379):
        feedbacks.append(["Keep right elbow little bit upward"])
    if (Temp_Dict['RHS'] < -1.1143):
        feedbacks.append(["Create 90 degree with elbow in right hand and move hand toward your mouth little bit"])
    elif (Temp_Dict['RHS'] > -1.082):
    
        exec_Dict_cricket[no] = dict()
        exec_Dict_cricket[no]["dist"] = sum_exec
        exec_Dict_cricket[no]["Dict"] = user_slopes

        return HttpResponse("Working !!")
    else:
        return HttpResponse("Error")





def uploadVideoURL(request):
    videoURL = request.GET['videoURL']
    YouTube(videoURL).streams.first().download('C:\\brij\\personal\\hackathon\\django\\VideoTranslation\\media')
    video = VideoFileClip("C:/brij/personal/hackathon/django/VideoTranslation/media/i made this for my french class please don’t attack me.mp4")
    path = "C:/brij/personal/hackathon/django/VideoTranslation/media//vaudiofrench.wav"
    video.audio.write_audiofile(path)
    path = "C:/brij/personal/hackathon/django/VideoTranslation/media//vaudiofrench.wav"
    target = vget_large_audio_transcription(path)
    print("\nFull text:", target)
    # The text that you want to convert to audio 
    mytext = hindi_text
      
    # Language in which you want to convert 
    language = 'hi'
      
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    #myobj = gTTS(text=target, lang=language, slow=False) 
      
    # Saving the converted audio in a mp3 file named 
    # welcome  
    
    
    #myobj.save("C:/brij/personal/hackathon/django/VideoTranslation/media/vwelcome.mp3") 
      
    # Playing the converted file 
    #os.system("mpg321 vwelcome.mp3")
    #videoclip = VideoFileClip("C:/brij/personal/hackathon/django/VideoTranslation/media/i made this for my french class please don’t attack me.mp4")
   
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text




def vget_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.
    # return the text for all chunks detected
    return hindi_text