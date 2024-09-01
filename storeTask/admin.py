from django.contrib import admin
from .models import Image, Video, Audio


admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Audio)