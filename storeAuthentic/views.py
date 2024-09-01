import base64
from collections import ChainMap
from fileinput import FileInput
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
import datetime, uuid, re 
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.conf import settings 
from Task_Project import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 

from storeAuthentic.models import UserProfile

from django.core.files.base import ContentFile  
def logIn(request):    
    if request.method == "POST":   
        username = request.POST.get('email')
        password = request.POST.get('password')
        obj_user = authenticate(request, username = username, password = password)
        profile_obj = UserProfile.objects.filter(email = username).first()
        if profile_obj is None:
            messages.error(request, 'User or E-mail not found.')
            return redirect('logIn')
        if not profile_obj.is_verified:
            messages.error(request, 'User is not verified check your E-mail.')
            return redirect('logIn')
        if obj_user is  None:
            messages.error(request, 'Wrong password.')
            return redirect('logIn') 
                
        login(request , obj_user) 
        return redirect('home')
            
    context = { 
        }
    return render(request, 'login.html',context )
 
def register(request):
    if request.method == "POST":
        var_fname = request.POST.get('fname')  
        var_lname = request.POST.get('lname')  
        var_email = request.POST.get('email') 
        var_password = request.POST.get('password') 
        var_conf_password = request.POST.get('conf-password')  
        var_gender = request.POST.get('gender')
        var_profile = request.POST.get('image')  
        
        if((len(var_profile) == 0) and len(request.FILES) == 0):
            pass
        else:
            if len(request.FILES) != 0:
                var_profile = request.FILES['input_img']  # this is pass by java filed modalShow 
            else:
                var_profile = Image_Decode(var_profile)
    
      
        if(len(var_email) <= 5):
            messages.error(request, 'Email Failed must be filled with correctly.')
            return redirect('register')
        elif(len(var_fname) <=2 ):
            messages.error(request, 'First name  must be have 3 character')
            return redirect('register')
        elif(len(var_lname) <=2 ):
            messages.error(request, 'First name  must be have 3 character')
            return redirect('register')
        elif(len(var_password) < 6):
            messages.error(request, 'Password must be  have 6 Character or Digits.')
            return redirect('register')
        elif(var_password != var_conf_password):
            messages.error(request, 'Password and Confirm Password must same.')
            return redirect('register') 
        elif(len(var_gender) < 3):
            messages.error(request, 'Gender Option must be Selected')
            return redirect('register')
        else: 
            if UserProfile.objects.filter(username = var_email).first():
                    messages.error(request, 'Username / Email is already Taken.')
                    return redirect('register')
            else:
                try:
                    user_obj = UserProfile(username = var_email , email = var_email, profile_image = var_profile)
                    user_obj.first_name = var_fname
                    user_obj.last_name = var_lname 
                    user_obj.gender = var_gender  
                    user_obj.set_password(var_password)
                    user_obj.auth_token = str(uuid.uuid4()) 
                    user_obj.save()       
                    messages.success(request, 'Your Account are successfully Created.')
                    return redirect('logIn')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Some Internal Error found 404')
                    return redirect('register')
                
    context = { }
    return render(request, 'register.html',context )

def Image_Decode(img): 
    base64_img = img # get the base64 img 
    base64key = ";base64,"
    name_file = "Profile_image" # name for new upload img
                        
    if base64key in base64_img:
        format, img_str = base64_img.split(base64key)
        ext = format.split('/')[-1]
        full_file_name = f'{name_file}.{ext}'

        full_file_name = f'{name_file}.{ext}'
        var_profile = ContentFile(base64.b64decode(img_str), name=full_file_name)  
        return var_profile

def logout(request):
    logout(request)
    return redirect("logIn")