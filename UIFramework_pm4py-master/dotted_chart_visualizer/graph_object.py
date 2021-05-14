class dottedChartAbstract:
 
    def __init__(self, attributes, eventlog, valid, dataframe):
     self.attribute_list=attributes
     self.eventlog= eventlog
     self.valid = valid #syntaxcheck ok
     self.dataframe = dataframe
     self.attribute_dic=dict(zip(["x_axis","y_axis","color","shape"], attributes))