import pandas as pd
from .filter_functions import get_Colored_Col as get_Col_OR_Shape
from .filter_functions import get_Colored_AND_Shaped
from .filter_functions import get_unique_values as to_set

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










