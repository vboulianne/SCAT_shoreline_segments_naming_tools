# ============== OVERVIEW =================

# 1. Use identity to identity to give the grid Name value to segment. (Analysis Tools/Overlay/Identity)

# 2. Use clip to select according to a specify grid cell OR Select all the segments with the same grid cell => a list of list:  mast_list[GridCell][Segment]
# 3. For segment calculate distance with each other segment NOT ordered yet by using a list (initial list is a copy of distance_list = master_list[GridCell][1:]) (***Ideallly from the whole geometry not the centroid so connected lines would be the closest***) and put in a list
# 4. Name with next sequential number the segment at minimal distance. 
# 5. Remove newly named segemnt from distance_list
# 6. Select newly named segment and loop to 3 until no remained segment unnamed.

# #. Create special cases for archipelagos.


# =========================================



# Import modules

import arcpy
import os
import locale
from uuid import uuid4
arcpy.env.overwriteOutput = True
#arcpy.env.scratchWorkspace = "c:/GIS/Shoreline/Scratch"

# Declarations

# TODO: Find how to specify in the working directory of loaded datasets or input dataset
# arcpy.env.workspace = arcpy.GetParameterAsText(2) # Set ArcGIS workspace 




# Input feature classes - static

#shoreline_to_process = r"C:\GIS\Shoreline\shln_bay_of_fundy.shp"
#reference_grid = r"C:\GIS\Shoreline\Data\nts_snrc\nts_snrc_50k.shp"

# Input from tool gui
'''
shoreline_to_process = arcpy.GetParameterAsText(0)
reference_grid = arcpy.GetParameterAsText(1)
method = arcpy.GetParameterAsText(2)
islands_ordered = arcpy.GetParameterAsText(3)
shoreline_order_field = arcpy.GetParameterAsText(4)
island_order_field = arcpy.GetParameterAsText(5)
output = arcpy.GetParameterAsText(6)
'''

shoreline = r"C:\GIS\Shoreline\Shoreline_Database.gdb\shoreline_classification_bay_of_fundy"
segment_processed = r"C:\GIS\Shoreline\Shoreline_Database.gdb\shln_bof_1segment"
reference_grid = r"C:\GIS\Shoreline\code_sgmt_naming\grid\nts_grid.shp"
#islands_ordered = arcpy.GetParameterAsText(2)
shoreline_order_field = "OBJECTID"
shoreline_field_id = "UNIQUEID"
#island_order_field = arcpy.GetParameterAsText(4)
output = r"C:\GIS\Shoreline\Output\output14.shp"
shoreline_processed_path = r"C:\GIS\Shoreline\Output"
shoreline_processed_name = r"shoreline_with_name.shp"
output_test = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_"  +  str(uuid4()).replace("-", "")
#arcpy.env.workspace = r"C:\GIS\Shoreline"
method = 2
scriptPath = sys.argv[0]
dataPath = os.path.dirname(os.path.dirname(scriptPath))
output_symbology = os.path.join(dataPath, "process_output_symbology.lyr")

print(scriptPath)
print(dataPath)
print(output_symbology)

########### CHECKS #################
# Check is line/polyline
# Check if shoreline and grid feature classes is projected properly. If not exit.

########### CREATE LOGIC ##############

# arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


# Attribute Grid to Segment

# Create will be problematic shln_proximity_table =  arcpy.GenerateNearTable_analysis(in_features=shoreline_to_process, near_features=shoreline_to_process, out_table="C:/GIS/Shoreline/Shoreline_Database.gdb/shln_northern_bc_proximity_table", search_radius="", location="NO_LOCATION", angle="NO_ANGLE", closest="CLOSEST", closest_count="0", method="GEODESIC")

#segments_remaining = arcpy.SpatialJoin_analysis(target_features=shoreline_to_process, out_feature_class="in_memory\shln_grid_" + str(uuid4()).replace("-", ""),  join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")
shln_to_process = arcpy.CopyFeatures_management(in_features=shoreline, out_feature_class="in_memory\shln_proc_" + str(uuid4()).replace("-", ""))
#arcpy.DeleteRows_management(in_rows=shln_processed)
#arcpy.GenerateNearTable_analysis(segment_processed, shln_to_process_with_grid, out_table="in_memory\prox_tbl_" +  str(uuid4()).replace("-", ""),  closest="CLOSEST", method="GEODESIC")
# arcpy.GenerateNearTable_analysis(segment_processed, shln_to_process_with_grid, out_table="C:\GIS\Shoreline\Scratch\prox_tbl_" +  str(uuid4()).replace("-", "") + ".shp",  closest="CLOSEST", method="GEODESIC")


#arcpy.Select_analysis(in_features=segments_remaining, out_feature_class="in_memory\seg_proc" + str(uuid4()).replace("-", ""), where_clause="UNIQUEID='190'")
#print(output_test)
arcpy.CopyFeatures_management(shln_to_process, output_test)

# arcpy.AddField_management(shln_to_process,"SEQUENTIAL_NO", "LONG")



#field_index = arcpy.ListIndexes(shln_to_process)

#print(field_index)


if output_symbology != "":
    params = arcpy.GetParameterInfo()
    params[2].symbology = output_symbology