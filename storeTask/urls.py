from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
import sys , os

from . import views 

from django.urls import include, path
from django.conf.urls import include

urlpatterns = [
    path('home/' , views.home, name='home'),  
    path('Imge/' , views.Imge, name='Imge'), 
    path('Vdeo/' , views.Vdeo, name='Vdeo'), 
    path('Adio/' , views.Adio, name='Adio'),  
    path('map/' , views.map, name='map'),  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
