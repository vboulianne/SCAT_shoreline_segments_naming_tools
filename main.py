


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
arcpy.env.overwriteOutput = True

# Declarations

# TODO: Find how to specify in the working directory of loaded datasets or input dataset
# arcpy.env.workspace = arcpy.GetParameterAsText(2) # Set ArcGIS workspace 

# Functions
def unique(input_list):
    
    # insert the list to the set
    list_set = set(input_list)
    # convert the set to the list
    unique_list = (list(list_set))
    for x in unique_list:
        print (x)
    return unique_list



def initiate_shoreline_segments_naming():

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

    shoreline_to_process = r"C:\GIS\Shoreline\Shoreline_Database.gdb\shoreline_classification_bay_of_fundy"
    segment_processed = r"C:\GIS\Shoreline\Shoreline_Database.gdb\shln_bof_1segment"
    reference_grid = r"C:\GIS\Shoreline\code_sgmt_naming\nts_grid\nts_grid.shp"
    #islands_ordered = arcpy.GetParameterAsText(2)
    shoreline_order_field = "OBJECTID"
    shoreline_field_id = "UNIQUEID"
    #island_order_field = arcpy.GetParameterAsText(4)
    output = r"C:\GIS\Shoreline\Output\output14.shp"
    shoreline_processed_path = r"C:\GIS\Shoreline\Output"
    shoreline_processed_name = r"shoreline_with_name.shp"
    output_test = r"C:\GIS\Shoreline\shln_naming_work.gdb\scratch\test6"
    #arcpy.env.workspace = r"C:\GIS\Shoreline"
    method = 2

    


    ########### CHECKS #################
    # Check is line/polyline
    # Check if shoreline and grid feature classes is projected properly. If not exit.

    ########### CREATE LOGIC ##############

    # arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


    # Attribute Grid to Segment

    # Create will be problematic shln_proximity_table =  arcpy.GenerateNearTable_analysis(in_features=shoreline_to_process, near_features=shoreline_to_process, out_table="C:/GIS/Shoreline/Shoreline_Database.gdb/shln_northern_bc_proximity_table", search_radius="", location="NO_LOCATION", angle="NO_ANGLE", closest="CLOSEST", closest_count="0", method="GEODESIC")

    shln_to_process_with_grid = arcpy.SpatialJoin_analysis(target_features=shoreline_to_process , join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")
    #shln_processed = arcpy.CreateFeatureclass_management(out_path=shoreline_processed_path, out_name=shoreline_processed_name, geometry_type="POLYLINE", template=shln_to_process_with_grid, has_m="DISABLED", has_z="DISABLED", spatial_reference="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")
    shln_processed = arcpy.Copy_management(shln_to_process_with_grid)
    arcpy.TruncateTable_management(shln_processed)




    ########## GROUP SEGMENTS BY SECTOR ##############

# Search Unique Values of grid for shapefile and put in list

    values_list = []
    segments_id_remaining = []
    with arcpy.da.SearchCursor(shln_to_process_with_grid,("UNIQUEID", "NTS_SNRC")) as cursor:
        for row in cursor:
            segments_id_remaining.append(row[0])
            values_list.append(row[1])
    sector_list = list(set(values_list))

    sector_count = 0
    for sector in  sector_list:

        '''
        Various methods to name sequentially. Choose one.
        Method 1: Use an ordered field. 
        Method 2: Use segment proximity
        
        '''

        if method == 1:

            # LOOP


            # Select all segments within grid sector
        



            
            '''
            Current problem. 
            arcpy.Select_analysis create a separate output feature and is not a selection in the current 
            '''

            # TODO: Work up to here 


            sql_clause_ord = (None, "ORDER BY " + shoreline_order_field + " ASC")



            num_seq = 1
            with arcpy.da.UpdateCursor(shln_to_process_with_grid, ["NAME_EN"], where_clause="NTS_SNRC='" + sector + "'", sql_clause=sql_clause_ord) as cursor:
                for row in cursor:
                    row[0] = sector + "-" +  str(num_seq).zfill(4)
                    cursor.updateRow(row)
                    num_seq += 1


        
        elif method == 2:

            # List has to be created from which segments can be deleted after being named. Current segment would not be in that list. Then spatial join can be used to select the closest next segment. 

            # Select First Segment

            segments_remaining = arcpy.Select_analysis(in_features=shln_to_process_with_grid, where_clause="NTS_SNRC='" + sector + "'")
            #arcpy.Copy_management(segments_remaining , output_test)

            sql_clause_ord = (None, "ORDER BY TARGET_FID ASC")
            num_seq = 1

            with arcpy.da.UpdateCursor(segments_remaining, ["*"], sql_clause=sql_clause_ord) as segments_remaining_cursor:
                
                for segment in segments_remaining_cursor:

                    if num_seq == 1:
                        segment[5] = segment[6] = sector + "-0001"

                        segments_remaining_cursor.deleteRow()
                        segment_id_processed = segment[4]
                        segments_id_remaining.remove(segment_id_processed)
                        segment_processed = arcpy.Select_analysis(in_features=segments_remaining, where_clause="UNIQUEID='" + segment_id_processed + "'")
                        num_seq += 1

                        # near_table = arcpy.GenerateNearTable_analysis(segment, segments_remaining, closest="CLOSEST", method="GEODESIC", out_table="C:\GIS\Shoreline\Scratch\near_table.shp")
                    break 
                near_table = arcpy.GenerateNearTable_analysis(segment_processed, segments_remaining, closest="CLOSEST", method="GEODESIC")

            with arcpy.da.InsertCursor(shln_processed, "*") as shln_processed_cursor:
                shln_processed_cursor.insertRow(segment)
            arcpy.Copy_management(shln_processed , output_test)
            '''
            with arcpy.da.SearchCursor(near_table, "*") as cursor:
                for row in cursor:
                    #segment = row
                    segment_id = row[2]
                    break
                print("Step 2")
            break

            while segments_id_remaining > 0:
                with arcpy.da.UpdateCursor(segments_remaining,"*", where_clause= "OBJECTID =" + segment_id) as cursor:

                    for segment in cursor: 
                        segment[5] = segment[6] = sector + "-" +  str(num_seq).zfill(4)

                        segments_remaining_cursor.deleteRow()
                        segment_id_processed = segment[0]
                        # segments_id_remaining.remove(segment_id_processed)
                        break
                with arcpy.da.InsertCursor(shln_processed, "*") as shln_processed_cursor:
                    shln_processed_cursor.insertRow(segment)
                near_table = arcpy.GenerateNearTable_analysis(segment, segments_remaining, closest="CLOSEST", method="GEODESIC", out_table="C:\GIS\Shoreline\Scratch\NearTable.shp")

                with arcpy.da.SearchCursor(near_table, "*") as cursor:
                    for row in cursor:
                        # segment = row
                        segment_id = row[0]
                        break

                            # End Select First segment
            


        sector_count += 1
    # arcpy.DeleteField_management(outFeatureClass, ["join_count", "SRID", "TARGET_FID"])
    # arcpy.Copy_management(shln_to_process_with_grid, output)
'''


        
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

