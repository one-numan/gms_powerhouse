from django.urls import path
from .views import dashboard_router,dashboard_org

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_router, name='router'),
    path('org/', dashboard_org, name='org'),
    path('branch/', dashboard_org, name='branch'),
    path('staff/', dashboard_org, name='staff'),
]
