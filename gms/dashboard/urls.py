from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('org/', views.sample_page, name='org'),
    path('branch/', views.sample_page, name='branch'),
    path('staff/', views.sample_page, name='staff'),
    path('blank-page/',views.blank_page,name='blank')
]
