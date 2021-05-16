from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from os import listdir
from os.path import isfile, join
from django.conf import settings
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter

from pm4py.algo.filtering.pandas.attributes.attributes_filter import apply as df_filter

class graphData:
    def __init__(self):
        self.name= self.retrieve_file()[0]
        self.attributes=attributes_all
        self.attributes_selected= attributes_selected

    def retrieve_file(self):
        event_log = settings.EVENT_LOG_NAME
        name, extension = os.path.splitext(event_log)
        return name,extension

    def convert_log_to_df(self):
        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
        event_log_file_path = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)

        if self.retrieve_file()[1] == ".xes":
            variant = xes_importer.Variants.ITERPARSE
            parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
            log = xes_importer.apply('event_log_file', variant=variant, parameters=parameters)
            df_event_log = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
            return df_event_log

        elif extension == ".csv":
            df_event_log = pd.read(event_log_file_path, 'r')
            return df_event_log

#def filter_df(set_attributes): #set_attributes as [4] or {}
    #for attribute in set_attributes:
    #return filtered_df
# generic filter 4, attributes
# return filtered df
