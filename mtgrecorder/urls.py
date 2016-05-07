"""mtgrecorder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^tournamentHost/', include('tournamentHost.urls')),
    url(r'^admin/', admin.site.urls),
    # Auth-related URLs:
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'^loggedin/$', 'mtgrecorder.views.loggedin', name='loggedin'),
    # Registration URLs
    url(r'^register/$', 'mtgrecorder.views.register', name='register'),
    url(r'^register/complete/$', 'mtgrecorder.views.registration_complete', name='registration_complete'),
    url(r'^welcome/', 'mtgrecorder.views.welcome', name='welcome'),
    url(r'^request/', 'mtgrecorder.views.request_verification', name='request_verification'),
    url(r'^verify_request/', 'mtgrecorder.views.verify_request', name='verify_request'),
    #url(r'', 'mtgrecorder.views.welcome', name='welcome'),
    url(r'^match/(\d+)$', 'mtgrecorder.views.confirm_match', name='confirm_match'),
    # Below should be all confirmed match results...
    #url(r'^answer/$',      'app.views.xxx_test1', name='newAnswer '),
]
