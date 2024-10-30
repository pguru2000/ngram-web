from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [ 
    path('', views.similarity_tool, name = 'similarity_tool'),
    path('uploadfiles', views.uploadfiles, name='uploadfiles'),
    path('startprocess', views.startprocess, name='startprocess'),
    path('checkprocess', views.checkprocess, name='checkprocess'),
    path('deletefiles', views.deletefiles, name='deletefiles'),
    path('calcngram', views.calcngram, name='calcngram'),
    path('ngramprocess', views.ngramprocess, name='ngramprocess'),
]
