"""
URL configuration for gms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path,include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('members/', include('members.urls')),
#     path('accounts/', include('accounts.urls')),
#     path('dashboard/', include('dashboard.urls')),

# ]
from django.contrib import admin
from django.urls import path, include, re_path
from dashboard.views import dashboard_router,fast_logout  # IMPORT IT
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('', dashboard_router, name='dashboard_router'),  # ✅ REQUIRED
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    # ✅ LOGOUT AT ROOT
    path('logout/', fast_logout, name='logout'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), 
]
