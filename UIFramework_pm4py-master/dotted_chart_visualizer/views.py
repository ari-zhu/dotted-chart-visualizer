from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from django.http import HttpResponseRedirect
from bootstrapdjango import settings

# Create your views here.

def dcv(request):
    return render(request, 'dcv.html', {'log_name': settings.EVENT_LOG_NAME})

