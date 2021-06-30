import os
import pandas as pd
import re
import numpy as np
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from pm4py.objects.conversion.log import converter as log_converter
from .filter_functions import get_Colored_Col as get_Col_OR_Shape
from .filter_functions import get_Colored_AND_Shaped
from .filter_functions import get_unique_values as to_set
from .filter_functions import getAttributeNames
from .filter_functions import getTimeLabel
from .filter_functions import renameXesColumns
from .filter_functions import sortByAttribute as sort_df


def extract_attr_log_level(df):
    log_level_attributes = [attr for attr in getAttributeNames(df) if 'case' in attr]
    return log_level_attributes


def extract_attr_case_level(df, log_level_attributes):
    case_level_attributes = [attr for attr in getAttributeNames(df) if attr not in log_level_attributes]
    return case_level_attributes


def extract_attribute_value(log_object, event, attribute):
    pass


def convertLogToDf(file_dir):
    name, extension = os.path.splitext(file_dir)

    if (extension == ".xes"):
        xes_log = xes_importer_factory.apply(file_dir)
        df_event_log = log_converter.apply(xes_log, variant=log_converter.Variants.TO_DATA_FRAME)
        df_event_log = df_event_log.replace(np.nan, 0)
        log_level_attributes = extract_attr_log_level(df_event_log)
        case_level_attributes = extract_attr_case_level(df_event_log, log_level_attributes)
        # log_level_attributes = [attr[5:] for attr in log_level_attributes]
        return df_event_log, case_level_attributes, log_level_attributes

    else:  # (extension == ".csv"):
        df_event_log = pd.read_csv(file_dir, keep_default_na=False)
        if (not checkCommaSeparated(df_event_log)):
            separator = ';'
            if separator in df_event_log.columns[0]:
                print("I am here")
                df_event_log = pd.read_csv(file_dir, sep=separator, keep_default_na=False, parse_dates=False, infer_datetime_format= False)
        log_level_attr = extract_attr_log_level(df_event_log)
        case_level_attr = extract_attr_case_level(df_event_log,log_level_attr)
        return df_event_log, case_level_attr, log_level_attr


# checks if Dataframe is Comma-Separated, returns True if it is, used in covert_log_to_df function
def checkCommaSeparated(df):
    if len((df.columns)) != 1:
        return True

# check for NaNs and convert to String

#def replaceNaNs(df):
    #df.replace(np.nan,0)
    #return df


# extract user settings from dropdown menu
def selection(selection_dict):
    selection_list = [selection_dict["xaxis_choice"], selection_dict["yaxis_choice"], None, None]
    axes_only = True
    complete = False
    if selection_dict["color_choice"] != "Choose here":
        selection_list[2] = selection_dict["color_choice"]
        axes_only = False

    if selection_dict["shape_choice"] != "Choose here":
        selection_list[3] = selection_dict["shape_choice"]
        axes_only = False
        if selection_list[2] is not None:
            complete = True
    return axes_only, complete, selection_list


# create lists for labelling of axes, data points for plot, attribute values for legend
def data_points(df, attr_dict):
    axes_only, complete, selection_list = selection(attr_dict)
    labels_list = [selection_list[0], selection_list[1], 'Choose here', 'Choose here']

    if axes_only:
        data_points_list = [df[selection_list[0]].tolist(), df[selection_list[1]].tolist()]
        return labels_list, data_points_list, []
    elif complete:
        labels_list[2], labels_list[3] = selection_list[2], selection_list[3]
        data_points_list = [get_Colored_AND_Shaped(df, selection_list[2], selection_list[3], selection_list[0]),
                            get_Colored_AND_Shaped(df, selection_list[2], selection_list[3], selection_list[1])]
        legend_list = [to_set(df, selection_list[2]).tolist(), to_set(df, selection_list[3]).tolist()]
        return labels_list, data_points_list, legend_list

    else:
        if selection_list[2] is not None:
            labels_list[2] = selection_list[2]
            selection_list = selection_list[:3]
            legend_list = [to_set(df, selection_list[2]).tolist(), []]
        else:
            labels_list[3] = selection_list[3]
            selection_list = selection_list[:2] + [selection_list[3]]
            legend_list = [[], to_set(df, selection_list[2]).tolist()]

        # legend_list = [to_set(df, selection_list[2]).tolist()]
        data_points_list = [get_Col_OR_Shape(df, selection_list[2], selection_list[0]),
                            get_Col_OR_Shape(df, selection_list[2], selection_list[1])]
        return labels_list, data_points_list, legend_list


def appendColumn(df, newName, list, caseLabel):
    dfu = df[caseLabel].unique()
    series = []
    for i in range(len(list)):
        for k in df[caseLabel]:
            if k == dfu[i]:
                series += [list[i]]
    df[newName] = series
    return df



