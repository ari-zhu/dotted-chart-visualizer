from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from django.http import HttpResponseRedirect
from bootstrapdjango import settings
from .filter_functions import setDefault
from .filter_functions import convertLogToDf
from .filter_functions import getAttributeNames
import pandas as pd

# Create your views here.

def dcv(request):
    #if (get,post--> user interaction)
    #else(response to clicking on sidebar, returns default graph)
    if settings.EVENT_LOG_NAME != ":notset:":

        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
        file_dir = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)

        if len(convertLogToDf(file_dir).columns) != 1: #check if valid file
            default_x_axis_df, default_y_axis_df, default_x_axis_label, default_y_axis_label = setDefault(convertLogToDf(file_dir))
            default_x_axis_list = default_x_axis_df.values.tolist()
            default_y_axis_list = default_y_axis_df.values.tolist()
            default_axis_list = [default_x_axis_list, default_y_axis_list]
            default_label_list = [default_x_axis_label, default_y_axis_label]
            log_attribute_list = getAttributeNames(convertLogToDf(file_dir))
            return render(request, 'dcv.html', {'log_name': settings.EVENT_LOG_NAME, 'default_axis_list': default_axis_list, 'default_label_list': default_label_list,
                                                'attribute_list':log_attribute_list})
        else:
            message = "file not valid or separator in CSV file not recognized"
            return render(request, 'dcv.html', {'error_message': message})

    #error message if no event log was selected:
    else:
        message = "no file selected"
        return render(request, 'dcv.html', {'error_message': message})

