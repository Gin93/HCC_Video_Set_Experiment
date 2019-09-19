from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

#跳转函数
from django.http import HttpResponseRedirect
from django.urls import reverse 

from .forms import Info1
from .models import historical_answer , all_info , completed_info_hcc
import numpy as np
import random 
import collections
import time
import json
from functools import reduce



dataset = 0 # default 0: HCC research group videos set;  1: AFEW videos datasets 

#Hyperparameter, to control the experiment process, mainly for testing 
quick_test = 0 # 1: play the videos directly
skip_confidence = 0 # 1 skip condifence questions
max_videos = 80
max_emotion_videos = 20

# global variables used to get access to the local variables of functions
# an elegant solution is put those temporary data into database with a fixed primary key 
# reload them when use them. 
all_global_vars = {'sequence' : [] , 'current_page' : 0 , 'videos_answer' : [],
    'user_name' : 'User', 'emo_sequence' : [] ,  'other_info' : [] , 'time_stamp' : [],
    'questions' : [], 'seen_before' : [] , 'confidence' : [] , 'personal_info' : {}
    }

sequence = []
current_page = 0
videos_answer = []
user_name = 'User'
emo_sequence = []
other_info = []
time_stamp = []
questions = []
seen_before = []
confidence = [] 
personal_info = {}



def return_emotions(emo_code):
    #case: 1: Anger 2: Happiness 3: Surpise 4: Fear
    if emo_code == '1':
        return 'Anger'
    elif emo_code == '2':
        return 'Happiness'
    elif emo_code == '3':
        return 'Surprise'
        path_emotion = 'S' # surprise
        q_emo = 'Surprise'
    elif emo_code == '4':
        return 'Fear'
        path_emotion = 'F' #fear
        q_emo = 'Fear'
        
def initialize():
    # ensure all global varibales are initialized.
    # Or initialize the those varibales via database in future 
    global current_page , videos_answer,sequence,user_name,time_stamp,other_info,emo_sequence
    current_page = 0
    videos_answer = []
    sequence = []
    user_name = 'User'
    emo_sequence = []
    other_info = []
    time_stamp = []    
    global all_global_vars
    all_global_vars = {'sequence' : [] , 'current_page' : 0 , 'videos_answer' : [],
        'user_name' : 'User', 'emo_sequence' : [] ,  'other_info' : [] , 'time_stamp' : [],
        'questions' : [], 'seen_before' : [] , 'confidence' : [] , 'personal_info' : {}
        }    
        
def generate_sequence():
    # one sequence for emotions
    # another for videos for each emotions
    emotion = np.random.permutation(range(1,5))
    videos = [np.random.permutation(range(1,21)) for i in range(4)]
    global all_global_vars
    for i in range(len(videos)):
        for j in range(len(videos[0])):
            all_global_vars['sequence'].append(str(emotion[i]) + '_' + str(videos[i][j]))
            
    emo1 = return_emotions(all_global_vars['sequence'][5][0])
    emo2 = return_emotions(all_global_vars['sequence'][25][0])
    emo3 = return_emotions(all_global_vars['sequence'][45][0])
    emo4 = return_emotions(all_global_vars['sequence'][65][0])
    all_global_vars['emo_sequence'].append (emo1)
    all_global_vars['emo_sequence'].append (emo2)
    all_global_vars['emo_sequence'].append (emo3)
    all_global_vars['emo_sequence'].append (emo4)
    print('-----------------------')
    print(all_global_vars['emo_sequence'][1])
    print('-----------------------')

def index(request):
    #接受一个request (相当于匹配到了一个url)
    #然后就返回一个template 即某一个HTML
    record = completed_info_hcc.objects.all()
    print(record)
    return render(request,'learn/index.html')

def choices(request):
    #choice page, to choose which dataset would like to use
    return render (request,'learn/dataset.html')

def intro_page(request):
    initialize()
    generate_sequence()
    global quick_test 
    if quick_test:
        return HttpResponseRedirect('emojudgement_playing')      
    global all_global_vars 
    emo1, emo2, emo3, emo4 = all_global_vars['emo_sequence']
    return render(request,'learn/Intro.html' , {'emo1': emo1 , 'emo2':emo2 , 'emo3':emo3 , 'emo4':emo4})

def intro_page2(request):
    return render(request,'learn/introtips.html')

def demo_page(request):
    return render(request,'learn/Demop.html')

def info_p1(request):
    return render(request, 'learn/survey1.html')

def info_p1_collection(request):
    global all_global_vars 
    if request.method =='POST':            
        all_global_vars['user_name'] = request.POST["Name"] if request.POST["Name"] else 'User'
        age = request.POST["Age"]
        gender = request.POST["Gender"]
        glass = request.POST["GlassesContacts"]
        all_global_vars['other_info'].append(age)
        all_global_vars['other_info'].append(gender)
        all_global_vars['other_info'].append(glass)
        all_global_vars['personal_info']['age'] = age
        all_global_vars['personal_info']['gender'] = gender
        all_global_vars['personal_info']['glass'] = glass
        
#    global dataset 
#    if dataset == 0:
    return HttpResponseRedirect('emojudgement_p004')       
#    else:
#        return HttpResponseRedirect('emojudgement_afew_p004')       


def p4(request):
    return render(request,'learn/p004.html')

def playing (request):
#    path = '<source src= {% static \'/learn/fear/videos/AF1.mp4\'%} type="video/mp4">'
#    global current_page , sequence , questions
    global all_global_vars 
#    global sequence
    try:
        emo , index = all_global_vars['sequence'][all_global_vars['current_page']].split('_')
    except:
        emo = '1' 
        index = '1'     # video_index > 10 --> acted ; 0-10 ---> genuine
    if emo == '1':
        path_emotion = 'A' #anger
        q_emo = 'Anger'
    elif emo == '2':
        path_emotion = 'H' # happiness
        q_emo = 'Happiness'
    elif emo == '3':
        path_emotion = 'S' # surprise
        q_emo = 'Surprise'
    elif emo == '4':
        path_emotion = 'F' #fear
        q_emo = 'Fear'
        
    if int (index) > 10:
        index = str (int(index) - 10) # index > 10 --> acted 
        path_authenticity = 'A'
    elif int(index) <= 10:
        path_authenticity = 'G'
        
    all_global_vars['current_page'] += 1 
    path = 'static/learn/videos/' + path_authenticity + path_emotion + index + '.mp4'
    all_global_vars['questions'].append(path)
    global max_videos 
    if all_global_vars['current_page'] >= max_videos : # finish all videos turn to survey p2 
        return HttpResponseRedirect('emojudgement_survey2')
#    global videos_answer
    all_global_vars['videos_answer'].append([path_emotion , path_authenticity])
#    global time_stamp
    all_global_vars['time_stamp'].append(str(int(time.time())))
    # in playing.html action='emojudgement_save_authenticity'
    return render(request,'learn/playing.html',{'path': path , 'emo':q_emo , 'count' :all_global_vars['current_page']})


def save_authenticity (request):
    global all_global_vars
    if request.method =='POST':
        authenticity = request.POST["authenticity"]
#        global videos_answer
        all_global_vars['videos_answer'][-1].append(authenticity)
#        global time_stamp
        all_global_vars['time_stamp'].append('-')
        all_global_vars['time_stamp'].append(str(int(time.time())))        
        print(all_global_vars['videos_answer'])       
#        if request.POST.has_key('continue'):
        global skip_confidence 
        if skip_confidence:
            return HttpResponseRedirect('emojudgement_playing')
        return HttpResponseRedirect('emojudgement_confidence')

def confidence (request):
    #render the condifence html file 
    return render (request, 'learn/confidence.html')
    
def savecondifence (request):
    # save the condifence data and redirect to playing.html 
    # check point, for per 20 videos, user can decide to save and quit or continue 
    # that is for each 20 videos, jump the choice page.
#    global seen_before , confidence
    global all_global_vars
    if request.method =='POST':
        con_level = request.POST["Option"]
        seen = request.POST["Unknown/Known"]
        all_global_vars['seen_before'].append(seen)
        all_global_vars['confidence'].append(con_level)
    keys = list(request.POST)
    print(keys)
    if 'continue' in keys:   
#        return HttpResponseRedirect('/confidence')
        pass
    if 'end' in keys:
        print('the second button do something')
        return HttpResponseRedirect('emojudgement_survey2')
    normal = 1 
    global current_page , emo_sequence
    print(all_global_vars['current_page'])
    if (all_global_vars['current_page']) == 20:
        normal = 0
    if (all_global_vars['current_page']) == 40:
        normal = 0
        emo_sequence.pop(0)
    if (all_global_vars['current_page']) == 60:
        normal = 0
        emo_sequence.pop(0)
    if normal:
        return HttpResponseRedirect('emojudgement_playing') 
    else:
        return HttpResponseRedirect('emojudgement_continueskip') 

def breakpage (request):
#    global emo_sequence
    global all_global_vars
    current_emo = all_global_vars['emo_sequence'][0]
    next_emo = all_global_vars['emo_sequence'][1]
    return render (request,'learn/breakorskip.html',{'next_emo' : next_emo , 'current_emo' :current_emo}) 
    


def info_collection_p2(request):
    return render(request, 'learn/survey2.html')

def info2_add(request):
    if request.method =='POST':
        Ethnicity = request.POST["Ethnicity"]
        Language = request.POST["Language"]
        OtherLanguage = request.POST["OtherLanguage"]
    global all_global_vars    
#    global other_info , personal_info
    all_global_vars['other_info'].append(Ethnicity)
    all_global_vars['other_info'].append(Language)
    all_global_vars['other_info'].append(OtherLanguage)
    all_global_vars['personal_info']['ethnicity'] = Ethnicity
    all_global_vars['personal_info']['Language'] = [Language,OtherLanguage]

    return HttpResponseRedirect('emojudgement_Conclusion/result')         

def end(request):
    return render (request,'learn/Conclusion.html')

def cal_accuracy(correct,count):
    try:
        return format (correct/count , '.0%')
        print(correct,count)
    except ZeroDivisionError:
        print(correct,count)
        return 'N/A'
    
def result_display(request):
    #analyze and display the result
#    return HttpResponse('hello world')
    global all_global_vars
    all_global_vars['user_name'] += '\'s'
    print(all_global_vars['videos_answer'])
    print(all_global_vars['user_name'])
    h_count = f_count = a_count = s_count = 0
    h_correct = f_correct = a_correct = s_correct = 0
    output = collections.defaultdict(lambda : 0)
    
    #count the correct and incorrect answers 
    for emo,actual,answer in all_global_vars['videos_answer']:
        if emo == 'H':
            output ['h_count'] += 1 
            if actual == answer:
                output['h_correct'] += 1              
        elif emo == 'F':
            output['f_count'] += 1
            if actual == answer:
                output['f_correct'] += 1 
        elif emo == 'A':
            output['a_count'] += 1
            if actual == answer:
                output['a_correct'] += 1
        elif emo == 'S':
            output['s_count'] += 1
            if actual == answer:
                output['s_correct'] += 1 
                
#    user_name = 'Kevin\'s'
    # get the accuracy 
    smile_accuracy = cal_accuracy (output['h_correct'] , output['h_count'])
    anger_accuracy = cal_accuracy (output['a_correct'] , output['a_count'])
    fear_accuracy = cal_accuracy (output['f_correct'] , output['f_count'])
    suprise_accuracy = cal_accuracy (output['s_correct'] , output['s_count'])
    

    # read the privous answers and cal the average accuracy 
    # filter out test datauser_name == test 
    record = historical_answer.objects.all().values('answer')
#    record = historical_answer.objects.exclude(name = 'test').values('answer')
    if record:
        historical_count = [collections.Counter(json.loads (i['answer'])) for i in record]
        historical_count_total = reduce(lambda x,y:x+y,historical_count)
    print(historical_count_total)            
    smile_accuracy_average = cal_accuracy (historical_count_total['h_correct'] , historical_count_total['h_count'])
    anger_accuracy_average = cal_accuracy (historical_count_total['a_correct'] , historical_count_total['a_count'])
    fear_accuracy_average = cal_accuracy (historical_count_total['f_correct'] , historical_count_total['f_count'])
    suprise_accuracy_average = cal_accuracy (historical_count_total['s_correct'] , historical_count_total['s_count'])            
    
    #save this participant's data into database 
    historical_answer.objects.create(
        date_id = int(time.time()),
        answer = json.dumps(output),
        name = all_global_vars['user_name'][:-2]
    )
    
    #save this participant's data into database 
    try:
        print('all info:')
        print(output)
        print(all_global_vars['user_name'][:-2])
        print(all_global_vars['other_info'])
        print(all_global_vars['time_stamp'])
        print(all_global_vars)
        all_info.objects.create(
            date_id = int(time.time()),
            answer = json.dumps(output),
            name = all_global_vars['user_name'][:-2],
            other_info = json.dumps(all_global_vars['other_info']),
            time_stamp = json.dumps(all_global_vars['time_stamp'])
        )
    except Exception as e:
        print(e)
        try:
            f = open('C:/workshop/' + str(int(time.time())) + '.txt','w')
            f.writelines(all_global_vars['user_name'][:-2])
            f.writelines(';')  
            for i in all_global_vars['other_info']:
                f.writelines(i)    
                f.writelines(',')  
            f.writelines(';')  
            for i in all_global_vars['videos_answer']:
                f.writelines(i)
                f.writelines(',')  
            f.writelines(';')  
            for i in time_stamp:
                f.writelines(i)  
                f.writelines(',')  
            f.close()
        except Exception as e:
            print('save falied')
            print(e)
#            print('save falied')
    
    try:
        all_info.objects.create(
                date_id = int(time.time()),
                name = user_name[:-2],
                other_info = json.dumps(other_info),
                time_stamp = json.dumps(time_stamp)
        )
    except Exception as e:
        print(e)
            
    return render (request,'learn/results.html',{'name':all_global_vars['user_name'] , 'smile':smile_accuracy , 
                   'anger': anger_accuracy , 'fear': fear_accuracy , 'surprise':suprise_accuracy,
                   'smile_ave' : smile_accuracy_average , 'anger_ave': anger_accuracy_average ,
                   'fear_ave' : fear_accuracy_average , 'surprise_ave': suprise_accuracy_average } )
    
def databasedisplay(request):
    # dataset admin page, to show the data stored in the database
    record = all_info.objects.all()
    print(record)
    return render(request,'learn/datadisplay.html',{'records':record})



    
    
#def test_page(request):
    
    
#def databasedisplay(request):
#    record = all_info.objects.all()
##    record1 = all_info.objects.filter(name = 'test')
#    xx = []
#    for i in record:
#        x = []
#        x.append(i.date_id)
#        x.append(i.name)
#        x.append(i.other_info)
##        x.append(json.loads (i['answer']))
#        x.append(json.loads (i.answer))
#        
#        xx.append(x)
#    print(xx)
#    return HttpResponse (xx)

#def table(request):
#    table_form=forms.SignupForm()   #样式 ，在forms.py里配置好了
#    record = all_info.objects.all()
#    return render_to_response("learn/datadisplay.html",locals()) #必须用这个return
    
#    return HttpResponse('Happiness correct: ' + str(output['h_correct']) + ' out of '+ str(output['h_count']) + '\n ')
#                        'Fear correct: ' + str(f_correct) + ' out of '+ str(f_count) + '\n ' +
#                        'Anger correct: ' + str(a_correct) + ' out of '+ str(a_count) + '\n ' +
#                        'Surprise correct: ' + str(s_correct) + ' out of '+ str(s_count) )
                

#def old_add2_redirect(request, a, b):
#    return HttpResponseRedirect(
#        reverse('add2', args=(a, b))
#    )
#    
#def add(request):
#    a = request.GET['a']
#    b = request.GET['b']
#    c = int(a)+int(b)
#    return HttpResponse(str(c))
#
#def add2(request, a, b):
#    c = int(a) + int(b)
#    return HttpResponse(str(c))

#def result_display(request):
#    #analyze and display the result
##    return HttpResponse('hello world')
#    global videos_answer
#    print(videos_answer)
#    h_count = f_count = a_count = s_count = 0
#    h_correct = f_correct = a_correct = s_correct = 0
#    for emo,actual,answer in videos_answer:
#        if emo == 'H':
#            h_count += 1 
#            if actual == answer:
#                h_correct += 1              
#        elif emo == 'F':
#            f_count += 1
#            if actual == answer:
#                f_correct += 1 
#        elif emo == 'A':
#            a_count += 1
#            if actual == answer:
#                a_correct += 1
#        elif emo == 'S':
#            s_count += 1
#            if actual == answer:
#                s_correct += 1 
#                
#    return HttpResponse('Happiness correct: ' + str(h_correct) + ' out of '+ str(h_count) + '\n ' +
#                        'Fear correct: ' + str(f_correct) + ' out of '+ str(f_count) + '\n ' +
#                        'Anger correct: ' + str(a_correct) + ' out of '+ str(a_count) + '\n ' +
#                        'Surprise correct: ' + str(s_correct) + ' out of '+ str(s_count) )
    

#                
##    context = { 'list_var' : videos_answer }
##    return render (request, 'learn/list.html', context)
#def info_collection_p1(request):
#    if request.method == 'POST':
#        # create a form instance and populate it with data from the request:
#        form = Info1(request.POST)
#        # check whether it's valid:
#        global other_info
#        if form.is_valid():
#            age = form.cleaned_data['Age']
#            sex = form.cleaned_data['sex']
#            glasses = form.cleaned_data['glasses']
#            # process the data in form.cleaned_data as required
#            # ...
#            # redirect to a new URL:
##            return HttpResponse([sex,glasses])
#            
#            other_info.append(sex)
#            other_info.append(glasses)
#            print(other_info)
#            return HttpResponseRedirect('emojudgement_info2')
#
#    # if a GET (or any other method) we'll create a blank form
#    else:
#        form = Info1()
#
#    return render(request, 'learn/survey1.html', {'form': form})