from django.urls import path
from . import views
from .views import UserLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),

    path('logout/', views.logout_view, name='logout'),
]
