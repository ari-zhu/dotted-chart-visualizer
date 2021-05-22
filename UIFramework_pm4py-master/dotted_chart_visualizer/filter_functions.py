import os
from os import listdir
from os.path import isfile, join

from django.conf import settings
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from pm4py.objects.conversion.log import converter as log_converter
from django.shortcuts import render
import re

def convert_log_to_df(request):
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    file_dir = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)

    name, extension = os.path.splitext(file_dir)

    if (extension == ".xes"):
        xes_log = xes_importer_factory.apply(file_dir)
        df_event_log = log_converter.apply(xes_log, variant=log_converter.Variants.TO_DATA_FRAME)

    elif (extension == ".csv"):
        csv_log = log_converter.apply(file_dir)
        df_event_log = log_converter.apply(csv_log, variant=log_converter.Variants.TO_DATA_FRAME)
        
        if (checkCommaSeparated(df_event_log)):
            pass
        else:
            df_event_log = log_converter.apply(csv_log, variant=log_converter.Variants.TO_DATA_FRAME, sep=';')
  
            
    else:
        event_logs = [f for f in listdir(event_logs_path) if isfile(join(event_logs_path, f))]
        message = "Unsupported file type"
        return render(request, 'upload.html', {'eventlog_list': event_logs, 'message': message})

    return df_event_log


# returns the number of events of event log df
def getNumberOfEvents(df):
    return len(df)

# returns the number of attributes of event log df
def getNumberOfAttributes(df):
    return len(df.columns)

# returns an list of the attribute names of event log df
def getAttributeNames(df):
    return list(df.columns.values.tolist())

# prints out the attribute names of event log df
def printAttributeNames(df):
    for col in df.columns:
        print(col)
        
# returns an array that contains the values of a specific attribute of event log df
# index of the attibute is needed, to do: get attribute by name
def getAttribute(df, attributeIndex):
    if (attributeIndex < len(df.columns)):
        return df.iloc[:, attributeIndex]
    else:
        print ("index out of bounds")

# returns the event log sorted by a specific attribute, attribute index needed        
def sortByAttribute(df, attributeIndex):
    return df.sort_values(by = df.columns[attributeIndex])

# reduces the number of events of the event log down to a specific range with start and end index
def delimitNumberOfEvents(df, startIndex, endIndex):
    if (startIndex < endIndex) &(startIndex >= 0) &(endIndex < len(df)):
        try:
            return df.iloc[startIndex : endIndex]
        except:
            print("Error")
            
# returns only the events of a specific trace with index traceIndex
def getTrace (df, traceIndex):
    index = "trace " + str(traceIndex)
    return df.loc [df['case'] == index]

#checks if Dataframe is Comma-Separated, returns True if it is, used in covert_log_to_df function
def checkCommaSeparated(df):
    if len ((df.columns) != 1):
        return True
    
#returns the Cases/Traces and Events/Activity Columns of a dataframe (for the default option of the plot)
def setDefault (df):
    pattern = re.compile("(C|c)ase.*|(T|t)race.*")
    match1 = None
        
    for col in df.columns:
        match = pattern.match(col)
    
        if match is None:
            pass
        else:
            match1 = match.group()
            break;
    
    pattern = re.compile("(E|e)vent.*|(A|a)ctivit.*")
    match2 = None
        
    for col in df.columns:
        match = pattern.match(col)
    
        if match is None:
            pass
        else:
            match2 = match.group()
            break;
    if((match1 is None) & (match2 is None)):
        return df.iloc[:,0], df.iloc[:,1]
    else: 
        return df[match1], df[match2]
    