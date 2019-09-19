from django.db import models

# class Employee(models.Model):
	# ID
    # name=models.CharField(max_length=20)
	 
	 
	 
# Create your models here.
class historical_answer(models.Model):
    date_id = models.IntegerField(primary_key = True)
    answer = models.TextField()
    name = models.TextField()

class all_info(models.Model):
    date_id = models.IntegerField(primary_key = True)
    answer = models.TextField()
    name = models.TextField()
    other_info = models.TextField()
    time_stamp = models.TextField()

class completed_info_hcc(models.Model):
    date_id = models.IntegerField(primary_key = True)
    name = models.TextField()
    language = models.TextField()
    ethnicity = models.TextField()
    glassess = models.TextField()
    age = models.TextField()
    gender = models.TextField()
    questions = models.TextField()
    answer = models.TextField()
    confidence = models.TextField()
    seen_before = models.TextField()

class sessions(models.Model):
    session_id = models.TextField(primary_key = True) # <int a>_<int b> .a is the count of full-dataset ; b is the session ID in this full-dataset 
    video_set =  models.TextField()
    is_watched = models.BooleanField(default= False) # 0 unwatched 1: watched
    
class afew_experiment_session(models.Model):
    date_id = models.IntegerField(primary_key = True)
    uid = models.TextField() # only required for full_set people
    is_full_dataset = models.BooleanField() # double check 
    name = models.TextField()
    language = models.TextField()
    ethnicity = models.TextField()
    glassess = models.TextField()
    age = models.TextField()
    gender = models.TextField()
    questions = models.TextField()
    answer = models.TextField()
    confidence = models.TextField()
    seen_before = models.TextField()
    time_stamp = models.TextField()
    erq = models.TextField(default = '')
    
class person_full_set(models.Model):
    uid = models.IntegerField(primary_key = True)
    emotions_if_watched = models.TextField()