import os
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from pm4py.objects.conversion.log import converter as log_converter
from .filter_functions import get_Colored_Col as get_Col_OR_Shape
from .filter_functions import get_Colored_AND_Shaped
from .filter_functions import get_unique_values as to_set
from .filter_functions import getAttributeNames
from .filter_functions import sortByAttribute as sort_df

def convertLogToDf(file_dir):

    name, extension = os.path.splitext(file_dir)

    if (extension == ".xes"):
        xes_log = xes_importer_factory.apply(file_dir)
        df_event_log = log_converter.apply(xes_log, variant=log_converter.Variants.TO_DATA_FRAME)
        log_level_attributes = [attr for attr in getAttributeNames(df_event_log) if 'case:' in attr]
        case_level_attributes = [attr for attr in getAttributeNames(df_event_log) if attr not in log_level_attributes]
        log_level_attributes = [attr[5:] for attr in log_level_attributes]
        return df_event_log, case_level_attributes, log_level_attributes

    else: #(extension == ".csv"):
        df_event_log = pd.read_csv(file_dir)
        if (not checkCommaSeparated(df_event_log)):
            separator = ';'
            if separator in df_event_log.columns[0]:
                df_event_log = pd.read_csv(file_dir, sep=separator)
        return df_event_log, getAttributeNames(df_event_log),[]

#checks if Dataframe is Comma-Separated, returns True if it is, used in covert_log_to_df function
def checkCommaSeparated(df):
    if len ((df.columns)) != 1:
        return True


#extract user settings from dropdown menu
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

#create lists for labelling of axes, data points for plot, attribute values for legend
def data_points(df, attr_dict):
    axes_only, complete, selection_list = selection(attr_dict)
    labels_list = [selection_list[0], selection_list[1], 'Choose here', 'Choose here']

    if axes_only:
        data_points_list = [df[selection_list[0]].tolist(), df[selection_list[1]].tolist()]
        return labels_list, data_points_list, []
    elif complete:
        labels_list[2], labels_list[3] = selection_list[2], selection_list[3]
        data_points_list = [get_Colored_AND_Shaped(df, selection_list[2],selection_list[3],selection_list[0]),
                            get_Colored_AND_Shaped(df, selection_list[2],selection_list[3],selection_list[1])]
        legend_list = [to_set(df, selection_list[2]).tolist(), to_set(df,selection_list[3]).tolist()]
        return labels_list, data_points_list, legend_list

    else:
        if selection_list[2] is not None:
            labels_list[2] = selection_list[2]
            selection_list = selection_list[:3]
        else:
            labels_list[3] = selection_list[3]
            selection_list = selection_list[:2] + [selection_list[3]]

        legend_list = [to_set(df, selection_list[2]).tolist()]
        data_points_list = [get_Col_OR_Shape(df, selection_list[2], selection_list[0]),
                             get_Col_OR_Shape(df, selection_list[2], selection_list[1])]
        return labels_list, data_points_list, legend_list

def sorted_data_points(df,attr_dict,sort_attr):
    return data_points(sort_df(df,sort_attr),attr_dict)








