"""leaf_it_to_us URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import include
from core import views
from registration.backends.simple.views import RegistrationView 
from django.conf import settings
from django.conf.urls.static import static

#Class that redirects user to homepage after login.
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return 'home'


urlpatterns = [
    re_path(r'^$', views.home, name = 'home'),
    re_path(r'^leafittous/', include('core.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/register/$', MyRegistrationView.as_view(), name = 'registration_register'),
    re_path(r'^accounts/social/$', views.account_settings, name='social_settings'),
    re_path(r'^accounts/pasword/$', views.manage_password, name = 'password'),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

