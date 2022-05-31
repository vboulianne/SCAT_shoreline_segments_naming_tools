


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
import sys
from uuid import uuid4
arcpy.env.overwriteOutput = True
#arcpy.env.scratchWorkspace = "c:/GIS/Shoreline/Scratch"

# Declarations


###### FUNCTIONS ######

def reorder_fields(table, out_table, field_order, add_missing=True):
    """
    http://joshwerts.com/blog/2014/04/17/arcpy-reorder-fields/

    Reorders fields in input featureclass/table
    :table:         input table (fc, table, layer, etc)
    :out_table:     output table (fc, table, layer, etc)
    :field_order:   order of fields (objectid, shape not necessary)
    :add_missing:   add missing fields to end if True (leave out if False)
    -> path to output table
    new_field_order = ["field2", "field3", "field1"]
    reorder_fields(in_fc, out_fc, new_field_order)

    """
    existing_fields = arcpy.ListFields(table)
    existing_field_names = [field.name for field in existing_fields]

    existing_mapping = arcpy.FieldMappings()
    existing_mapping.addTable(table)

    new_mapping = arcpy.FieldMappings()

    def add_mapping(field_name):
        mapping_index = existing_mapping.findFieldMapIndex(field_name)

        # required fields (OBJECTID, etc) will not be in existing mappings
        # they are added automatically
        if mapping_index != -1:
            field_map = existing_mapping.fieldMappings[mapping_index]
            new_mapping.addFieldMap(field_map)

    # add user fields from field_order
    for field_name in field_order:
        if field_name not in existing_field_names:
            raise Exception("Field: {0} not in {1}".format(field_name, table))

        add_mapping(field_name)

    # add missing fields at end
    if add_missing:
        missing_fields = [f for f in existing_field_names if f not in field_order]
        for field_name in missing_fields:
            add_mapping(field_name)

    # use merge with single input just to use new field_mappings
    arcpy.Merge_management(table, out_table, new_mapping)
    return out_table





def initiate_shoreline_segments_naming():

    testmode = 0

    ###### INPUT - TOOL GUI ######

    if testmode == 0:

        shoreline_file = arcpy.GetParameterAsText(0)
        reference_grid = arcpy.GetParameterAsText(1)
        single_segment_to_process = arcpy.GetParameterAsText(2)
        method = arcpy.GetParameterAsText(3)
        shoreline_order_field = arcpy.GetParameterAsText(4)
        process_output = arcpy.GetParameterAsText(5)
        # process_output = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_" + str(uuid4()).replace("-", "")

    ###### INPUT - TESTMODE - STATIC #######

    elif testmode == 1:
        

        #shoreline_file = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_bay_of_fundy"
        shoreline_file = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_bay_of_fundy_method2"
        #shoreline_file = "C:/GIS/Shoreline/Shoreline_Database.gdb/shoreline_classification_arctic_mb_nl_nt_nu_on_qc_yt"
        #shoreline_file = "C:/GIS/Shoreline/shln_naming_work.gdb/test_894200ae745045df96a344b64c81e393"
        reference_grid = "C:/GIS/Shoreline/SCAT_shoreline_segments_naming_tools/grid/nts_grid.shp"
        #single_segment_to_process = "021A12"
        single_segment_to_process = ""
        shoreline_order_field = "OBJECTID"
        process_output = "C:/GIS/Shoreline/shln_naming_work.gdb/scratch/test_" + str(uuid4()).replace("-", "")
        #arcpy.env.workspace = r"C:\GIS\Shoreline"
        method = "By Proximity"
        output_symbology = ""
    


    ########### CHECKS #################
    
    # Check is line/polyline
    # Check if shoreline and grid feature classes is projected properly. If not exit.

    ########### CREATE FINAL WORKING FILES ##############


    # Attribute Grid to Segment

    shln_to_process = arcpy.SpatialJoin_analysis(target_features=shoreline_file, out_feature_class="in_memory\shln_grid_" + str(uuid4()).replace("-", ""), join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")
    
    if single_segment_to_process != "":
        arcpy.DeleteField_management(shln_to_process, ['NAME_ENG', 'NOM_FRA', 'NTS_SNRC', 'SRID', 'Shape_area'])
    
    lstFields = arcpy.ListFields(shln_to_process)
    fld_seq_exists = 0
    fld_name_exists = 0
    for field in lstFields:
                if field.name == "SEQUENTIAL_NO":
                    fld_seq_exists = 1
                elif field.name == "NAME":
                    fld_name_exists = 1
    if fld_seq_exists == 0:
        arcpy.AddField_management(in_table=shln_to_process, field_name="SEQUENTIAL_NO", field_type="LONG")
    if fld_name_exists == 0:
        arcpy.AddField_management(in_table=shln_to_process, field_name="NAME", field_type="TEXT")
    

    # Make file for processed segment (Method 2)
    shln_processed = arcpy.CopyFeatures_management(in_features=shln_to_process, out_feature_class="in_memory\shln_proc_" + str(uuid4()).replace("-", ""))
    #reference_grid_file  = arcpy.CopyFeatures_management(in_features=reference_grid, out_feature_class="in_memory\ref_grid_" + str(uuid4()).replace("-", ""))
    # List field objects



    # Comment: Transpose fields?


    ########## GROUP SEGMENTS BY SECTOR ##############

    # Search Unique Values of grid for shapefile and put in list


    if single_segment_to_process == "":
        values_list = []
        with arcpy.da.SearchCursor(shln_to_process,("TARGET_FID", "NTS_SNRC")) as cursor:
            for row in cursor:
                values_list.append(row[1])
        sector_list = list(set(values_list))

    else:
        sector_list = []
        sector_list.append(single_segment_to_process)
        arcpy.AddMessage(sector_list)
        


    '''
    Various methods to name sequentially. Choose one.
    Method 1: Use an ordered field. 
    Method 2: Use segment proximity
    
    '''

    if method == "By Ordering Field":

        sector_count = 1

        # Shoreline to process *HAS* to be in filesystem to be sortable in the Cursor with SQL postfix. It is a limitation of 'In memory' storage.
        shln_to_process = arcpy.CopyFeatures_management(in_features= shln_to_process, out_feature_class="shln_proc_" + str(uuid4()).replace("-", ""))
        
        for sector in sector_list: # Loop by sector
            arcpy.AddMessage("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") being processed")
            
            #Sort by field
            sql_orderby = "ORDER BY " + shoreline_order_field

            # SQL query create a subgroup by sector and afterward named sequentially in ascending order of their "OBJECTID"
            num_seq = 1
            with arcpy.da.UpdateCursor(shln_to_process, ["NAME", "SEQUENTIAL_NO"], where_clause="NTS_SNRC='" + sector + "'", sql_clause=(None, sql_orderby)) as cursor:
                for row in cursor:
                    row[0] = sector + "-" +  str(num_seq).zfill(4)
                    row[1] = num_seq * 100
                    cursor.updateRow(row)
                    num_seq += 1
            
            sector_count += 1
            #print("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") completed")
            

        shln_processed = shln_to_process



    elif method == "By Proximity":

        sector_count = 1
        for sector in sector_list: # Loop by sector
            arcpy.AddMessage("Sector " + str(sector_count) + "/" + str(len(sector_list)) + " (" + sector + ") being processed")

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
            
            
            x = False
            for field in lstFields:
                if field.name == "sector_first_segment":
                    fs_count = 0
                    with arcpy.da.SearchCursor(segments_remaining, ['sector_first_segment']) as first_segments_cursor:
                        for first_seg in first_segments_cursor:
                            if first_seg[0] == 1:
                                x = True
                                fs_count += 1
                    if fs_count > 1: 
                        arcpy.AddMessage("Sector " + str(sector_count) + " has more than one 'first segment': review")
                        sys.exit()

            if x == True:
                sql_clause_ord = (None, 'ORDER BY sector_first DESC')
                with arcpy.da.UpdateCursor(segments_remaining, ['OBJECTID', 'TARGET_FID'], where_clause="sector_first_segment=1") as segments_remaining_cursor:
                
                    for segment in segments_remaining_cursor:
                        first_segment_id = segment[0]
                        segment_target_fid = segment[1]
                        segment_processed = arcpy.Select_analysis(in_features=segments_remaining, out_feature_class="in_memory\seg_proc" + str(uuid4()).replace("-", ""), where_clause="OBJECTID="+str(first_segment_id)+"")
                        segments_remaining_cursor.deleteRow()
                        
                        num_seq += 1
                        break
            else:
                sql_clause_ord = (None, 'ORDER BY TARGET_FID ASC')
                with arcpy.da.UpdateCursor(segments_remaining, ['OBJECTID', 'TARGET_FID'], sql_clause=sql_clause_ord) as segments_remaining_cursor:
                
                    for segment in segments_remaining_cursor:

                        first_segment_id = segment[0]
                        segment_target_fid = segment[1]
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
            
            with arcpy.da.UpdateCursor(shln_processed, ['NAME', 'SEQUENTIAL_NO'], where_clause="TARGET_FID="+str(segment_target_fid)+"") as shln_processed_cursor:
                for segment in shln_processed_cursor:
                    segment[0] = sector + "-0001"
                    segment[1] = 100
                    shln_processed_cursor.updateRow(segment)
            
                arcpy.Delete_management(near_table)
                arcpy.Delete_management(segment_processed)

            #arcpy.CopyFeatures_management(shln_processed , output_test)

            ###### PROCESS THE REMAINING SEGMENTS ####
            while len(segments_id_remaining) > 0:

                with arcpy.da.UpdateCursor(segments_remaining, ['OBJECTID', 'TARGET_FID'], where_clause="OBJECTID="+str(segment_id)+"") as segments_remaining_cursor:
                    
                    for segment in segments_remaining_cursor: 
                        segment_id = segment[0]
                        segment_target_fid = segment[1]
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

                with arcpy.da.UpdateCursor(shln_processed, ['NAME', 'SEQUENTIAL_NO'], where_clause="TARGET_FID="+str(segment_target_fid)+"") as shln_processed_cursor:
                    for segment in shln_processed_cursor:
                        segment[0] = sector + "-" +  str(num_seq).zfill(4)
                        segment[1] = num_seq*100
                        shln_processed_cursor.updateRow(segment)
                        break

                num_seq += 1

            arcpy.Delete_management(segments_remaining)
            sector_count += 1

   
    # Create alias
    arcpy.AlterField_management(shln_processed, "NAME", "NAME_SEG", "Alias_seg") # There seems to be an issue to have an alias that is the same but in proper case
    arcpy.AlterField_management(shln_processed, "NAME_SEG", "NAME", "Name")
    arcpy.AlterField_management(in_table=shln_processed, field="SEQUENTIAL_NO", new_field_alias="Sequential number (per sector)")

    # Delete fields
    arcpy.DeleteField_management(shln_processed, ['TARGET_FID', 'Join_count', 'NAME_ENG', 'NOM_FRA', 'NTS_SNRC', 'SRID', 'Shape_area'])
    
    # Reorder fields - Not working
    #new_field_order = ["UNIQUEID", "NAME"]
    #shln_reordered = reorder_fields(shln_processed, "in_memory\shln_grid_" + str(uuid4()).replace("-", ""), new_field_order)


    ###### OUTPUT ######

    arcpy.CopyFeatures_management(shln_processed, process_output)


    ###### END MESSAGE ######
    arcpy.AddMessage("Processed shoreline written to " + process_output)


        
if __name__ == '__main__':

    lic_arcinfo_status = arcpy.CheckProduct("arcinfo")
    lic_spatial_analyst_status = arcpy.CheckExtension("spatial")

    initiate_shoreline_segments_naming() # main function

    arcpy.CheckInExtension("spatial")


    #if lic_arcinfo_status == "AlreadyInitalized":  # check licenses (p.117)
    #    pass
    #elif  lic_arcinfo_status == "Available" or :
    #    pass
    #else:
        # Exit script gracefully
    
    # if lic_spatial_analyst_status = "Available":
    #    arcpy.CheckOutExtension("spatial")


