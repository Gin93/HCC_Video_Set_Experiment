from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.urls import reverse 

from .forms import Info1
import numpy as np
import random 
import collections
from .models import sessions , person_full_set , afew_experiment_session
import time
import json
from functools import reduce
import os 
import itertools 

all_global_vars = {}
emotion_types = ['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']

quick_test = 0 # 1: play the videos directly
skip_confidence = 0 # 1 skip condifence questions
test = 0
        
def delete_everything(table):
    table.objects.all().delete()
    
def all_files(path):
    all_videos_name = []
    all_videos_path = []
    for a ,b ,c in os.walk(path):
        for each_file in c:
            all_videos_name.append(each_file)
            x = os.path.join(a, each_file)
            all_videos_path.append(x)    
    return all_videos_name , all_videos_path
    
def shuffle_all_videos(videos ,amount_videos_each_group, emotion_types):
    #Seperate all videos to x sessions randomly 
    #new feature: keep the same class video together 
    #Not completely randomly, make sure that each group has a reasonable proportion of all types of videos
    #return a list, each element is a session (group of videos)
    last_emo = ''
    classified_videos = []
    for i in videos:
        cur_emo = i[:4]
        if cur_emo != last_emo:
            classified_videos.append([])
            classified_videos[-1].append(i)
        else:
            classified_videos[-1].append(i)
        last_emo = cur_emo
    # now, classified_videos: [[videos_class1],[videos_class2]]
    # randomize at here, shuffle videos sequence for each class, and also shuffle the videos class sequence 
    print(classified_videos)
    random.shuffle(classified_videos)
    for i ,ele in enumerate (classified_videos):
        random.shuffle(classified_videos[i])
    print('x' * 200)
    print(classified_videos)
    lens = len(videos)
    groups = int ( lens / amount_videos_each_group) + 1 
    percentage = [ int (len(i) / lens * amount_videos_each_group) for i in classified_videos]
    balanced_sequences = []
    for i in range (0,groups): # for each group, create a empty list first, then add videos into this list one class by one  
        balanced_sequences.append([])
        for j , amount in enumerate (percentage):
            for m in range(0,amount):
                if classified_videos[j]:
                    balanced_sequences[-1].append(classified_videos[j].pop())
                else:
                    pass
                    
    rest = sum(classified_videos,[]) # need to, address the class, and insert them to the appropriate position rather than the end of the last set  
#    balanced_sequences[-1] += rest
    while rest:
        cur_video = rest.pop()
        video_class = cur_video[:4]
        for i, ele in enumerate (balanced_sequences[-1]):
            if ele[:4] == video_class: # insert 
                balanced_sequences[-1].insert(i,cur_video)
                break 
    print('a' * 100)
    print(rest)
        
#    for i , ele in enumerate (balanced_sequences):
#        random.shuffle(balanced_sequences[i])
    return balanced_sequences
            
def session_generator_mixed():
    #fetch a unused seesion, if all used, create n/x and save to database
    #if any session is valid, fetch and set it watched
    global all_global_vars , emotion_types
    all_global_vars['is_full_dataset'] = False # True means play a specfica type of emotion ; False means mixed up 
#    record = sessions.objects.all()
    all_unwatched_sessions = sessions.objects.filter(is_watched = False) #try to fetch a unwatched session
    if all_unwatched_sessions: # not empty, then randomly choose one and set this one as watched 
#        print(all_unwatched_sessions)
        all_global_vars['other_vars']['session_id'] = all_unwatched_sessions[0].session_id
        all_videos = all_unwatched_sessions[0].video_set #input is text() type, so output is the same type, need to decode that.
        all_videos = all_videos.replace('[','') # should use json.dump 
        all_videos = all_videos.replace(']','')
        all_videos = all_videos.replace('\'','')
        all_videos = all_videos.replace(' ','')
        all_global_vars['video_sequence'] = all_videos.split(',')
    else:# all watched or empty, create a new m/x sessions, leave one and set it watched then save all to table sessiosn 
        #primary key, start from 1 
        video_path = os.getcwd() + '/learn/static/afew/AFEW_DATA'
        all_videos = all_files(video_path)[0]  
        all_new_sessions = shuffle_all_videos(all_videos ,100, emotion_types)     
        all_global_vars['video_sequence'] = all_new_sessions[0] # take the first set as for this experiment       
        # save all sessions into the database // DO NOT FORGET TO TRACK THE SESSION ID AND SWITCH THIS SESSION AS WATCHED AT THE END OF THIS EXPERIMENT 
        # session_id is the primary key, x_y , x is the x th full sets, y is y th sessions for a full set
        all_id = sessions.objects.all().values("session_id") # queryset type 
        
        if not all_id: # empty, then set the set id as 1
            max_set_id = 1
        else: # not empty, find the max value, then set the current set id as max + 1 
            a = [int(i['session_id'].split('_')[0]) for i in all_id]
            max_set_id = str(max(a)+1)
        for i in range(len(all_new_sessions)):
            sessions.objects.create(
                session_id = str(max_set_id) + '_' + str(i+1),
                is_watched = False,
                video_set = all_new_sessions[i]
                )       
        all_global_vars['other_vars']['session_id'] = max_set_id + '_' + '1' # remeber the session_id 
    
def session_generator_entire_class():
    # return a session which contain a video set of a specific emotion class
    # First time for this subject: create profile (table_person_full_set), UID is the primary key, return one emotion randomly, then generate and return a sequence for this class randomly
    # Not first time for this subject: fetch a UNWATCHED class of emotion from the table person_full_set, then generate and return a sequence for this class randomly
    # Need to record the returned class of emotion, modify this as WATCHED in the database 
    global emotion_types
    global all_global_vars
    all_global_vars['is_full_dataset'] = True # default is false 
    subject_id = all_global_vars['personal_info']['uid']
    subjects_record = person_full_set.objects.filter(uid = subject_id)
    # first part is getting the class of emotion for this session 
    if subjects_record: # fetch a unwatched one 
        emotion_info = json.loads(subjects_record[0].emotions_if_watched)
        for emotion in emotion_info:
            if emotion_info[emotion] == False:
                emotion_class = emotion
                all_global_vars['other_vars']['emotion_class'] = emotion_class # save for set this as unwatched later 
                break 
            else:
                print('this subject has wathced all the videos of afew dataset')
        pass
    else: # new , and pick one randomly, then save all to databse 
        random.shuffle(emotion_types)
        all_unwatched_initialization = {i: False for i in emotion_types}
        person_full_set.objects.create(
                uid = subject_id,
                emotions_if_watched = json.dumps(all_unwatched_initialization))
        emotion_class = emotion_types[0] # shuffled, pick the first one = randomly choose one 
        all_global_vars['other_vars']['emotion_class'] = emotion_class # save for set this as unwatched later 

    
    video_path = os.getcwd() + '/learn/static/afew/AFEW_DATA/' + emotion_class
    all_videos = all_files(video_path)[0]
    random.shuffle(all_videos)
    all_global_vars['video_sequence'] = all_videos
    print (all_global_vars['video_sequence'])
       
    
def video_display_choice(request):

    global all_global_vars # initialize all tem vars
    all_global_vars = {'video_sequence' : [] , 'current_page' : -1 , 'videos_answer' : [], 'erq_answer' : [],
        'user_name' : 'User',  'time_stamp' : [], 'seen_before' : [] , 'confidence' : [] , 'personal_info' : {} , 'is_full_dataset' : False  , 'other_vars' : {'submission process' : 'playing'}
        }
    
    return render(request,'afew/videoset.html')

def initialization(request,videos_set):
    print(videos_set)
    if videos_set == 1:
#        session_generator_entire_class()
        all_global_vars['is_full_dataset'] = True # default is false # do the generation later // maybe need to refactor later 
    elif videos_set == 2:#mixed_up
        session_generator_mixed()
        
    global quick_test  # used for testing 
    if quick_test:
        return HttpResponseRedirect('emojudgement_AFEW_play')  
    return HttpResponseRedirect('emojudgement_AFEW_intro')      

def intro_afew(request):  
    return render(request,'afew/Intro.html')

def intro_page2(request):
    return render(request,'afew/introtips.html')

def demo_page(request):
    return render(request,'afew/Demop.html')

def info_p1(request):
    return render(request, 'afew/survey1.html')

def info_p1_collection(request):
    global all_global_vars 
    if request.method =='POST':            
        all_global_vars['user_name'] = request.POST["Name"] if request.POST["Name"] else 'User'
        age = request.POST["Age"]
        gender = request.POST["Gender"]
        glass = request.POST["GlassesContacts"]
        uid = request.POST["UID"] if request.POST['UID'] else str(int (time.time())) # if they leave the uid, use the date as the UID, it's unique, so can be a primary key
        uid=uid.replace('u','')
        uid=int(uid.replace('U',''))
        all_global_vars['personal_info']['age'] = age
        all_global_vars['personal_info']['gender'] = gender
        all_global_vars['personal_info']['glass'] = glass
        all_global_vars['personal_info']['uid'] = uid
        if all_global_vars['is_full_dataset']: # not elegant, but works currently 
            session_generator_entire_class()
            return HttpResponseRedirect('emojudgement_afew_p004_02')   
    return HttpResponseRedirect('emojudgement_afew_p004')     

def info_collection_p2_afew(request):
    return render(request, 'afew/survey2.html')

def info2_add_afew(request):
    global all_global_vars  
    if request.method =='POST': # ok with multiple submission 
        Ethnicity = request.POST["Ethnicity"]
        Language = request.POST["Language"]
        OtherLanguage = request.POST["OtherLanguage"]
        OtherEthnicity = request.POST["OtherEthnicity"]
    all_global_vars['personal_info']['ethnicity'] = OtherEthnicity if OtherEthnicity else Ethnicity
    all_global_vars['personal_info']['language'] = OtherLanguage if OtherLanguage else Language
    
    erq_answered = 0 # for the full set siatuation, subject only need to answer once 
    # search the sessions with the id, to see if any answer stored in the seesion 
    record = afew_experiment_session.objects.filter(uid = all_global_vars['personal_info']['uid'])
    for i in record: # a bug, some subjects participanted in this experiment, but no erq data, no data != empty 
        print('------------------------i------------------------')
        try:
            if json.loads(i.erq): 
#            print(json.loads(i.erq))
                erq_answered = 1 
                break
        except:
            pass
    if erq_answered:
        return HttpResponseRedirect('emojudgement_afew_end')
    return HttpResponseRedirect('emojudgement_afew_erq')
    
    
def erq_render_afew(request):
    return render(request, 'afew/ERQ.html')
    
def erq_collection_afew(request):
    global all_global_vars
    if request.method =='POST':
        for i in range(1,11):
            dir_name = 'Item' + str(i)
            all_global_vars['erq_answer'] += request.POST[dir_name]
#    print(all_global_vars['erq_answer'])
    return HttpResponseRedirect('emojudgement_afew_end')        

def p4_afew(request):
    # for mixed up emotion experiment 
    #show the total amount of videos, estimated time and the video sequence
    global all_global_vars
    emo = ''.join([i for i in all_global_vars['video_sequence'][0].split('.')[0] if not i.isdigit()])
    amount = len(all_global_vars['video_sequence'])
    estimated_time = int  (amount/ 5 ) + 2 
    return render(request,'afew/p004.html',{'emo' : emo , 'amount' : amount , 'estimated_time': estimated_time} )
    
def p4_02_afew(request):
    global all_global_vars
    current_emotion = all_global_vars['other_vars']['emotion_class']
    emotions_if_watched = person_full_set.objects.get(uid=all_global_vars['personal_info']['uid']).emotions_if_watched
    emotions_if_watched = json.loads(emotions_if_watched)
    watched = []
    unwatched = [] 
    for i in emotions_if_watched:
#        if i == current_emotion: # skip the current one, otherwise 
#            continue 
        if emotions_if_watched[i]:
            watched.append(i)
        else:
            unwatched.append(i)
    amount = len(all_global_vars['video_sequence'])
    estimated_time = int  (amount/ 5 ) + 2 
        # empty set problem // can return none to them 
    return render(request,'afew/p004_2.html', {'user_name': all_global_vars['user_name'], 'finished': watched,
                                               'current_emotion':current_emotion , 'unwatched': unwatched , 
                                               'estimated_time': estimated_time})
    
def playing_afew(request):

    global all_global_vars
    if all_global_vars['other_vars']['submission process']  == 'playing':# have to return something for the last click
        all_global_vars['other_vars']['submission process']  = 'authenticity'
        # THe core is, all operation except the render function only should be excuted once, it will be excuted mutiple times without this flag chaecking 
        all_global_vars['current_page'] += 1 # start from -1 
        questions = all_global_vars ['video_sequence'] # get all videos name 
        question_paths = ['static/afew/AFEW_DATA/{category}/{filename}'.format(category =i[:-13] , filename = i) for i in questions] # get all videos path, according to their name 
        all_global_vars['other_vars']['current_video_path'] = question_paths[all_global_vars['current_page']] # save the path to global one, do not use local variable since it's hard to solve the mutiple submission problem        
        print('this is the start timestamp: {}'.format((str(time.time()))))
        all_global_vars['time_stamp'].append(str(time.time()))
        return render(request,'afew/playing.html',{'path': all_global_vars['other_vars']['current_video_path'] , 
        'emo':'xxx' , 'count' : all_global_vars['current_page'] + 1 ,'total': len(all_global_vars['video_sequence'])})
        
    else:# else = there defenitly is a request is excuted successfully 
        return render(request,'afew/playing.html',{'path': all_global_vars['other_vars']['current_video_path'] , 
        'emo':'xxx' , 'count' : all_global_vars['current_page'] + 1 ,'total': len(all_global_vars['video_sequence'])})        

def save_authenticity_afew (request):

    global all_global_vars
    
    if all_global_vars['other_vars']['submission process']  == 'authenticity':# have to return something for the last click
        all_global_vars['other_vars']['submission process']  = 'confidence'
        if request.method =='POST':
            authenticity = request.POST["authenticity"]
            all_global_vars['videos_answer'].append(authenticity)     
#            print('this is the end timestamp: {}'.format((str(time.time()))))
            all_global_vars['time_stamp'][-1] += '-'
            all_global_vars['time_stamp'][-1] += (str(time.time()))   
#            print(all_global_vars['time_stamp'])
#            all_global_vars['other_vars']['submission process']  = 'confidence'
            global skip_confidence # testing only, speed up the test by skiping the confidence page 
            if skip_confidence:
                return HttpResponseRedirect('emojudgement_AFEW_play')
            return HttpResponseRedirect('emojudgement_afew_confidence')
    else: # click multiple times 
        return HttpResponseRedirect('emojudgement_afew_confidence')
        
def confidence_afew(request):

    return render (request, 'afew/confidence.html')

    
    
def savecondifence_afew (request):
    # save the condifence data and redirect to playing.html 
    # check point, for per 20 videos, user can choice to take a rest 
    # that is for each 20 videos, jump the choice page.
    
    global all_global_vars , test 
    current_page_index = all_global_vars['current_page'] + 1
    length_session = len(all_global_vars ['video_sequence'])
         
    if test:
        length_session = 2 # test only, speed up 
    break_after_videos = 20 # after watching every 20 video clips, take a break, user click the back button when they rest enough         
    keep_playing = 1 if current_page_index < length_session else 0 # 0 means all videos are played, end the palying and request to render the question page 
    if all_global_vars['other_vars']['submission process']  == 'confidence':
        all_global_vars['other_vars']['submission process']  = 'playing'
        if request.method =='POST':
            con_level = request.POST["Option"]
            seen = request.POST["Unknown/Known"]
            all_global_vars['seen_before'].append(seen)
            all_global_vars['confidence'].append(con_level)
        if keep_playing:
            if all_global_vars['is_full_dataset'] and current_page_index % break_after_videos == 0 and length_session - current_page_index > 10: 
                return HttpResponseRedirect('emojudgement_afew_break') 
            if not all_global_vars['is_full_dataset']:
                next_emo = all_global_vars ['video_sequence'][current_page_index]
                next_emo = ''.join([i for i in next_emo.split('.')[0] if not i.isdigit()])
                last_emo = all_global_vars ['video_sequence'][current_page_index-1]
                last_emo = ''.join([i for i in last_emo.split('.')[0] if not i.isdigit()])
#                print(next_emo)
#                print(last_emo)
                if next_emo != last_emo:

                    all_global_vars['other_vars']['next_emo'] = next_emo
                    return HttpResponseRedirect('emojudgement_afew_break1') 
            return HttpResponseRedirect('emojudgement_AFEW_play') 
        else:
            return HttpResponseRedirect('emojudgement_afew_survey2')    
    else:
        if keep_playing:
            return HttpResponseRedirect('emojudgement_AFEW_play')
        else:
            return HttpResponseRedirect('emojudgement_afew_survey2') 
            
        #to end the experiment directly, won't be used during the experiment 
#        keys = list(request.POST)
#        print(keys)
#        if 'continue' in keys:   
#        #        return HttpResponseRedirect('/confidence')
#            pass
#        if 'end' in keys:
#            print('the second button do something')
#            return HttpResponseRedirect('emojudgement_afew_survey2')    
def breakpage_afew (request):
    return render (request,'afew/breakorskip.html') 

def breakpage_afew_mixed (request):
    return render (request,'afew/breakorskip1.html' , {'next_emo' : all_global_vars['other_vars']['next_emo'] }) 

def save_to_local(data,time_id):
    #save all global vars to a local .txt file
    #in case the database crash or other users are unfamiliar with sql
    #file name is the primary key 
    #first row is personal info 
    file_name = 'data/'+ str(time_id) + '.txt'
    
    personal_info = [data['user_name'], data['personal_info']['uid'],data['personal_info']['gender'], data['personal_info']['age'],
                     data['personal_info']['glass'],data['personal_info']['ethnicity'], data['personal_info']['language'] , data['erq_answer'],
                    'only one emotion' if data['is_full_dataset'] else 'all emotions mixed up id is: ' + str (all_global_vars['other_vars']['session_id']) ]

    verbal_response = list(itertools.zip_longest(data['video_sequence'] , data['videos_answer'], data['time_stamp'], 
                                                 data['seen_before'],data['confidence'], fillvalue=''))
    with open (file_name , 'w') as f:
        for i in personal_info:
            i = str(i)
            f.write(i)
            f.write(',')
        f.write('\n')
        for i in verbal_response:
            for j in i:
                f.write(j)
                f.write(',')
            f.write(';')
            f.write('\n')

def end_afew(request):
    global all_global_vars
    print(all_global_vars)
    time_id = int(time.time())

    afew_experiment_session.objects.create(
    date_id = time_id,
    uid = all_global_vars['personal_info']['uid'],
    is_full_dataset =  all_global_vars['is_full_dataset'],
    name = all_global_vars['user_name'],
    age = all_global_vars['personal_info']['age'],
    gender = all_global_vars['personal_info']['gender'],
    glassess = all_global_vars['personal_info']['glass'],
    ethnicity = all_global_vars['personal_info']['ethnicity'],
    language = all_global_vars['personal_info']['language'],
    questions =  json.dumps(all_global_vars['video_sequence']),
    answer = json.dumps(all_global_vars['videos_answer']),
    confidence = json.dumps(all_global_vars['confidence']),
    seen_before =json.dumps(all_global_vars['seen_before']),
    time_stamp = json.dumps(all_global_vars['time_stamp']),
    erq = json.dumps(all_global_vars['erq_answer']),
    )

    # set this session as watched 
    if all_global_vars['is_full_dataset']:
        # read, json load, modify, then save to the database 
        UID = all_global_vars['personal_info']['uid']
        subjects_record = person_full_set.objects.get(uid = UID) # Query
#        print(subjects_record)
        emotion_info = json.loads(subjects_record.emotions_if_watched) # get the dict storing the emotion info
        emotion_info[all_global_vars['other_vars']['emotion_class']] = True # update 
#        print(emotion_info)
        person_full_set.objects.filter(uid = UID).update(emotions_if_watched = json.dumps(emotion_info)) #update at database 
    else:
        sessions.objects.filter(session_id=all_global_vars['other_vars']['session_id']).update(is_watched=True) # so far, this session is compelted, set the session as watched.
    
    save_to_local(all_global_vars,time_id)
    
    return render (request,'afew/Conclusion.html')


def databasedisplay1(request):
    # dataset admin page, to show the data stored in the database
    record = sessions.objects.all()
    print(record)
    return render(request,'afew/datadisplay_1.html',{'records':record})

def databasedisplay2(request):
    # dataset admin page, to show the data stored in the database
    record = person_full_set.objects.all()
    print(record)
    return render(request,'afew/datadisplay_2.html',{'records':record})

def databasedisplay(request):
    # dataset admin page, to show the data stored in the database
    record = afew_experiment_session.objects.all()
    print(record)
    return render(request,'afew/datadisplay.html',{'records':record})
    
def unit_test(request):
#    print('for unit testing')
#    delete_everything(sessions)
#    delete_everything(afew_experiment_session)
    
#    all_id = sessions.objects.all().values("session_id")
#    
#    x = afew_experiment_session.objects.all()[0]
##    .values("questions")    
#    print(x.questions)
#    xxx = json.loads(    x.questions   )
#    for i in xxx:
#        print(i)
#    print(xxx)
    
#    set_id = '3'
#    for i in range (1,9):
#        ids = set_id + '_' + str(i)
#        sessions.objects.filter(session_id=ids ).update(is_watched=True)
    sessions.objects.all().update(is_watched=True)
#    with open ('data/1538629744.txt' , 'w') as f:
#        f.write('hello')
    return HttpResponse('all good you bitch')