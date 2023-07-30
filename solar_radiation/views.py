from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .forms import MyForm, member
from .models import User

from suntime import Sun
from datetime import datetime, timedelta
import requests
import xgboost as xgb
from joblib import load
import numpy as np
import os

import matplotlib.pyplot as plt

#get latitude longtitude
response = requests.get('https://ipinfo.io/json')
data = response.json()
location = data['loc'].split(',')
latitude = float(location[0])
longitude = float(location[1])

def login(request):
    template = loader.get_template('login.html')
    members = User.objects.all().values()

    if request.method == 'POST':
        form = member(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            for x in members:
                if username == x["username"] and password == x["password"]:
                    return redirect('/colar/')
                else:
                    context = {'form': form, "massage":"Invalid Username and Password"}
                    return HttpResponse(template.render(context, request))
    else:
        form = member()

    context = {'form': form}
    return HttpResponse(template.render(context, request))

def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context,request))

def predict(request):
    #set value
    result = 0
    
    #where sun
    sun = Sun(latitude, longitude)

    #rise hour/minute
    sunrise_time = str(sun.get_sunrise_time()).split(' ')[1].split(':00+00:00')[0]
    start_time = datetime.strptime(sunrise_time, "%H:%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=7)).time().strftime("%H:%M")
    risehour = int(end_time.split(':')[0])
    riseminute = int(end_time.split(':')[1])

    #set  hour/minute
    sunset_time = str(sun.get_sunset_time()).split(' ')[1].split(':00+00:00')[0]
    start_time = datetime.strptime(sunset_time, "%H:%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=7)).time().strftime("%H:%M")
    sethour = int(end_time.split(':')[0])
    setminute = int(end_time.split(':')[1])

    #unixtime
    current_datetime = datetime.now()
    unixtime = int(current_datetime.timestamp())

    #date month year hour minute second
    date  = current_datetime.day
    month = current_datetime.month
    hour  = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            temp = form.cleaned_data['temperature']
            pressure = form.cleaned_data['pressure']
            humidity = form.cleaned_data['humidity']
            wind = form.cleaned_data['wind']
            speed = form.cleaned_data['speed']
            
            #current path
            current_path = os.getcwd()
            current_path = current_path.split('\mysite')[0]

            #load model
            model_path = os.path.join(current_path, "model\model.bin")
            load_model = xgb.Booster()
            load_model.load_model(model_path)

            #load scaler
            scaler_path = os.path.join(current_path, "model\scaler.pkl")
            scaler = load(scaler_path)

            #predicting
            data = [unixtime, temp, pressure, humidity, wind, speed, month, date, hour, minute, second, riseminute, sethour, setminute]
            data = np.array(data).reshape(1,-1)
            data = scaler.transform(data)
            data = xgb.DMatrix(data)
            result = round(load_model.predict(data)[0],2)
    else:
        form = MyForm()

    template = loader.get_template('prediction.html')
    context = {'form': form, 
             'result': result,
             'rise': str(risehour) + ":" + str(riseminute),
             'set': str(sethour) + ":" + str(setminute),
    }
    
    return HttpResponse(template.render(context, request))

def user(request):
    template = loader.get_template('user.html')
    current_datetime = datetime.now()

    context = {
        'date': str(current_datetime.strftime("%d/%m/%Y")),
        'time': str(current_datetime.strftime("%H:%M:%S")),
        'lati':latitude,
        'long':longitude,
        'temp': 37,
        'humi': 70,
    }
    return HttpResponse(template.render(context, request))

def game(request):
    template = loader.get_template('share.html')
    context = {}
    return HttpResponse(template.render(context, request))

def play(request):
    template = loader.get_template('game.html')
    context = {}
    return HttpResponse(template.render(context, request))

def hackathon(request):
    template = loader.get_template('hackathon.html')
    context = {}
    return HttpResponse(template.render(context, request))
