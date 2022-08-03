from django.urls import path
from main import views
from main import bot_user

urlpatterns = [
    path('api/', views.index, name='handler'),
  
   
]
