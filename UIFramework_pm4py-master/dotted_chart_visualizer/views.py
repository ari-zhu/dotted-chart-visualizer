from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from django.http import HttpResponseRedirect
from bootstrapdjango import settings
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from .filter_functions import setDefault, get_unique_values, convertTimeStamps, convertDateTimeToString, \
    sortByTime, getTimeLabel

from .filter_functions import getAttributeNames
from .utils import convertLogToDf, data_points

from .utils import sorted_data_points
import pandas as pd
import json

# Create your views here.

def dcv(request):
    #if (get,post--> user interaction)
    #else(response to clicking on sidebar, returns default graph)
    if settings.EVENT_LOG_NAME != ":notset:":

        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
        file_dir = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)
        log_df, case_level_attributes,log_level_attributes = convertLogToDf(file_dir)
        log_attribute_list = log_level_attributes+case_level_attributes

        if request.method == 'POST':
            selection_dict = {k: v[0] for k, v in dict(request.POST).items()}
            print(selection_dict)
            selection_dict.pop('csrfmiddlewaretoken')
            sort_attr, attr_level = selection_dict['trace_sort'].split(';')
            selection_dict.pop('trace_sort')
            selection_list = [v for k, v in selection_dict.items()]
            print(selection_list)

            if "setButton" in request.POST:
                selection_dict.pop('setButton')


            if getTimeLabel(log_df) in selection_list:
                t_label = getTimeLabel(log_df)
                log_df_time_sorted = sortByTime(log_df)
                time_values_list = convertDateTimeToString(convertTimeStamps(log_df_time_sorted))

                if selection_dict['xaxis_choice'] == t_label:
                    x_axis_order = time_values_list
                else: x_axis_order = get_unique_values(log_df, selection_dict['xaxis_choice']).tolist()

                if selection_dict['yaxis_choice'] == t_label:
                    y_axis_order = time_values_list[::-1]
                else: y_axis_order = get_unique_values(log_df, selection_dict['yaxis_choice']).tolist()[::-1]


            else:
                x_axis_order = get_unique_values(log_df, selection_dict['xaxis_choice']).tolist()
                y_axis_order = get_unique_values(log_df, selection_dict['yaxis_choice']).tolist()[::-1]

            if sort_attr == 'default':
                print(attr_level)
                print(sort_attr)
                label_list, data_list, legend_list = data_points(log_df, selection_dict)
            elif sort_attr == 'duration':
                pass
            else:
                pass
            default_try = False
            axes_order = [x_axis_order, y_axis_order]
            return render(request, 'dcv.html',
                          {'log_name': settings.EVENT_LOG_NAME, 'axis_list': data_list, 'label_list': label_list,
                            'legend_list': legend_list, 'attribute_list': log_attribute_list,
                             'log_level_attributes': log_level_attributes, 'case_level_attributes':case_level_attributes,
                             'axes_order': axes_order,
                             'sort_attr': sort_attr, 'attr_level': attr_level, 'default_try': default_try})

            #else:

            #return HttpResponse()
            #return HttpResponse(json.dumps(log_df.columns.tolist()))
            #return HttpResponse(["label list: ",label_list, "legend list ", legend_list])
            #return HttpResponse(json.dumps(request.POST))
            #return HttpResponse(json.dumps(log_level_attributes))




        else:
            if len(log_df.columns) != 1: #check if valid file
                default_axis_list, default_x_axis_label, default_y_axis_label, default_axis_order = setDefault(log_df)
                default_label_list = [default_x_axis_label, default_y_axis_label]
                default_try = True
                sort_selection = 'default;log'
                # log_attribute_list = getAttributeNames(convertLogToDf(file_dir))
                # return HttpResponse(json.dumps(default_axis_list))
                print(default_axis_order)
                return render(request, 'dcv.html',
                              {'log_name': settings.EVENT_LOG_NAME, 'default_axis_list': default_axis_list,
                               'default_label_list': default_label_list,
                               'attribute_list': log_attribute_list, 'default_try': default_try,
                               'log_level_attributes': log_level_attributes,
                               'case_level_attributes': case_level_attributes,
                               'default_axis_order': default_axis_order,
                               'sort_selection': sort_selection})
            else:
                message = "file not valid or separator in CSV file not recognized"
                return render(request, 'dcv_test.html', {'error_message': message})

    #error message if no event log was selected:
    else:
        message = "no file selected"
        return render(request, 'dcv.html', {'error_message': message})