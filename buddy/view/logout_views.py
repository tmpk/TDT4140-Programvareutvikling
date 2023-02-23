from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('buddy:index'))
