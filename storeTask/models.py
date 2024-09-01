from asyncio.windows_events import NULL
from email.policy import default
from enum import auto
from datetime import datetime, time, date, timezone
from random import choices
import uuid, re 
import django

from django.contrib import messages
from django.db import models
from django.utils.translation import gettext_lazy as _ 
#  verbose_name='Username',
    # profile_image = models.FileField(_("Profile Image"), upload_to="Profile/", blank = False, null=False, default="/Profile/defaultDP.png")

class Image(models.Model):
    img_id = models.AutoField(primary_key=True) 
    img_file = models.FileField(upload_to="Image/")
    created_at = models.DateTimeField(default = django.utils.timezone.now)
     
    
class Video(models.Model):
    vid_id = models.AutoField(primary_key=True) 
    vid_file = models.FileField(upload_to="Video/", max_length = 10000000000)
    created_at = models.DateTimeField(default = django.utils.timezone.now)
    def __str__(self):
        return self.vid_id
    
class Audio(models.Model):
    aud_id = models.AutoField(primary_key=True) 
    aud_file = models.FileField(upload_to="Audio/")
    created_at = models.DateTimeField(default = django.utils.timezone.now)
    def __str__(self):
        return self.aud_id