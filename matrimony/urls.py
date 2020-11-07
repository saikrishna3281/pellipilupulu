"""matrimony URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from . import settings
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('show_users', views.show_users, name="show_users"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('otp_view', views.otp_view, name="otp_view"),
    path('view_profile_readonly/(?P<reg_id>\d(10,18))/$', views.view_profile_readonly, name="view_profile_readonly"),
    path('matrimony_registration', views.matrimony_registration, name="matrimony_registration"),
    path('update_password', views.update_password, name="update_password"),
    # path('user_images', views.user_images, name="user_images"),
    # path('display_user_images', views.display_user_images, name="display_user_images"),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
