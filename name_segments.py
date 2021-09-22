


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

    testmode = 0

    if testmode == 0:

        ###### INPUT - TOOL GUI ######

        shoreline_file = arcpy.GetParameterAsText(0)
        reference_grid = arcpy.GetParameterAsText(1)
        #method = arcpy.GetParameterAsText(2)
        method = 2
        islands_ordered = arcpy.GetParameterAsText(3)
        shoreline_order_field = arcpy.GetParameterAsText(4)
        #island_order_field = arcpy.GetParameterAsText(5)
        process_output = arcpy.GetParameterAsText(5)
        # process_output = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_" + str(uuid4()).replace("-", "")


    elif testmode == 1:
        ###### INPUT - STATIC #######

        shoreline_file = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_bay_of_fundy"
        #shoreline_file = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_arctic_mb_nl_nt_nu_on_qc_yt"
        reference_grid = "C:/GIS/Shoreline/code_sgmt_naming/nts_grid/nts_grid.shp"
        shoreline_order_field = "OBJECTID"
        # shoreline_field_id = "TARGET_ID"
        process_output = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_" + str(uuid4()).replace("-", "")
        #arcpy.env.workspace = r"C:\GIS\Shoreline"
        method = 2
    


    ########### CHECKS #################
    
    # Check is line/polyline
    # Check if shoreline and grid feature classes is projected properly. If not exit.

    ########### CREATE FINAL WORKING FILES ##############


    # Attribute Grid to Segment
    shln_to_process = arcpy.SpatialJoin_analysis(target_features=shoreline_file, out_feature_class="in_memory\shln_grid_" + str(uuid4()).replace("-", ""), join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")
    
    # Make file for processed segment (Method 2)
    shln_processed = arcpy.CopyFeatures_management(in_features=shln_to_process, out_feature_class="in_memory\shln_proc_" + str(uuid4()).replace("-", ""))


    ########## GROUP SEGMENTS BY SECTOR ##############

    # Search Unique Values of grid for shapefile and put in list

    values_list = []
    with arcpy.da.SearchCursor(shln_to_process,("TARGET_FID", "NTS_SNRC")) as cursor:
        for row in cursor:
            values_list.append(row[1])
    sector_list = list(set(values_list))

    sector_count = 0

    '''
    Various methods to name sequentially. Choose one.
    Method 1: Use an ordered field. 
    Method 2: Use segment proximity
    
    '''

    if method == 1:

        for sector in sector_list: # Loop by sector

            # Select all segments within grid sector
        

            sql_clause_ord = (None, "ORDER BY " + shoreline_order_field + " ASC")

            # SQL query create a subgroup by sector and afterward named sequentially in ascending order of their "OBJECTID"
            num_seq = 1
            with arcpy.da.UpdateCursor(shln_to_process, ["NAME_EN"], where_clause="NTS_SNRC='" + sector + "'", sql_clause=sql_clause_ord) as cursor:
                for row in cursor:
                    row[0] = sector + "-" +  str(num_seq).zfill(4)
                    cursor.updateRow(row)
                    num_seq += 1
            
            sector_count += 1
            #print("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") completed")
            arcpy.AddMessage("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") completed")

        shln_processed = shln_to_process



    elif method == 2:

        for sector in sector_list: # Loop by sector

            segments_remaining = arcpy.Select_analysis(in_features=shln_to_process, out_feature_class="in_memory\seg_rem_" + str(uuid4()).replace("-", ""), where_clause="NTS_SNRC='" + sector + "'")
            
            segments_id_remaining = []
            segment_id = ""
            first_segment_id = ""
            with arcpy.da.SearchCursor(segments_remaining,("OBJECTID", "NTS_SNRC")) as cursor:
                for row in cursor:
                    segments_id_remaining.append(row[0])

            ##### PROCESS FIRST SEGMENT ####

            ''' 
            First segment of a sector has to be selected according to spatial relationship. 
            A simple solution is to select segment with lowest OBJECTID as in naming method 1.
            Another solution would be to select according to proximity to a particular border. 
            Lastly and probably the best solution, First segment can be selected manually by
            editing a "sector_first_segment" field added for this purpose. 
        
            '''

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
            # Create near table table with processed segment and all the other segments remaining. 

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
            ## SHOW PROGRESS ##
            #print("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") completed")
            arcpy.AddMessage("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") completed")



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

    #arcpy.CheckInExtension("spatial")

