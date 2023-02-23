
from django.conf.urls import include, url
from django.contrib import admin
from buddy import views


urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^', include('buddy.urls')),
]
