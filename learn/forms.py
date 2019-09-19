from django import forms
 
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    
class Info1(forms.Form):
#    your_name = forms.CharField(label='Your name', max_length=100)
#    MEDIA_CHOICES = (('Audio', (('vinyl', 'Vinyl'),('cd', 'CD'),)),('Video', (('vhs', 'VHS Tape'),('dvd', 'DVD'),)),('unknown', 'Unknown'),)
    gender_choices = [('m' , 'Male') , ('f','Female'),('unkown','Not disclosed')]
    glasses_choice = [('y','Yes') , ('n','No')]
    
    ege = forms.IntegerField(min_value = 1)
    sex = forms.ChoiceField(choices = gender_choices)
    glasses = forms.ChoiceField(choices = glasses_choice)
#    sex = forms.ChoiceField(MultipleChoiceField)

#class Display(forms.Form):
#    your_name = forms.CharField(label='Your name', max_length=100)
#    
#    date_id = models.IntegerField(primary_key = True)
#    answer = models.TextField()
#    name = models.TextField()
#    other_info = models.TextField()
#    time_stamp = models.TextField()