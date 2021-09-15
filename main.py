


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

# Functions
''''
def unique(input_list):
    
    # insert the list to the set
    list_set = set(input_list)
    # convert the set to the list
    unique_list = (list(list_set))
    for x in unique_list:
        print (x)
    return unique_list
'''


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

    #shoreline_to_process = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_bay_of_fundy"
    shoreline_to_process = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_arctic_mb_nl_nt_nu_on_qc_yt"
    #segment_processed = r"C:\GIS\Shoreline\Shoreline_Database.gdb\shln_bof_1segment"
    reference_grid = "C:/GIS/Shoreline/code_sgmt_naming/nts_grid/nts_grid.shp"
    #islands_ordered = arcpy.GetParameterAsText(2)
    shoreline_order_field = "OBJECTID"
    shoreline_field_id = "TARGET_ID"
    #island_order_field = arcpy.GetParameterAsText(4)
    output = "C:/GIS/Shoreline/Output/output14.shp"
    shoreline_processed_path = r"C:\GIS\Shoreline\Output"
    shoreline_processed_name = r"shoreline_with_name.shp"
    output_test = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_" + str(uuid4()).replace("-", "")
    #shln_processed_file = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/shln_proc" + str(uuid4()).replace("-", "")
    #arcpy.env.workspace = r"C:\GIS\Shoreline"
    method = 2



    ########### CHECKS #################
    # Check is line/polyline
    # Check if shoreline and grid feature classes is projected properly. If not exit.

    ########### CREATE LOGIC ##############

    # arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


    # Attribute Grid to Segment

    # Create will be problematic shln_proximity_table =  arcpy.GenerateNearTable_analysis(in_features=shoreline_to_process, near_features=shoreline_to_process, out_table="C:/GIS/Shoreline/Shoreline_Database.gdb/shln_northern_bc_proximity_table", search_radius="", location="NO_LOCATION", angle="NO_ANGLE", closest="CLOSEST", closest_count="0", method="GEODESIC")

    shln_to_process_with_grid = arcpy.SpatialJoin_analysis(target_features=shoreline_to_process, out_feature_class="in_memory\shln_grid_" + str(uuid4()).replace("-", ""), join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")
    shln_processed = arcpy.CopyFeatures_management(in_features=shln_to_process_with_grid, out_feature_class="in_memory\shln_proc_" + str(uuid4()).replace("-", ""))
    #arcpy.CopyFeatures_management(in_features=shln_to_process_with_grid, out_feature_class=shln_processed_file)
    #arcpy.TruncateTable_management(shln_processed_file)
    #shln_processed = arcpy.CopyFeatures_management(in_features=shln_processed_file, out_feature_class="in_memory\shln_proc_" + str(uuid4()).replace("-", ""))


    # segs_rem = arcpy.CopyFeatures_management(in_features=shln_to_process_with_grid, out_feature_class="C:/GIS/Shoreline/Scratch/segs_rem" +str(uuid4()).replace("-", "") + ".shp")





    ########## GROUP SEGMENTS BY SECTOR ##############

# Search Unique Values of grid for shapefile and put in list

    values_list = []
    with arcpy.da.SearchCursor(shln_to_process_with_grid,("TARGET_FID", "NTS_SNRC")) as cursor:
        for row in cursor:
            values_list.append(row[1])
    sector_list = list(set(values_list))

    sector_count = 0
    for sector in sector_list:

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
            
            shln_processed = shln_to_process_with_grid



        
        elif method == 2:

            
            segments_remaining = arcpy.Select_analysis(in_features=shln_to_process_with_grid, out_feature_class="in_memory\seg_rem_" + str(uuid4()).replace("-", ""), where_clause="NTS_SNRC='" + sector + "'")
            
            segments_id_remaining = []
            segment_id = ""
            first_segment_id = ""
            with arcpy.da.SearchCursor(segments_remaining,("OBJECTID", "NTS_SNRC")) as cursor:
                for row in cursor:
                    segments_id_remaining.append(row[0])
            #arcpy.Copy_management(segments_remaining , output_test)

            ##### PROCESS FIRST SEGMENT ####

            num_seq = 1
            
            lstFields = arcpy.ListFields(segments_remaining)

            x = False
            for field in lstFields:
                if field.name == "sector_first_segment":
                    x = True

            if x == True:
                sql_clause_ord = (None, 'ORDER BY sector_first DESC')
                with arcpy.da.UpdateCursor(segments_remaining, ["*"], where_clause="sector_first_segment=1") as segments_remaining_cursor:
                
                    for segment in segments_remaining_cursor:

                        if num_seq == 1:
                            first_segment_id = segment[0]
                            segment_target_fid = segment[3]
                            segment_processed = arcpy.Select_analysis(in_features=segments_remaining, out_feature_class="in_memory\seg_proc" + str(uuid4()).replace("-", ""), where_clause="OBJECTID="+str(first_segment_id)+"")
                            segments_remaining_cursor.deleteRow()
                            
                            num_seq += 1
                            
                        break
            else:
                sql_clause_ord = (None, 'ORDER BY TARGET_FID ASC')
                with arcpy.da.UpdateCursor(segments_remaining, ["*"], sql_clause=sql_clause_ord) as segments_remaining_cursor:
                
                    for segment in segments_remaining_cursor:

                        if num_seq == 1:
                            first_segment_id = segment[0]
                            segment_target_fid = segment[3]
                            segment_processed = arcpy.Select_analysis(in_features=segments_remaining, out_feature_class="in_memory\seg_proc" + str(uuid4()).replace("-", ""), where_clause="OBJECTID="+str(first_segment_id)+"")
                            segments_remaining_cursor.deleteRow()
                            
                            num_seq += 1
                            
                        break


            '''
            with arcpy.da.UpdateCursor(segments_remaining, ["*"], sql_clause=sql_clause_ord) as segments_remaining_cursor:
                
                for segment in segments_remaining_cursor:

                    if num_seq == 1:
                        first_segment_id = segment[0]
                        segment_target_fid = segment[3]
                        segment_processed = arcpy.Select_analysis(in_features=segments_remaining, out_feature_class="in_memory\seg_proc" + str(uuid4()).replace("-", ""), where_clause="OBJECTID="+str(first_segment_id)+"")
                        segments_remaining_cursor.deleteRow()
                        
                        num_seq += 1
                        
                    break
            '''
            near_table = arcpy.GenerateNearTable_analysis(segment_processed, segments_remaining, out_table="in_memory\prox_tbl_" +  str(uuid4()).replace("-", ""),  closest="CLOSEST", method="GEODESIC")
            segments_id_remaining.remove(first_segment_id)

            
            with arcpy.da.SearchCursor(near_table, "*") as near_table_cursor:
                for row_table in near_table_cursor:
                    segment_id = row_table[2]
                    break
            
            with arcpy.da.UpdateCursor(shln_processed, "*", where_clause="TARGET_FID="+str(segment_target_fid)+"") as shln_processed_cursor:
                for segment in shln_processed_cursor:
                    segment[5] = sector + "-0001"
                    segment[6] = sector + "-0001"
                    shln_processed_cursor.updateRow(segment)
            
                arcpy.Delete_management(near_table)
                arcpy.Delete_management(segment_processed)

            #arcpy.CopyFeatures_management(shln_processed , output_test)

            ###### PROCESS THE REMAINING SEGMENTS ####
            while len(segments_id_remaining) > 0:
                # print("Next segment: " + str(segment_id) + "|| Segments remaining:" + str(len(segments_id_remaining)))
                with arcpy.da.UpdateCursor(segments_remaining,"*", where_clause="OBJECTID="+str(segment_id)+"") as segments_remaining_cursor:
                    
                    for segment in segments_remaining_cursor: 
                        segment_id = segment[0]
                        segment_target_fid = segment[3]
                        segment_processed = arcpy.Select_analysis(in_features=segments_remaining, out_feature_class="in_memory\seg_proc" + str(uuid4()).replace("-", ""), where_clause="OBJECTID="+str(segment_id)+"")
                        segments_remaining_cursor.deleteRow()
                        
                        break
                
                near_table = arcpy.GenerateNearTable_analysis(segment_processed, segments_remaining, out_table="in_memory\prox_tbl_" +  str(uuid4()).replace("-", ""),  closest="CLOSEST", method="GEODESIC")

                segments_id_remaining.remove(segment_id)

                with arcpy.da.SearchCursor(near_table, "*") as cursor:
                    for row in cursor:
                        # segment = row
                        segment_id = row[2]
                        
                        break
                arcpy.Delete_management(near_table)
                arcpy.Delete_management(segment_processed)

                with arcpy.da.UpdateCursor(shln_processed, "*", where_clause="TARGET_FID="+str(segment_target_fid)+"") as shln_processed_cursor:
                    for segment in shln_processed_cursor:
                        segment[5] = sector + "-" +  str(num_seq).zfill(4)
                        segment[6] = sector + "-" +  str(num_seq).zfill(4)
                        shln_processed_cursor.updateRow(segment)
                        break

                num_seq += 1

        arcpy.Delete_management(segments_remaining)
        sector_count += 1
        print("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") completed")

        
    # arcpy.DeleteField_management(outFeatureClass, ["join_count", "SRID", "TARGET_FID"])
    arcpy.CopyFeatures_management(shln_processed, output_test)



        
if __name__ == '__main__':

    #lic_arcinfo_status = arcpy.CheckProduct("arcinfo")
    #lic_spatial_analyst_status = arcpy.CheckExtension("spatial")

    #if lic_arcinfo_status == "AlreadyInitalized":  # check licenses (p.117)
    #    pass
    #elif  lic_arcinfo_status == "Available" or :
    #    pass
    #else:
        # Exit script gracefully
    
    # if lic_spatial_analyst_status = "Available":
    #    arcpy.CheckOutExtension("spatial")

    initiate_shoreline_segments_naming() # main function

    #arcpy.CheckInExtension("spatial")

