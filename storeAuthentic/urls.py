from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
import sys , os

from . import views 

from django.urls import include, path
from django.conf.urls import include

urlpatterns = [
    path('logIn/' , views.logIn, name='logIn'),  
    path('register/' , views.register, name='register'),  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
