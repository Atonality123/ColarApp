from django.urls import path
from .views import login, home, predict, user, game, hackathon, play

urlpatterns = [  
    # path('', login , name= "login"),
    path('', home , name= "home"),
    path('predict/' , predict , name= "predict"),
    path('hackathon/', hackathon , name= "hackathon"),
    path('game/', game , name= "game"),
    path('game/play', play , name= "play"),
    path('user/', user , name= "user"),
]