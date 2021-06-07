import pandas as pd
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

def to_set(list):
    return [i for j, i in enumerate(list) if i not in list[:j]]


def data_points(df, attr_dict):
    axes_only, complete, selection_list = selection(attr_dict)
    labels_list = [selection_list[0], selection_list[1], 'Choose here', 'Choose here']

    if axes_only:
        data_points_list = [df[selection_list[0]].tolist(), df[selection_list[1]].tolist()]
        return labels_list, data_points_list, []
    elif complete:
        xaxis_list = []
        yaxis_list = []
        labels_list[2], labels_list[3] = selection_list[2], selection_list[3]
        color_values = df[selection_list[2]].tolist()
        color_values_set = to_set(color_values)
        shape_values = df[selection_list[3]].tolist()
        shape_values_set = to_set(shape_values)
        df_filtered = df[selection_list]

        for color_value in color_values_set:
            for shape_value in shape_values_set:
                xaxis_list.append(df_filtered.loc[(df_filtered[selection_list[2]] == color_value) & (
                            df_filtered[selection_list[3]] == shape_value)][selection_list[0]].values.tolist())
                yaxis_list.append(df_filtered.loc[(df_filtered[selection_list[2]] == color_value) & (
                            df_filtered[selection_list[3]] == shape_value)][selection_list[1]].values.tolist())

        data_points_list = [xaxis_list, yaxis_list]
        legend_list = [color_values_set, shape_values_set]
        return labels_list, data_points_list, legend_list

    else:
        if selection_list[2] is not None:
            values_set = to_set(df[selection_list[2]].tolist())
            legend_list = [values_set]
            labels_list[2] = selection_list[2]
            selection_list = selection_list[:3]
        else:
            values_set = to_set(df[selection_list[3]].tolist())
            legend_list = [values_set]
            labels_list[3] = selection_list[3]
            selection_list = selection_list[:2] + [selection_list[3]]

        xaxis_list = []
        yaxis_list = []
        df_filtered = df[selection_list]
        for value in values_set:
            xaxis_list.append(df_filtered.loc[df_filtered[selection_list[2]] == value][selection_list[0]].values.tolist())
            yaxis_list.append(df_filtered.loc[df_filtered[selection_list[2]] == value][selection_list[1]].values.tolist())
        return labels_list, [xaxis_list, yaxis_list], legend_list






