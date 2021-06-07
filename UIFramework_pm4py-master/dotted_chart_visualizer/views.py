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
from .test import data_points
import pandas as pd
import json

# Create your views here.

def dcv(request):
    #if (get,post--> user interaction)
    #else(response to clicking on sidebar, returns default graph)
    if settings.EVENT_LOG_NAME != ":notset:":

        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
        file_dir = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)
        log_df = convertLogToDf(file_dir)
        log_attribute_list = getAttributeNames(log_df)

        if request.method == 'POST':
            selection_dict = {k: v[0] for k, v in dict(request.POST).items()}
            selection_dict.pop('csrfmiddlewaretoken')
            selection_dict.pop('setButton')
            label_list, data_list, legend_list = data_points(log_df, selection_dict)
            default_try = False
                #return HttpResponse(json.dumps(selection_dict))
            #data_list=data_list[:2]
            return render(request,'dcv.html', {'log_name': settings.EVENT_LOG_NAME, 'axis_list': data_list, 'label_list': label_list, 'legend_list': legend_list, 'attribute_list': log_attribute_list, 'default_try': default_try})
            #return HttpResponse(json.dumps(data_list)+"labels:"+json.dumps(label_list))
            #return HttpResponse(json.dumps(label_list))
            #return HttpResponse(json.dumps(log_df.columns.tolist()))
           # return HttpResponse(json.dumps(selection_dict))



        else:
            if len(log_df.columns) != 1: #check if valid file
                default_x_axis_df, default_y_axis_df, default_x_axis_label, default_y_axis_label = setDefault(log_df)
                default_x_axis_list = default_x_axis_df.values.tolist()
                default_y_axis_list = default_y_axis_df.values.tolist()
                default_axis_list = [default_x_axis_list, default_y_axis_list]
                default_label_list = [default_x_axis_label, default_y_axis_label]
                default_try= True
                #log_attribute_list = getAttributeNames(convertLogToDf(file_dir))
                #return HttpResponse(json.dumps(default_axis_list))
                return render(request, 'dcv.html', {'log_name': settings.EVENT_LOG_NAME, 'default_axis_list': default_axis_list, 'default_label_list': default_label_list,
                                                'attribute_list': log_attribute_list, 'default_try': default_try})
            else:
                message = "file not valid or separator in CSV file not recognized"
                return render(request, 'dcv_test.html', {'error_message': message})

    #error message if no event log was selected:
    else:
        message = "no file selected"
        return render(request, 'dcv.html', {'error_message': message})

