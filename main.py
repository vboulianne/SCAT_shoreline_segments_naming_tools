


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
arcpy.env.workspace = "C:/Data" # Set ArcGIS workspace 

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

    shoreline_to_process = r"C:\GIS\Shoreline\shln_bay_of_fundy.shp"
    reference_grid = r"C:\GIS\Shoreline\Data\nts_snrc\nts_snrc_50k.shp"

    # Input from tool gui

    # shorelineToProcess = arcpy.GetParameterAsText(0)
    # referecnceGrid = arcpy.GetParameterAsText(1)


    # CHECKS
    # Check is line/polyline
    # Check if shoreline and grid feature classes is projected properly. If not exit.



    # arcpy.Project_management(in_dataset="nts_snrc_50k", out_dataset="C:/GIS/Shoreline/Data/nts_snrc_projected", out_coor_system="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="'NAD_1983_CSRS_To_WGS_1984_2 + NAD_1983_To_WGS_1984_1'", in_coor_system="GEOGCS['GCS_North_American_1983_CSRS',DATUM['D_North_American_1983_CSRS',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")


    # Attribute Grid to Segment


    arcpy.SpatialJoin_analysis(target_features= shoreline_to_process , join_features= reference_grid, "shore_line_with_grid", join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping='OBJECTID "OBJECTID" true true false 10 Long 0 10 ,First,#,shln_bay_of_fundy,OBJECTID,-1,-1;UNIQUEID "UNIQUEID" true true false 50 Text 0 0 ,First,#,shln_bay_of_fundy,UNIQUEID,-1,-1;NAME_EN "NAME_EN" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,NAME_EN,-1,-1;NAME_FR "NAME_FR" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,NAME_FR,-1,-1;NAME_OTHER "NAME_OTHER" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,NAME_OTHER,-1,-1;LABEL_EN "LABEL_EN" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,LABEL_EN,-1,-1;LABEL_FR "LABEL_FR" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,LABEL_FR,-1,-1;URL "URL" true true false 250 Text 0 0 ,First,#,shln_bay_of_fundy,URL,-1,-1;URL_FR "URL_FR" true true false 250 Text 0 0 ,First,#,shln_bay_of_fundy,URL_FR,-1,-1;LEGISLATIO "LEGISLATIO" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,LEGISLATIO,-1,-1;LEGISLAT_1 "LEGISLAT_1" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,LEGISLAT_1,-1,-1;JURISDICTI "JURISDICTI" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,JURISDICTI,-1,-1;JURIDICTIO "JURIDICTIO" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,JURIDICTIO,-1,-1;GROUP_EN "GROUP_EN" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,GROUP_EN,-1,-1;GROUP_FR "GROUP_FR" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,GROUP_FR,-1,-1;SUBGROUP_E "SUBGROUP_E" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,SUBGROUP_E,-1,-1;SUBGROUP_F "SUBGROUP_F" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,SUBGROUP_F,-1,-1;STATUS_EN "STATUS_EN" true true false 200 Text 0 0 ,First,#,shln_bay_of_fundy,STATUS_EN,-1,-1;STATUS_FR "STATUS_FR" true true false 200 Text 0 0 ,First,#,shln_bay_of_fundy,STATUS_FR,-1,-1;DESCRIPTIO "DESCRIPTIO" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,DESCRIPTIO,-1,-1;DESCRIPT_1 "DESCRIPT_1" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,DESCRIPT_1,-1,-1;VALIDATION "VALIDATION" true true false 8 Date 0 0 ,First,#,shln_bay_of_fundy,VALIDATION,-1,-1;PROVINCEEX "PROVINCEEX" true true false 50 Text 0 0 ,First,#,shln_bay_of_fundy,PROVINCEEX,-1,-1;ABUNDANCE "ABUNDANCE" true true false 13 Float 0 0 ,First,#,shln_bay_of_fundy,ABUNDANCE,-1,-1;DATASOURCE "DATASOURCE" true true false 200 Text 0 0 ,First,#,shln_bay_of_fundy,DATASOURCE,-1,-1;uiscatclas "uiscatclas" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uiscatclas,-1,-1;siscatclas "siscatclas" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,siscatclas,-1,-1;width "width" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,width,-1,-1;createdby "createdby" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,createdby,-1,-1;creationda "creationda" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,creationda,-1,-1;confidence "confidence" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,confidence,-1,-1;generalcom "generalcom" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,generalcom,-1,-1;uiform "uiform" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uiform,-1,-1;uislope "uislope" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uislope,-1,-1;uiheight "uiheight" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uiheight,-1,-1;uisubstrat "uisubstrat" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uisubstrat,-1,-1;uisubstr_1 "uisubstr_1" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uisubstr_1,-1,-1;uisubstr_2 "uisubstr_2" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,uisubstr_2,-1,-1;siform "siform" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,siform,-1,-1;sislope "sislope" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,sislope,-1,-1;siheight "siheight" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,siheight,-1,-1;sisubstrat "sisubstrat" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,sisubstrat,-1,-1;sisubstr_1 "sisubstr_1" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,sisubstr_1,-1,-1;sisubstr_2 "sisubstr_2" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,sisubstr_2,-1,-1;bsform "bsform" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bsform,-1,-1;bsslope "bsslope" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bsslope,-1,-1;bsheight "bsheight" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bsheight,-1,-1;bssubstrat "bssubstrat" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bssubstrat,-1,-1;bssubstr_1 "bssubstr_1" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bssubstr_1,-1,-1;bssubstr_2 "bssubstr_2" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bssubstr_2,-1,-1;uisubstr_3 "uisubstr_3" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,uisubstr_3,-1,-1;sisubstr_3 "sisubstr_3" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,sisubstr_3,-1,-1;bssubstr_3 "bssubstr_3" true true false 254 Text 0 0 ,First,#,shln_bay_of_fundy,bssubstr_3,-1,-1;siespacecl "siespacecl" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,siespacecl,-1,-1;bsespacecl "bsespacecl" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bsespacecl,-1,-1;bsespace_1 "bsespace_1" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,bsespace_1,-1,-1;directalon "directalon" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,directalon,-1,-1;directback "directback" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,directback,-1,-1;fetch_ "fetch_" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,fetch_,-1,-1;miclass "miclass" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,miclass,-1,-1;liclass "liclass" true true false 100 Text 0 0 ,First,#,shln_bay_of_fundy,liclass,-1,-1;lowconfrea "lowconfrea" true true false 150 Text 0 0 ,First,#,shln_bay_of_fundy,lowconfrea,-1,-1;access "access" true true false 150 Text 0 0 ,First,#,shln_bay_of_fundy,access,-1,-1;exposure "exposure" true true false 150 Text 0 0 ,First,#,shln_bay_of_fundy,exposure,-1,-1;Shape_Leng "Shape_Leng" true true false 19 Double 0 0 ,First,#,shln_bay_of_fundy,Shape_Leng,-1,-1;NTS_SNRC "NTS_SNRC" true true false 50 Text 0 0 ,First,#,nts_snrc_projected,NTS_SNRC,-1,-1;NAME_ENG "NAME_ENG" true true false 120 Text 0 0 ,First,#,nts_snrc_projected,NAME_ENG,-1,-1;NOM_FRA "NOM_FRA" true true false 120 Text 0 0 ,First,#,nts_snrc_projected,NOM_FRA,-1,-1;SRID "SRID" true true false 10 Long 0 10 ,First,#,nts_snrc_projected,SRID,-1,-1;SHAPE_AREA "SHAPE_AREA" true true false 19 Double 0 0 ,First,#,nts_snrc_projected,SHAPE_AREA,-1,-1;SHAPE_LEN "SHAPE_LEN" true true false 19 Double 0 0 ,First,#,nts_snrc_projected,SHAPE_LEN,-1,-1', match_option="HAVE_THEIR_CENTER_IN", search_radius="", distance_field_name="")


    # Search Unique Values of grid for shapefile and put in list

    values_list = []
    with arcpy.da.SearchCursor(featureClass,("NTS_SNRC")) as cursor:
        for row in cursor:
            values_list.append(row[0])
    list_Set = set(values_list)
    sector_list = list(list_set)


    # LOOP
    sectorCount = 0
    for sector in sectorList

        # Select all segments within grid sector
    

        # List has to be created from which segments can be deleted after being named. Current segment would not be in that list. Then spatial join can be used
        # to select the closest next segment. 

        #SNIPPET: arcpy.Select_analysis(in_features="work_shln_bay_of_fundy_withGrid", out_feature_class="C:/GIS/Shoreline/work5.shp", where_clause='"NTS_SNRC" = '021A12'')
        with arcpy.Select_analysis("shoreLine_with_grid", "segments_within_grid_sector", where_clause='"NTS_SNRC" = '' + sector + '') as cursor:
            
            try: 

            # Select segment at to the bottom left of the grid

            # LOOP

            # For the currently selected segment, find the distance of all other segments
            # Select closest segment to the current segment.
            # Name closest segment 
            #END LOOP

                

            except:

            finally:
        sectorCount += 1



        
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
