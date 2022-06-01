# Reorder fields

import arcpy


def reorder_fields():

    testmode = 0

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

    if testmode == 0:

        table = arcpy.GetParameterAsText(0)
        field_order = arcpy.GetParameterAsText(1)
        out_table = arcpy.GetParameterAsText(2)
        omit_other_fields = arcpy.GetParameterAsText(3)
        field_order = field_order.split(", ")

        arcpy.AddMessage(omit_other_fields)

        if omit_other_fields == 'true':
            add_missing = False
        else:
            add_missing = True


    ###### INPUT - TESTMODE - STATIC #######

    elif testmode == 1:
        
        table = "C:/GIS/Shoreline/shln_naming_work.gdb/Work/bof_newname_test7"
        field_order = ["NAME"]
        out_table ="C:/GIS/Shoreline/shln_naming_work.gdb/Work/bof_newname_test7_res"
        add_missing = True

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

if __name__ == '__main__':

    lic_arcinfo_status = arcpy.CheckProduct("arcinfo")
    reorder_fields()
