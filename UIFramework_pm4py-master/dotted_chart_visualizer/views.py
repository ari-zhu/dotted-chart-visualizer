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
from .filter_functions import convert_log_to_df
import pandas as pd

# Create your views here.

def dcv(request):
    #if (get,post--> user interaction)
    #else(response to clicking on sidebar, returns default graph)
    if settings.EVENT_LOG_NAME != ":notset:":

        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
        file_dir = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)

        # validity check

        default_x_axis_df, default_y_axis_df = setDefault(convert_log_to_df(file_dir))
        x_label, y_label= de
        default_x_axis_list = default_x_axis_df.values.tolist()
        default_y_axis_list = default_y_axis_df.values.tolist()

        return render(request, 'dcv.html', {'log_name': settings.EVENT_LOG_NAME, 'default_x_axis_list': default_x_axis_list,
                                        'default_y_axis_list': default_y_axis_list})

    #error message if no event log was selected:
    else:
        message = "no file selected"
        return render(request, 'dcv.html', {'error_message': message})

