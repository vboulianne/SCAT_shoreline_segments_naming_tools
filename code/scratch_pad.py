            ##arcpy.MakeFeatureLayer_management(shln_to_process_with_grid, "lyr") 
            #arcpy.SelectLayerByAttribute_management("lyr", "SUBSET_SELECTION", '"NTS_SNRC" = ' + ''+ sector + '')
            #arcpy.CopyFeatures_management("lyr", "segments_remaining")
            
            
            
                        #segments_remaining = arcpy.CreateFeatureclass_management(out_path=shoreline_processed_path, out_name=shoreline_processed_name, geometry_type="POLYLINE", template=shln_to_process_with_grid, has_m="DISABLED", has_z="DISABLED", spatial_reference="GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")
            
            
                    with arcpy.da.UpdateCursor(segments_remaining, ["OBJECTID", "NAME_EN"], where_clause="OBJECTID =" + row[0] + "") as cursor2:
                        for row2 in cursor2:
                            cursor2.deleteRow()
                    break
                    
                    
                    
                    ====================
                    
                    
            while segments_id_remaining.count() > 0:

                segment_processed = arcpy.da.SearchCursor(shln_to_process_with_grid,("OBJECTID", "NAME_EN"), where_clause="OBJECTID='" + segment_id_processed + "'")
                
                near_table = arcpy.GenerateNearTable_analysis(segment_processed, segments_remaining, closest="CLOSEST", method="GEODESIC", out_table="C:\GIS\Shoreline\Scratch\NearTable.shp")

                with arcpy.da.SearchCursor(near_table, "*") as cursor:
                    for row in cursor:
                        nearest_segment = row[2]
                        break
                
                
                with arcpy.da.UpdateCursor(shln_to_process_with_grid, ["OBJECTID", "NAME_EN"], where_clause="OBJECTID='" + nearest_segment + "'") as cursor:
                    for row in cursor:
                        row[1] = sector + "-" +  str(num_seq).zfill(4)
                        cursor.updateRow(row)
                        segment_id_processed = row[0]
                        segments_id_remaining.remove(row[0])
                        num_seq += 1
                
            break
                

            
            arcpy.Copy_management(shln_to_process_with_grid , segments_remaining)
            arcpy.TruncateTable_management(table)






=========================


rec=0 
def autoIncrement(): 
     global rec 
     pStart = 1 
     pInterval = 1 
     if (rec == 0): 
     rec = pStart 
     else: 
     rec += pInterval 
     return rec
     

