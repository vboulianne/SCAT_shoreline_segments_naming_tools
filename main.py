


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

# Declarations

# TODO: Find how to specify in the working directory of loaded datasets or input dataset
arcpy.env.workspace = arcpy.GetParameterAsText(2) # Set ArcGIS workspace 

# Functions
def unique(input_list):
    
    # insert the list to the set
    list_set = set(input_list)
    # convert the set to the list
    unique_list = (list(list_set))
    for x in unique_list:
        print x
    return unique_list



def initiate_shoreline_segments_naming():

    # Input feature classes - static

    #shoreline_to_process = r"C:\GIS\Shoreline\shln_bay_of_fundy.shp"
    #reference_grid = r"C:\GIS\Shoreline\Data\nts_snrc\nts_snrc_50k.shp"

    # Input from tool gui

    shoreline_to_process = arcpy.GetParameterAsText(0)
    reference_grid = arcpy.GetParameterAsText(1)
    islands_ordered = arcpy.GetParameterAsText(2)
    shoreline_order_field = arcpy.GetParameterAsText(3)
    island_order_field = arcpy.GetParameterAsText(4)
    output = arcpy.GetParameterAsText(5)



    # CHECKS
    # Check is line/polyline
    # Check if shoreline and grid feature classes is projected properly. If not exit.



    # arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


    # Attribute Grid to Segment


    shln_to_process_with_grid = arcpy.SpatialJoin_analysis(target_features=shoreline_to_process , join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")


# Search Unique Values of grid for shapefile and put in list

    values_list = []
    with arcpy.da.SearchCursor(shln_to_process_with_grid,("NTS_SNRC")) as cursor:
        for row in cursor:
            values_list.append(row[0])
    sector_list = list(set(values_list))


    # LOOP
    sector_count = 0
    for sector in  sector_list:

        # Select all segments within grid sector
    

        # List has to be created from which segments can be deleted after being named. Current segment would not be in that list. Then spatial join can be used
        # to select the closest next segment. 

        #SNIPPET: arcpy.Select_analysis(in_features="work_shln_bay_of_fundy_withGrid", out_feature_class="C:/GIS/Shoreline/work5.shp", where_clause='"NTS_SNRC" = '021A12'')
        
        #if shoreline_order_field:
        #    order_by = shoreline_order_field
        
        '''
        Current problem. 
        arcpy.Select_analysis create a separate output feature and is not a selection in the current 
        '''

        # TODO: Work up to here 


        sql_clause_ord = (None, "ORDER BY " + shoreline_order_field + " ASC")

        num_seq = 1
        with arcpy.da.UpdateCursor(shln_to_process_with_grid, ["NAME_EN"], where_clause="NTS_SNRC='" + sector + "'", sql_clause=sql_clause_ord) as cursor:
            for row in cursor:
                row[0] = sector + "-" +  str(num_seq).zfill(3)
                cursor.updateRow(row)
                num_seq += 1

        sector_count += 1

    arcpy.Copy_management(shln_to_process_with_grid, output)




        
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



# UNUSED CODE:
'''
            segmentsWithinGrid = arcpy.SelectLayerByLocation_management(shorelineToProcess, 'CONTAINED', selectionStateLayer)

        except:

        finally:
            arcpy.Delete_management("")
            arcpy.Delete_management("")

        for sector in grid:
            with arcpy.da.SearchCursor(shorelineToProcess, (NTS_SNRC), sector) as cursor:

                # Calculate nearest segment and name it
                for row in cursor:
                    # Calculate nearest segment
'''
