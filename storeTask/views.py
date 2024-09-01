import base64
from collections import ChainMap
from curses import meta
import curses
from fileinput import FileInput
import django
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
import requests 
from Task_Project import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt
from storeTask.models import Image, Video, Audio
from django.utils import timezone
from django.core.files.base import ContentFile  
import folium
from folium.plugins import FastMarkerCluster

# any datamodel
from django.db.models import Avg
# Create your views here.
def home(request):
    template = loader.get_template('home.html')   
    context = {       
        } 
    return HttpResponse(template.render(context, request))



# /////////////////////////////////   ///////////////////      IMAGE      //////////////////      ////////////////////////////////

@csrf_exempt
def Imge(request):
    template = loader.get_template('image.html')   
    img_show = Image.objects.filter()
    if request.method == "POST":
        var_img = request.POST.get('data_img')
        data_coded = Image_Decode(var_img)
         
        obj_image = Image.objects.create(img_file = data_coded)
        obj_image.save()
    context = {      
               'img_show': img_show ,  
        } 
    return HttpResponse(template.render(context, request))


def Image_Decode(img): 
    base64_img = img # get the base64 img 
    base64key = ";base64,"
    date = timezone.now().strftime('%Y%m%d%H%M%S%f') 
    name_file =  "Profile_"+ str(date) # name for new upload img 
                        
    if base64key in base64_img:
        format, img_str = base64_img.split(base64key)
        ext = format.split('/')[-1]  
        ext_0 = format.split('A')[0]    
        print("ext_0: ", ext_0 )
        full_file_name = f'{name_file}.{ext}' 
        var_profile = ContentFile(base64.b64decode(img_str), name = full_file_name)   
        return var_profile

# /////////////////////////////////   ///////////////////      VIDEO      //////////////////      ////////////////////////////////
def Vdeo(request):
    template = loader.get_template('video.html') 
    
    vid_show = Video.objects.filter()  
    if request.method == "POST":
        var_vid = request.POST.get('data_vid')
        data_coded = Image_Decode(var_vid)
        obj_video = Video.objects.create(vid_file = data_coded)
        obj_video.save()
    context = {      
               'vid_show': vid_show 
        } 
    return HttpResponse(template.render(context, request))



# /////////////////////////////////   ///////////////////      AUDIO      //////////////////      ////////////////////////////////
def Adio(request):
    template = loader.get_template('audio.html')  
    aud_show = Audio.objects.filter() 
    if request.method == "POST":
        var_aud = request.POST.get('data_aud')
        data_coded = Image_Decode(var_aud)
        obj_audio = Audio.objects.create(aud_file = data_coded)
        obj_audio.save() 
    context = {   
               'aud_show': aud_show    
        } 
    return HttpResponse(template.render(context, request))


# /////////////////////////////////   ///////////////////      MAP      //////////////////      ////////////////////////////////

 


# def get_coordinates(location_name, api_key):
#     url = 'https://api.openrouteservice.org/geocode/search'
#     params = {
#         'api_key': api_key,
#         'text': location_name,
#         'size': 1  # We only need one result
#     }
#     response = requests.get(url, params=params)
    
#     if response.status_code != 200:
#         print(f"Request failed with status code: {response.status_code}")
#         raise ValueError(f"Could not geocode location: {location_name}")

#     try:
#         data = response.json()
#     except requests.exceptions.JSONDecodeError:
#         print("Failed to decode JSON, response text:", response.text)
#         raise ValueError(f"Could not geocode location: {location_name}")

#     # Debugging: print the geocoding response
#     print("Geocoding Response:", data)
    
#     if 'features' in data and len(data['features']) > 0:
#         coordinates = data['features'][0]['geometry']['coordinates']
#         print("this:", data['bbox'][0])
#         return (coordinates[1], coordinates[0])

#     else:
#         raise ValueError(f"Could not geocode location: {location_name}")
 
    

import folium
from django.http import HttpResponse
from django.template import loader
import requests

def map(request):
    template = loader.get_template('maped.html') 
    ors_api_key = settings.MAP_API_SERVICE
    if request.method == 'POST':
        start_location = request.POST.get('start')
        end_location = request.POST.get('end')
        
        start_lat = request.POST.get('start_lat')
        start_lon =  request.POST.get('start_lon')
        end_lat =  request.POST.get('end_lat')
        end_lon =  request.POST.get('end_lon')
        
        location1 = (start_lat, start_lon)
        location2 = (end_lat, end_lon)
        
        # location1 = get_coordinates(start_location, ors_api_key)
        # location2 = get_coordinates(end_location, ors_api_key)
  
        ors_url = f'https://api.openrouteservice.org/v2/directions/driving-car'
        params = {
            'api_key': ors_api_key,
            'start': f'{location1[1]},{location1[0]}',
            'end': f'{location2[1]},{location2[0]}'
        }

        response = requests.get(ors_url, params=params)
        
        try:
            route_data = response.json()
            print( route_data) 
            # Check if 'features' key is in the response
            if 'features' in route_data:
                # Extract coordinates from the route data
                coordinates = route_data['features'][0]['geometry']['coordinates']
                # Convert coordinates to (lat, lng) tuples
                route_coords = [(coord[1], coord[0]) for coord in coordinates]

                # Create Folium map centered on the start location
                m = folium.Map(location=location1, width=1000, height=700, crs="EPSG3857", left=50)

                # Add markers for start and end locations
                folium.Marker(location1, popup=start_location).add_to(m)
                folium.Marker(location2, popup=end_location).add_to(m)

                # Add the route as a PolyLine to the map
                folium.PolyLine(route_coords, tooltip="Route", color="blue", opacity=0.85).add_to(m)
            else:
                print("No features found in the route data")
                m = folium.Map(location=location1, width=1000, height=700, crs="EPSG3857", left=50)
                folium.Marker(location1, popup=start_location).add_to(m)
                folium.Marker(location2, popup=end_location).add_to(m)
                folium.Popup("Error: Could not retrieve route data").add_to(m)

        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"Response JSON: {route_data}")
            # Create an empty map with an error message
            m = folium.Map(location=location1, width=1000, height=700, crs="EPSG3857", left=50)
            folium.Marker(location1, popup=start_location).add_to(m)
            folium.Marker(location2, popup=end_location).add_to(m)
            folium.Popup("Error: Could not retrieve route data").add_to(m)

        context = {
            'map': m._repr_html_()
        }
        return HttpResponse(template.render(context, request))
    context = {
            'map': "Please Enter Your  Location"
        }
    return HttpResponse(template.render(context, request))

   

# def map(request):
#     template = loader.get_template('maped.html')

#     # Define location names
#     location_name1 = 'Bhatta Chowk, Lahore, Pakistan'
#     location_name2 = 'Model  Town, Lahore, Pakistan'

#     # OpenRouteService API setup
#     ors_api_key = settings.MAP_API_SERVICE

#     # Get coordinates for location names
#     try:
#         coords1 = get_coordinates(location_name1, ors_api_key)
#         coords2 = get_coordinates(location_name2, ors_api_key)
#     except ValueError as e:
#         return HttpResponse(str(e))

#     # OpenRouteService API setup for routing
#     ors_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
#     headers = {
#         'Authorization': ors_api_key,
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'coordinates': [[coords1[1], coords1[0]], [coords2[1], coords2[0]]]
#     }

#     response = requests.post(ors_url, json=data, headers=headers)
#     route_data = response.json()

#     # Debugging: print the routing response
#     print("Routing Response:", route_data)

#     try:
#         # Use index-based access for lists within the response
#         if 'routes' in route_data and len(route_data['routes']) > 0:
#             coordinates = route_data['routes'][0]['geometry']['coordinates']
#             # Convert coordinates to (lat, lng) tuples
#             route_coords = [(coord[1], coord[0]) for coord in coordinates]

#             # Create Folium map centered on the start location
#             m = folium.Map(location=coords1, width=1000, height=700, crs="EPSG3857", left=50)

#             # Add markers for start and end locations
#             folium.Marker(coords1, popup="Start Location").add_to(m)
#             folium.Marker(coords2, popup="End Location").add_to(m)

#             # Add the route as a PolyLine to the map
#             folium.PolyLine(route_coords, tooltip="Route", color="blue", opacity=0.85).add_to(m)
#         else:
#             print("No routes found in the route data")
#             m = folium.Map(location=coords1, width=1000, height=700, crs="EPSG3857", left=50)
#             folium.Marker(coords1, popup="Start Location").add_to(m)
#             folium.Marker(coords2, popup="End Location").add_to(m)
#             folium.Popup("Error: Could not retrieve route data").add_to(m)

#     except (IndexError, KeyError, TypeError) as e:
#         print(f"Exception: {e}")
#         print(f"Response JSON: {route_data}")
#         # Create an empty map with an error message
#         m = folium.Map(location=coords1, width=1000, height=700, crs="EPSG3857", left=50)
#         folium.Marker(coords1, popup="Start Location").add_to(m)
#         folium.Marker(coords2, popup="End Location").add_to(m)
#         folium.Popup("Error: Could not retrieve route data").add_to(m)

#     context = {
#         'map': m._repr_html_()
#     }
#     return HttpResponse(template.render(context, request))










# def map(request):
#     template = loader.get_template('maped.html') 
#     # api = "AIzaSyAVFCQMkgWC6p_4YO3osVHL-0WSGqHZvFg"
#     # location_name = 'pakistan'  # Example location name 
#     # context = {     
#     #         'location_name': location_name,
#     #         'api': api
#     #     } 
    
#     avg_lat = 41.3344
#     #avg_lat = EvChargingLocation.objects.aggregate(avg = Avg('latitude'))['avg']
#     #stations = EvChargingLocation.objects.filter(latitude__gt = avg_lat)
#     Data1 = [
#     {'latitude': 30.100, 'longitude': 71.100}, 
#     ]
#     Data2 = [
#     {'latitude': 30.200, 'longitude': 71.200}, 
#     ]
#     for data in Data1:
#         location1 = data['latitude'] , data['longitude']  
#     for data in Data2: 
#         location2 = data['latitude'] , data['longitude']
    
#     m = folium.Map(location=location1, width=1000, height=700,crs="EPSG3857", left=50)
#     folium.Marker(location1, popup="Multan").add_to(m)
#     folium.Marker(location2, popup="Jhang").add_to(m)
#     folium.PolyLine((location1, location2) ,tooltip="Transit Route 100", color="blue", dot_array='10', opacity='0.85').add_to(m)
    
#     context = {   
#                'map': m._repr_html_() 
#         }
#     return HttpResponse(template.render(context, request))

# from geopy.distance import geodesic
# import osmnx as ox
# import networkx as nx
# from geopy.distance import geodesic
# def map(request):
#     template = loader.get_template('maped.html') 
#     start = "pakistan" # request.GET.get('start')
#     end = "india" #request.GET.get('end')
#     YOUR_MAPBOX_ACCESS_TOKEN  = "pk.eyJ1IjoidXJzY2FwZSIsImEiOiJjamo5bbb2Vnd2YzOHR1M2tsZmE1eGE4d3o0In0.ZsZf1GeBzwNFLxnhH-Vzjw"
#     response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{start}.json?access_token={YOUR_MAPBOX_ACCESS_TOKEN}')
#     start_data = response.json()
#     start_coord = ['31.23212', '71.12312']

#     response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{end}.json?access_token={YOUR_MAPBOX_ACCESS_TOKEN}')
#     end_data = response.json()
#     end_coord = ['31.23212', '71.12312']

#     directions_url = f'https://api.mapbox.com/directions/v5/mapbox/driving/{start_coord[0]},{start_coord[1]};{end_coord[0]},{end_coord[1]}?geometries=geojson&access_token={YOUR_MAPBOX_ACCESS_TOKEN}'

#     response = requests.get(directions_url)
#     route_data = response.json()

#     return JsonResponse(route_data)






#https://www.youtube.com/watch?v=BkGtNBrOhKU