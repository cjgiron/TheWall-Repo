from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('process_message', views.process_message),
    path('process_comment', views.process_comment)
]