from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from bootstrapdjango import settings
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from .filter_functions import setDefault, get_unique_values, convertTimeStamps, convertDateTimeToString, \
    sortByTime, getTimeLabel, sortyByTraceDuration, \
    getCaseLabel, convertDateTimeToStringsDf,sortByFirstInTrace,sortByLastInTrace

from .filter_functions import getAttributeNames
from .utils import convertLogToDf, data_points, selection


# Create your views here.

def dcv(request):
    #if (get,post--> user interaction)
    #else(response to clicking on sidebar, returns default graph)
    if settings.EVENT_LOG_NAME != ":notset:":

        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
        file_dir = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)
        name, extension = os.path.splitext(file_dir)
        log_df, case_level_attributes,log_level_attributes = convertLogToDf(file_dir)
        log_attribute_list = log_level_attributes+case_level_attributes

        if request.method == 'POST':
            selection_dict = {k: v[0] for k, v in dict(request.POST).items()}
            print(selection_dict)
            selection_dict.pop('csrfmiddlewaretoken')
            sort_attr, attr_level = selection_dict['trace_sort'].split(';')
            selection_dict.pop('trace_sort')
            selection_list = [v for k, v in selection_dict.items()]

            if "setButton" in request.POST:
                selection_dict.pop('setButton')

            #axes_only, complete, selection_list = selection(selection_dict)

            #if ('duration' and getCaseLabel(log_df)) and axes_only:
                #draw graph
                #if sort by duration sort

            if getTimeLabel(log_df) in selection_list[2:]:
                error_message = 'invalid configuration'
                #return render(request, 'dcv.html', {'error_message': error_message})
                default_axis_list, default_x_axis_label, default_y_axis_label, default_axis_order = setDefault(log_df)
                default_label_list = [default_x_axis_label, default_y_axis_label]
                default_try = True
                sort_selection = 'default;log'
                return render(request, 'dcv.html',
                              {'error_message': error_message, 'log_name': settings.EVENT_LOG_NAME, 'default_axis_list': default_axis_list,
                               'default_label_list': default_label_list,
                               'attribute_list': log_attribute_list, 'default_try': default_try,
                               'log_level_attributes': log_level_attributes,
                               'case_level_attributes': case_level_attributes,
                               'default_axis_order': default_axis_order,
                               'sort_selection': sort_selection})

            if getTimeLabel(log_df) in selection_list[:2]:
                t_label = getTimeLabel(log_df)
                log_df_time_sorted = sortByTime(log_df)
                time_values_list = convertDateTimeToString(convertTimeStamps(log_df_time_sorted))
                if extension == '.xes':
                    convertDateTimeToStringsDf(log_df)

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
                label_list, data_list, legend_list = data_points(log_df, selection_dict)
            elif sort_attr == 'duration' and getCaseLabel(log_df) in selection_list[:2]:
                case_label = getCaseLabel(log_df)
                if extension == '.csv':
                    trace = sortyByTraceDuration(log_df,string=True)
                else:
                    trace = sortyByTraceDuration(log_df)
                #provisorisch:
                trace_id_list = [a[0] for a in trace]
                if selection_dict['xaxis_choice'] == case_label:
                    x_axis_order = trace_id_list
                if selection_dict['yaxis_choice'] == case_label:
                    y_axis_order = trace_id_list[::-1]

            else:
                if getCaseLabel(log_df) in selection_list:
                    case_label = getCaseLabel(log_df)
                    if attr_level == 'log':
                        if case_label == selection_dict['xaxis_choice']:
                            x_axis_order = sortByFirstInTrace(log_df, sort_attr)
                        if case_label == selection_dict['yaxis_choice']:
                            y_axis_order = sortByFirstInTrace(log_df, sort_attr)[::-1]
                    else:
                        if attr_level == 'first':
                            if case_label == selection_dict['xaxis_choice']:
                                x_axis_order = sortByFirstInTrace(log_df, sort_attr)
                            if case_label == selection_dict['yaxis_choice']:
                                y_axis_order = sortByFirstInTrace(log_df, sort_attr)[::-1]
                        else: #attr_level == 'last'
                            if case_label == selection_dict['xaxis_choice']:
                                x_axis_order = sortByLastInTrace(log_df, sort_attr)
                            if case_label == selection_dict['yaxis_choice']:
                                y_axis_order = sortByLastInTrace(log_df, sort_attr)[::-1]

            default_try = False
            axes_order = [x_axis_order, y_axis_order]
            label_list, data_list, legend_list = data_points(log_df, selection_dict)

            return render(request, 'dcv.html',
                          {'log_name': settings.EVENT_LOG_NAME, 'axis_list': data_list, 'label_list': label_list,
                            'legend_list': legend_list, 'attribute_list': log_attribute_list,
                             'log_level_attributes': log_level_attributes, 'case_level_attributes':case_level_attributes,
                             'axes_order': axes_order,
                             'sort_attr': sort_attr, 'attr_level': attr_level, 'default_try': default_try})


        else:
            if len(log_df.columns) != 1: #check if valid file
                default_axis_list, default_x_axis_label, default_y_axis_label, default_axis_order = setDefault(log_df)
                default_label_list = [default_x_axis_label, default_y_axis_label]
                default_try = True
                sort_selection = 'default;log'
                return render(request, 'dcv.html',
                              {'log_name': settings.EVENT_LOG_NAME, 'default_axis_list': default_axis_list,
                               'default_label_list': default_label_list,
                               'attribute_list': log_attribute_list, 'default_try': default_try,
                               'log_level_attributes': log_level_attributes,
                               'case_level_attributes': case_level_attributes,
                               'default_axis_order': default_axis_order,
                               'sort_selection': sort_selection})
            else:
                error_message = "file not valid or separator in CSV file not recognized"
                return render(request, 'dcv_test.html', {'error_message': error_message})

    #error message if no event log was selected:
    else:
        fatal_error_message = 'You have not set any event log as input. Use "Event Data" tab to set an event log as input!'
        return render(request, 'dcv.html', {'fatal_error_message': fatal_error_message})