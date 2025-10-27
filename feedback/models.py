from django.db import models
from django.contrib.auth.models import User 

class Videos(models.Model):
    uploader_id = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE)
    video_url = models.CharField(max_length=1024)
    school_name = models.CharField(max_length=255, blank=True, null=True)

class Form_feedback(models.Model):
    filled_by =  models.ForeignKey(User, related_name='form', on_delete=models.CASCADE)
    school_name = models.CharField(null=True, max_length=100)
    q1 = models.IntegerField(default = 0)
    q2 = models.IntegerField(default = 0)
    q3 = models.IntegerField(default = 0)
    q4 = models.IntegerField(default = 0)
    q5 = models.IntegerField(default = 0)
    q6 = models.IntegerField(default = 0)
    q7 = models.IntegerField(default = 0)
    q8 = models.IntegerField(default = 0)
    q9 = models.IntegerField(default = 0)
    q10 = models.IntegerField(default = 0)