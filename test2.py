import arcpy

shoreline_to_process = r"C:\GIS\Shoreline\shln_bay_of_fundy.shp"
reference_grid = r"C:\GIS\Shoreline\code_sgmt_naming\nts_grid\nts_grid.shp"
#islands_ordered = arcpy.GetParameterAsText(2)
shoreline_order_field = "UNIQUEID"
#island_order_field = arcpy.GetParameterAsText(4)
output = r"C:\GIS\Shoreline\Output\output.shp"


# CHECKS/VALIDATION
# Check is line/polyline
# Check if shoreline and grid feature classes is projected properly. If not exit.


# arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


# Attribute Grid to Segment


shln_with_grid = arcpy.SpatialJoin_analysis(target_features=shoreline_to_process , join_features=reference_grid, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="HAVE_THEIR_CENTER_IN")


# Search Unique Values of grid for shapefile and put in list

values_list = []
with arcpy.da.SearchCursor(shln_with_grid,("NTS_SNRC")) as cursor:
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

    segments_in_sector = arcpy.Select_analysis(shln_with_grid, out_feature_class="C:\GIS\Shoreline\Output\segments_in_sector.php", where_clause="NTS_SNRC='" + sector + "'")
    
    # TODO: Work up to here 

    sql_clause_ord = (None, "ORDER BY " + shoreline_order_field + " ASC")

    num_seq = 1
    with arcpy.da.SearchCursor(segments_in_sector, field_names="*", sql_clause=sql_clause_ord) as cursor:
        print(sector + "-" +  str(num_seq))
        num_seq += 1

    sector_count += 1

