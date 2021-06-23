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
import datetime



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
        print("index out of bounds")


# returns the event log sorted by a specific attribute, attribute index needed
def sortByAttribute(df, attribute):
    return df.sort_values(by=[attribute])


# reduces the number of events of the event log down to a specific range with start and end index
def delimitNumberOfEvents(df, startIndex, endIndex):
    if (startIndex < endIndex) & (startIndex >= 0) & (endIndex < len(df)):
        try:
            return df.iloc[startIndex: endIndex]
        except:
            print("Error")


# returns only the events of a specific trace with index traceIndex
def getTrace(df, traceIndex):
    index = "trace " + str(traceIndex)
    return df.loc[df['case'] == index]


# returns the Cases/Traces and Events/Activity Columns of a dataframe (for the default option of the plot)
def setDefault(df):
    pattern = re.compile("case:concept.*|(C|c)ase.*|(T|t)race.*")
    x_label = None
    x_column = None

    for col in df.columns:
        match = pattern.match(col)

        if match is None:
            pass
        else:
            x_label = match.group()
            break

    pattern = re.compile("concept.*|(E|e)vent.*|(A|a)ctivit.*")
    y_label = None
    y_column = None

    for col in df.columns:
        match = pattern.match(col)

        if match is None:
            pass
        else:
            y_label = match.group()
            break

    if ((x_label is None) & (y_label is None)):
        x_column = df.iloc[:, 0]
        y_column = df.iloc[:, 1]
        x_label = df.columns[0]
        y_label = df.columns[1]
    elif ((x_label is None) & (y_label is not None)):
        x_column = df.iloc[:, 0]
        y_column = df[y_label]
        x_label = df.columns[0]
    elif ((x_label is not None) & (y_label is None)):
        x_column = df[x_label]
        y_column = df.iloc[:, 1]
        y_label = df.columns[1]
    else:
        x_column = df[x_label]
        y_column = df[y_label]

    x_column = x_column.tolist()
    y_column = y_column.tolist()
    x_axis_order = get_unique_values(df, x_label).tolist()
    y_axis_order = get_unique_values(df, y_label).tolist()[::-1]
    return [x_column, y_column], x_label, y_label, [x_axis_order, y_axis_order]


def get_unique_values(df, col_name):
    return df[col_name].unique()


def get_Colored_Values(df, color_att, color_val, target_att):
    # filter rows where color_att is equal to color_val
    df_color = df.loc[df[color_att] == color_val]
    # reduce to target column
    df_color_col = df_color[target_att]
    # convert to list
    return list(df_color_col.values.tolist())


# returns a list of lists where each inner list is the values of the column specified by target index
# where the values of this column are equal to a unique value of the color column
def get_Colored_Col(df, color_att, target_att):
    unique_vals = get_unique_values(df, color_att)
    col_list = []
    for val in unique_vals:
        val_list = get_Colored_Values(df, color_att, val, target_att)
        col_list.append(val_list)
    return col_list


def get_Colored_And_Shaped_Values(df, color_att, color_val, shaped_att, shaped_val, target_att):
    # filter rows where color_att is equal to color_val
    df_color = df.loc[df[color_att] == color_val]
    df_color_shape = df_color.loc[df_color[shaped_att] == shaped_val]
    # reduce to target column
    target_col = df_color_shape[target_att]
    # convert to list
    return list(target_col.values.tolist())


def get_Colored_AND_Shaped(df, color_att, shaped_att, target_att):
    unique_colored = get_unique_values(df, color_att)
    unique_shaped = get_unique_values(df, shaped_att)
    res_list = []
    for u in unique_colored:
        for v in unique_shaped:
            val_list = get_Colored_And_Shaped_Values(df, color_att, u, shaped_att, v, target_att)
            res_list.append(val_list)
    return res_list

# new helper functions
def getCaseIndex(df):
    pattern = re.compile(".*(C|c)ase.*")
    caseLabel = -1
    caseIndex = None
    caseFoundList = []

    for col in df.columns:
        match = pattern.match(col)

        if match is None:
            pass
        else:
            caseLabel = match.group()
            caseFoundList.append(caseLabel)

    if (len(caseFoundList) == 1):
        caseIndex = df.columns.get_loc(caseLabel)
    if (len(caseFoundList) > 1):
        caseIndex = df.columns.get_loc("case:concept:name")
        caseLabel = "case:concept:name"
    if (caseIndex == -1):
        print("ERRRRORRRRR")
    return caseIndex


def getCaseLabel(df):
    return df.columns[getCaseIndex(df)]


def getTimeLabel(df):
    return df.columns[getTimeIndex(df)]


def getTimeIndex(df):
    pattern = re.compile(".*(T|t)ime.*")
    timeLabel = -1
    timeIndex = None
    timeFoundList = []
    match = None

    for col in df.columns:
        match = pattern.match(col)

        if match is None:
            pass
        else:
            timeLabel = match.group()
            timeFoundList.append(timeLabel)

    if (len(timeFoundList) == 1):
        timeIndex = df.columns.get_loc(timeLabel)
    if (len(timeFoundList) > 1):
        timeIndex = df.columns.get_loc("time:timestamp")
        timeLabel = "time:timestamp"
    if (timeIndex == -1):
        print("ERRRRORRRRR")
    return timeIndex



# Sorting Functions
def sortByTrace(df):
    caseLabel = getCaseLabel(df)
    return df.sort_values(by=[caseLabel])


def sortByTime(df):
    timeLabel = getTimeLabel(df)
    return df.sort_values(by=[timeLabel])


def sortByFirstInTrace(df, attr):
    caseLabel = getCaseLabel(df)
    dfu = get_unique_values(df, caseLabel)
    firstInTraceList = []
    for d in dfu:
        dfr = df.loc[df[caseLabel] == d]
        firstInTraceList.append(dfr.iloc[0])
    groupedDf = pd.DataFrame(firstInTraceList).sort_values([attr])
    caseIDList = groupedDf[caseLabel].tolist()
    return caseIDList


def sortByLastInTrace(df,attr):
    caseLabel = getCaseLabel(df)
    dfu = get_unique_values(df, caseLabel)
    firstInTraceList = []
    for d in dfu:
        dfr = df.loc[df[caseLabel] == d]
        firstInTraceList.append(dfr.iloc[-1])
    groupedDf = pd.DataFrame(firstInTraceList).sort_values([attr])
    caseIDList = groupedDf[caseLabel].tolist()
    return caseIDList


def sortyByTraceDuration(df):
    durationList = []
    traceList = []
    dfu = get_unique_values(df, getCaseLabel(df))
    for d in dfu:
        dfr = df.loc[df[getCaseLabel(df)] == d]
        finishTime = pd.to_datetime(dfr.iloc[-1][getTimeIndex(df)])
        startTime = pd.to_datetime(dfr.iloc[0][getTimeIndex(df)])
        duration = finishTime - startTime
        durationList.append(duration)
        traceList.append(d)
        trace_duration_df = pd.DataFrame(list(zip(traceList, durationList)), columns=['trace', 'duration'])
        td_sort = trace_duration_df.sort_values(by='duration', ascending=False)
    return td_sort.values.tolist()


# Converting TimeStamps

def convertStringToDateTime(date_string):
    format = "%Y-%m-%d %H:%M:%S"
    date_time_obj = datetime.datetime.strptime(date_string, format)
    return date_time_obj


def convertListOfStringsToDateTime(list_of_strings):
    res_list = []
    for l in list_of_strings:
        dt_obj = convertStringToDateTime(l)
        res_list.append(dt_obj)
    return res_list


# this one works best
def convertTimeStamps(df):
    timeIndex = getTimeIndex(df)
    if (isinstance(df.iloc[0, timeIndex], str)):
        df[getTimeLabel(df)] = pd.to_datetime(df[getTimeLabel(df)])
    return df


# returns the values of the time column converted from date time to string
def convertDateTimeToString(df):
    timeIndex = getTimeIndex(df)
    strList = []
    for v in df.iloc[:, timeIndex]:
        u = v.strftime("%Y-%m-%d %H:%M:%S")
        strList.append(u)
    return strList


#converts date time objects of time column to string for df, no return value, df is changed
def convertDateTimeToStringsDf(df):
    timeIndex = getTimeIndex(df)
    if(not isinstance(df.iloc[0,timeIndex],str)):
        for i in range(0, len(df)):
            df.iloc[i, getTimeIndex(df)] = df.iloc[i, getTimeIndex(df)].strftime("%Y-%m-%d %H:%M:%S")


        
#renames column names to get prettier names, used for XES files

def renameXesColumns(df):
    df = df.rename(columns={getTimeLabel(df): "Time", getCaseLabel(df): "Case"})
    if ("org:resource" in df.columns):
        df = df.rename(columns={"org:resource": "Resource"})
    if ("concept:name" in df.columns):
        df = df.rename(columns={"concept:name": "Activity"})
    if ("case:creator in df.columns"):
        df = df.rename(columns={"case:creator": "Creator"})
    if ("lifecycle:transition" in df.columns):
        df = df.rename(columns={"lifecycle:transition": "Lifecycle"})
    if ("case:description" in df.columns):
        df = df.rename(columns={"case:description": "Description"})
    for col in df.columns:
        if "case:" in col:
            prefix, colName = col.split(":")
            if colName.islower():
                firstLetter = colName[:1].upper()
                restWord = colName.split([colName[:1]])[1]
                res = ''.join([firstLetter, restWord])
                df = df.rename(columns={colName: res})
            else:
                df = df.rename(columns={col: colName})
    return df

# sorts