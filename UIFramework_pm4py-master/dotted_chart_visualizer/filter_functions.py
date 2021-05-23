import os
from os import listdir
from os.path import isfile, join

from django.conf import settings
import pandas as pd
from django.http import HttpResponse
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from pm4py.objects.conversion.log import converter as log_converter
from django.shortcuts import render
import re

def convertLogToDf(file_dir):

    name, extension = os.path.splitext(file_dir)

    if (extension == ".xes"):
        xes_log = xes_importer_factory.apply(file_dir)
        df_event_log = log_converter.apply(xes_log, variant=log_converter.Variants.TO_DATA_FRAME)
        return df_event_log

    else: #(extension == ".csv"):
        df_event_log = pd.read_csv(file_dir)
        if (not checkCommaSeparated(df_event_log)):
            separator = ';'
            if separator in df_event_log.columns[0]:
                df_event_log = pd.read_csv(file_dir, sep=separator)
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
    if len ((df.columns)) != 1:
        return True
    
#returns the Cases/Traces and Events/Activity Columns of a dataframe (for the default option of the plot)
def setDefault(df):
    pattern = re.compile("case:concept.*|(C|c)ase.*|(T|t)race.*")
    match1 = None

    for col in df.columns:
        match = pattern.match(col)

        if match is None:
            pass
        else:
            match1 = match.group()
            break;

    pattern = re.compile("concept.*|(E|e)vent.*|(A|a)ctivit.*")
    match2 = None

    for col in df.columns:
        match = pattern.match(col)

        if match is None:
            pass
        else:
            match2 = match.group()
            break;
    if ((match1 is None) & (match2 is None)):
        return df.iloc[:, 0], df.iloc[:, 1]

    elif ((match1 is None) & (match2 is not None)):
        return df.iloc[:, 0], df[match2]

    elif ((match1 is not None) & (match2 is None)):
        return df[match1], df.iloc[:, 1]
    else:
        return df[match1], df[match2]