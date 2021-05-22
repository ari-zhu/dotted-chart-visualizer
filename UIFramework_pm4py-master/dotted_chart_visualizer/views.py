from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from django.http import HttpResponseRedirect
from bootstrapdjango import settings
from filter_functions import setDefault, convert_log_to_df
import pandas as pd

# Create your views here.

def dcv(request):
    #if
    #else:
    default_x_axis_df, default_y_axis_df = setDefault(convert_log_to_df(request))
    default_x_axis_list = default_x_axis_df.values.tolist()
    default_y_axis_list = default_y_axis_df.values.tolist()
    return render(request, 'dcv.html', {'log_name': settings.EVENT_LOG_NAME, 'default_x_axis': default_x_axis_list,
                                        'default_y_axis': default_y_axis_list})

