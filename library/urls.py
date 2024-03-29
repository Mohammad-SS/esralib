"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.utils import timezone
from django.contrib import admin
from lib import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$' , views.index , name='index'),
    url(r'^cats/(?P<pk>[0-9]+)/$' , views.category ,name='category'),
    url(r'^cats/(?P<pk>[0-9]+)/$' , views.category ,name='category'),
    url(r'^resource/(?P<pk>[0-9]+)/$' , views.books ,name='books'),
    url(r'^action/reserve/$' , views.reserveaction ,name='reserve_action'),
    url(r'^login$' , views.login ,name='login'),
    url(r'^action/dologin/$' , views.dologin , name='dologin'),
    url(r'^logout$' , views.logout ,name='logout'),
    url(r'^dmdb$' , views.dummybooks ,name='db'),
    
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)