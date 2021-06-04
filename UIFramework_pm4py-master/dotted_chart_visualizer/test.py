import pandas as pd

def data_points(df, attr_dict):
    data_points_list=[]
    labels_list =[]
    for label in attr_dict:
        attribute = attr_dict[label]
        if attribute in df.columns.tolist():
            data_points_list.append(df[attribute].tolist())
            labels_list.append(attribute)
        else:
            data_points_list.append(None)
            labels_list.append(None)
    return data_points_list, labels_list
