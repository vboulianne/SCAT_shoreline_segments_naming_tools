import arcpy

shoreline_to_process = r"C:\GIS\Shoreline\shln_bay_of_fundy.shp"
reference_grid = r"C:\GIS\Shoreline\code_sgmt_naming\nts_grid\nts_grid.shp"
#islands_ordered = arcpy.GetParameterAsText(2)
shoreline_order_field = "OBJECTID"
#island_order_field = arcpy.GetParameterAsText(4)
output = r"C:\GIS\Shoreline\Output\output10.shp"


# CHECKS/VALIDATION
# Check is line/polyline
# Check if shoreline and grid feature classes is projected properly. If not exit.


# arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


# Attribute Grid to Segment


shln_to_process_with_grid = arcpy.SpatialJoin_analysis(target_features=shoreline_to_process, join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")


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


    # WRONG segments_in_sector = arcpy.Select_analysis(shln_with_grid, where_clause="NTS_SNRC='" + sector + "'")
    '''
    Current problem. 
    arcpy.Select_analysis create a separate output feature and is not a selection in the current 
    '''

    # TODO: Work up to here 


    sql_clause_ord = (None, "ORDER BY " + shoreline_order_field + " ASC")

    num_seq = 1
    with arcpy.da.UpdateCursor(shln_to_process_with_grid, ["NAME_EN"], where_clause="NTS_SNRC='" + sector + "'", sql_clause=sql_clause_ord) as cursor:
        for row in cursor:
            row[0] = sector + "-" +  str(num_seq)
            cursor.updateRow(row)
            num_seq += 1

    sector_count += 1

arcpy.Copy_management(shln_to_process_with_grid, output)
