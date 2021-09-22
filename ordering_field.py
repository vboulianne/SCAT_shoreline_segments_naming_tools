


# ============== OVERVIEW =================

# 1. Use identity to identity to give the grid Name value to segment. (Analysis Tools/Overlay/Identity)

# 2. Use clip to select according to a specify grid cell OR Select all the segments with the same grid cell => a list of list:  mast_list[GridCell][Segment]
# 3. For segment calculate distance with each other segment NOT ordered yet by using a list (initial list is a copy of distance_list = master_list[GridCell][1:]) (***Ideallly from the whole geometry not the centroid so connected lines would be the closest***) and put in a list
# 4. Name with next sequential number the segment at minimal distance. 
# 5. Remove newly named segemnt from distance_list
# 6. Select newly named segment and loop to 3 until no remained segment unnamed.

# #. Create special cases for archipelagos.


# =========================================



###### IMPORT MODULES ######

import arcpy
import os
import locale
from uuid import uuid4
arcpy.env.overwriteOutput = True
#arcpy.env.scratchWorkspace = "c:/GIS/Shoreline/Scratch"

# Declarations

# TODO: Find how to specify in the working directory of loaded datasets or input dataset
# arcpy.env.workspace = arcpy.GetParameterAsText(2) # Set ArcGIS workspace 

###### FUNCTIONS ######



def initiate_shoreline_segments_naming():

    testmode = 1

    if testmode == 0:

        ###### INPUT - TOOL GUI ######

        shoreline_file = arcpy.GetParameterAsText(0)
        shoreline_order_field = arcpy.GetParameterAsText(1)
        pace = arcpy.GetParameterAsText(2)
        process_output = arcpy.GetParameterAsText(3)



    elif testmode == 1:
        
        ###### INPUT - STATIC #######

        shoreline_file = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_bay_of_fundy"
        shoreline_order_field = "OBJECTID"
        pace = 100
        process_output = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_" + str(uuid4()).replace("-", "")

    

    shln_to_process = arcpy.CopyFeatures_management(in_features=shoreline_file, out_feature_class="in_memory\shln_proc_" + str(uuid4()).replace("-", ""))

    arcpy.AddField_management(shln_to_process, "SEQUENTIAL_NO", "LONG", 9, field_alias="Segment Sequential Number", field_is_nullable="NULLABLE")


        # SQL query create a subgroup by sector and afterward named sequentially in ascending order of their "OBJECTID"
    sql_clause_ord = (None, "ORDER BY " + shoreline_order_field + " ASC")
    with arcpy.da.UpdateCursor(shln_to_process, [shoreline_order_field, "SEQUENTIAL_NO"], sql_clause=sql_clause_ord) as cursor:
        for row in cursor:
            row[1] = row[0]*pace
            cursor.updateRow(row)

    shln_processed = shln_to_process


    ###### OUTPUT ######
    arcpy.CopyFeatures_management(shln_processed, process_output)
    print("Processed shoreline written to " + process_output)



        
if __name__ == '__main__':

    lic_arcinfo_status = arcpy.CheckProduct("arcinfo")
    lic_spatial_analyst_status = arcpy.CheckExtension("spatial")

    #if lic_arcinfo_status == "AlreadyInitalized":  # check licenses (p.117)
    #    pass
    #elif  lic_arcinfo_status == "Available" or :
    #    pass
    #else:
        # Exit script gracefully
    
    # if lic_spatial_analyst_status = "Available":
    #    arcpy.CheckOutExtension("spatial")

    initiate_shoreline_segments_naming() # main function

    arcpy.CheckInExtension("spatial")
    arcpy.CheckInExtension("arcinfo")

