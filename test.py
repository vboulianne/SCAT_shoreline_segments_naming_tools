
# Reads the fields in a feature class
'''
import arcpy

featureClass = r'C:\GIS\Shoreline\shln_bay_of_fundy.shp'

def unique(input_list):
     
    # insert the list to the set
    list_set = set(input_list)
    # convert the set to the list
    unique_list = (list(list_set))
    for x in unique_list:
        print x
#    return unique_list

values_list = []
with arcpy.da.SearchCursor(featureClass,("SUBGROUP_E", "DATASOURCE")) as cursor:
    for row in cursor:
        values_list.append(row[0])
list_set = set(values_list)
grid_list = list(list_set)
print grid_list

'''

import arcpy
tools = arcpy.ListTools("*_analysis")
for tool in tools:
	print arcpy.Usage(tool)