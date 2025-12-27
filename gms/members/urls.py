from django.urls import path
from .views import create_member

urlpatterns = [
    path('add/', create_member, name='member-add'),
]
