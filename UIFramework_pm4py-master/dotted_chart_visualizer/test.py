import pandas as pd
def selection(selection_dict):
    selection_list = [selection_dict["xaxis_choice"], selection_dict["yaxis_choice"], None, None]
    axes_only = True
    complete = True #TODO: change when 3/4 attributes selected implemented
    if selection_dict["color_choice"] != "Choose here":
        selection_list[2] = selection_dict["color_choice"]
        axes_only = False

    if selection_dict["shape_choice"] != "Choose here":
        selection_list[3] = selection_dict["shape_choice"]
        axes_only = False
        if selection_list[2] != None:
            complete = True
    return axes_only, complete, selection_list

#def getAttribute(df, attributeName):
    #return df[attributeName].tolist()


def data_points(df, attr_dict):
    axes_only, complete, selection_list = selection(attr_dict)
    labels_list = [selection_list[0], selection_list[1], None, None]

    if axes_only:
        data_points_list = [df[selection_list[0]].tolist(), df[selection_list[1]].tolist(), None, None]
        return labels_list, data_points_list, None
    elif complete:
        xaxis_list = []
        yaxis_list = []
        labels_list[2], labels_list[3] = [selection_list[2], selection_list[3]]
        color_values = df[selection_list[2]].tolist()
        color_values_set = [i for j, i in enumerate(color_values) if i not in color_values[:j]]
        shape_values = df[selection_list[3]].tolist()
        shape_values_set = [i for j, i in enumerate(shape_values) if i not in shape_values[:j]]
        df_filtered = df[selection_list]

        for color_value in color_values_set:
            for shape_value in shape_values_set:
                xaxis_list.append(df_filtered.loc[(df_filtered[selection_list[2]] == color_value) & (
                            df_filtered[selection_list[3]] == shape_value)][selection_list[0]].values.tolist())
                yaxis_list.append(df_filtered.loc[(df_filtered[selection_list[2]] == color_value) & (
                            df_filtered[selection_list[3]] == shape_value)][selection_list[1]].values.tolist())
                # print(df_filtered.loc[(df_filtered[selection_list[2]] == color_value) & (df_filtered[selection_list[3]] == shape_value)])
                # print(yaxis_list)
                # print(shape_values_set)
                # print(color_values_set)
                data_points_list = [xaxis_list, yaxis_list]
        # print(selection_list)
        legend_list = [color_values_set, shape_values_set]
        return labels_list, data_points_list, legend_list






