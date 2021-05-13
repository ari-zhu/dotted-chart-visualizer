#from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from django.conf import settings
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter

from pm4py.algo.filtering.pandas.attributes.attributes_filter import apply as df_filter

def convert_log_to_df():
    event_log= settings.EVENT_LOG_NAME #replaced by function parameter later
    event_logs_path = os.path.join(settings.MEDIA_ROOT,"event_logs")
    event_log_file_path=os.path.join(event_logs_path,event_log)
    with open(event_log_file_path,'r') as event_log_file:
        
                name, extension = os.path.splitext(event_log)

                if(extension == ".xes"):
                    variant = xes_importer.Variants.ITERPARSE
                    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
                    log = xes_importer.apply('event_log_file', variant=variant, parameters=parameters)
                    df_event_log = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
                    return df_event_log

                elif(extension == ".csv"):
                    df_event_log= pd.read(event_log_file_path,'r')
                    return df_event_log
                    




    event_log= 
    return df_event_log = to_df_converter(log, variant=log_converter.Variants.TO_DATA_FRAME)
    #retrieve log file from media
    # return log_data_frame
convert to data
generic filter 4, attributes
return filtered df


