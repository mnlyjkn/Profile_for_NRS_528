# Final, see instructions

import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Land_Cover_Class_Selection,Species_Heatmap, Clip_and_Merge]
        # self.tools = [Species_Heatmap]

class Land_Cover_Class_Selection(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Land Cover Class Selection"
        self.description = "Selects a county from a shapefile of multiple counties and uses that as the clipping region for when selecting a land cover class"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_shape = arcpy.Parameter(name="input_shape",
                                     displayName="Input Counties Shapefile (Ex: Towns_Washington.shp)",
                                     datatype="DEShapefile",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_shape.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Towns_Washington.shp"  # Default
        params.append(input_shape)  # This is parameters[0].  This is the shapefile that the town will be selected from.

        input_string = arcpy.Parameter(name="input_string",
                                    displayName="Input Township Name In Uppercase (Ex: SOUTH KINGSTOWN)",
                                    datatype="GPString",
                                    parameterType="Required",
                                    direction="Input",
                                    )
        # input_string.value = "SOUTH KINGSTOWN"  # Default
        params.append(input_string)  # This is parameters[1].  This is the name of the town used in the select tool.

        output = arcpy.Parameter(name="output_shape",
                                    displayName="Selected Town Output (Ex: Township.shp)",
                                    datatype="DEShapefile",
                                    parameterType="Required",
                                    direction="Output",  # Input|Output
                                    )
        # output.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\Township.shp"  # Default
        params.append(output)  # This is parameters[2].  This is output for the first select tool.  Also used for as the clip feature.



        input_land_class = arcpy.Parameter(name="input_land_class",
                                      displayName="Input Land Class Shapefile (Ex: Land_Cover_2011_RI_State_Plane.shp)",
                                      datatype="DEShapefile",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Input",  # Input|Output
                                      )
        # input_land_class.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Land_Cover_2011_RI_State_Plane.shp"  # Default
        params.append(input_land_class)  # This is parameters[3].  This is the land cover class shapefile input for the clip tool.

        output_clip = arcpy.Parameter(name="output_clip",
                                 displayName="Clipped Land Cover Class Output (Ex: Town_land_cover.shp)",
                                 datatype="DEShapefile",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # output_clip.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\Town_land_cover.shp"  # Default
        params.append(output_clip)  # This is parameters[4].  This is output for the clip tool.  Will be used in the select tool.



        input_string_2 = arcpy.Parameter(name="input_string_2",
                                       displayName="Input A Land Cover Type (Ex: Water)",
                                       datatype="GPString",
                                       parameterType="Required",  # Required|Optional|Derived
                                       direction="Input",  # Input|Output
                                       )
        # input_string_2.value = "Water"  # Default
        params.append(input_string_2)  # This is parameters[5].  This is the name of the land class type used in the select tool.

        input_string_3 = arcpy.Parameter(name="input_string_3",
                                         displayName="Input An Additional Land Cover Type (Ex: Wetland)",
                                         datatype="GPString",
                                         parameterType="Required",  # Required|Optional|Derived
                                         direction="Input",  # Input|Output
                                         )
        # input_string_3.value = "Wetland"  # Default
        params.append(input_string_3)  # This is parameters[6].  This is the name of an additional land class type used in the select tool.

        output_final_select = arcpy.Parameter(name="output_final_select",
                                 displayName="Output Final Shapefile (Ex: Town_water.shp)",
                                 datatype="DEShapefile",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # output_final_select.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\Town_water.shp"  # Default
        params.append(output_final_select)  # This is parameters[7]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        input_shape = parameters[0].valueAsText
        input_string = parameters[1].valueAsText
        output_shape = parameters[2].valueAsText

        expression = "NAME = " + "'" + input_string + "'"
        arcpy.AddMessage(expression)

        arcpy.Select_analysis(in_features=input_shape,
                              out_feature_class=output_shape,
                              where_clause=expression
                              )
        arcpy.AddMessage("Done selecting township.")

        #  Next is to use the selected town as the clip feature

        input_shape_2 = parameters[3].valueAsText
        output_2 = parameters[4].valueAsText

        arcpy.Clip_analysis(in_features=input_shape_2,   # gets the land types within the township
                            clip_features=output_shape,
                            out_feature_class=output_2,
                            cluster_tolerance=""
                            )
        arcpy.AddMessage("Done clipping town land cover classes.")

        input_string_2 = parameters[5].valueAsText
        input_string_3 = parameters[6].valueAsText
        output_shape = parameters[7].valueAsText

        expression = "Descr_2011 = " + "'" + input_string_2 + "'" + " Or " + "Descr_2011 = " + "'" + input_string_3 + "'"
        arcpy.AddMessage(expression)

        arcpy.Select_analysis(in_features=output_2,
                              out_feature_class=output_shape,
                              where_clause=expression
                              )
        arcpy.AddMessage("Done selecting land cover.")

        return

class Species_Heatmap(object):   #
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Species Heatmap"
        self.description = "Creates a heatmap from a csv file of a single species"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_workspace = arcpy.Parameter(name="input_workspace",
                                   displayName="Input Workspace (Select a folder)",
                                   datatype="DEFolder",
                                   parameterType="Required",  # Required|Optional|Derived
                                   direction="Input",  # Input|Output
                                   )
        # input_workspace.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Test"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_workspace)  # This is parameters[0]

        input_csv = arcpy.Parameter(name="input_csv_file",
                                     displayName="Input Single Species CSV File (Ex: Cepphus_grylle.csv)",
                                     datatype="DEFile",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_csv.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Test\Cepphus_grylle.csv"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_csv)  # This is parameters[1]

        input_string = arcpy.Parameter(name="input_string",
                                    displayName="Input Single Species Name (No Spaces; Ex: Cepphus_grylle)",
                                    datatype="GPString",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Input",  # Input|Output
                                    )
        # input_string.value = "Cepphus_grylle"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_string)  # This is parameters[2]

        output_file = arcpy.Parameter(name="output_file",
                                    displayName="Species Heatmap Output (Ex: HeatMap_Cepphus_grylle.shp)",
                                    datatype="DEShapefile",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Output",  # Input|Output
                                    )
        # output_file.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Test\HeatMap_Cepphus_grylle.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_file)  # This is parameters[3]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True


    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        workspace = parameters[0].valueAsText
        input_file = parameters[1].valueAsText
        input_string = parameters[2].valueAsText
        output_file = parameters[3].valueAsText

        arcpy.env.workspace = workspace

        output_temp = input_string + '_output.shp'
        arcpy.AddMessage(output_temp)

        # csv to a shapefile
        in_Table = input_file
        x_coords = "lon"
        y_coords = "lat"
        z_coords = ""
        out_Layer = input_string
        saved_Layer = output_temp  # r"Cepphus_grylle_output.shp"
        spRef = arcpy.SpatialReference(4326)
        arcpy.AddMessage("Spatial reference created")
        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

        arcpy.AddMessage(saved_Layer)

        arcpy.CopyFeatures_management(lyr, saved_Layer)
        if arcpy.Exists(saved_Layer):
            arcpy.AddMessage("Created file successfully!")

        # Extact the Extent
        desc = arcpy.Describe(saved_Layer)
        arcpy.AddMessage(desc.extent)
        y_min = desc.extent.YMin
        y_max = desc.extent.YMax
        x_min = desc.extent.XMin
        x_max = desc.extent.XMax

        # Generate a fishnet
        arcpy.env.outputCoordinateSystem = spRef
        outFeatureClass = "Fishnet.shp"
        originCoordinate = (str(x_min) + " " + str(y_min))
        yAxisCoordinate = (str(x_min) + " " + str(y_max))
        cellSizeWidth = "0.25"
        cellSizeHeight = "0.25"
        numRows = ""
        numColumns = ""
        oppositeCorner = (str(x_max) + " " + str(y_max))
        labels = "NO_LABELS"
        templateExtent = "#"
        geometryType = "POLYGON"

        arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                       cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                       oppositeCorner, labels, templateExtent, geometryType)
        arcpy.AddMessage("Fishnet created")

        # Spatial Join the fishnet to the observed points
        target_features = outFeatureClass
        join_features = saved_Layer
        out_feature_class = output_file
        join_operation = "JOIN_ONE_TO_ONE"
        join_type = "KEEP_ALL"
        field_mapping = ""
        match_option = "INTERSECT"
        search_radius = ""
        distance_field_name = ""

        arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                                   join_operation, join_type, field_mapping, match_option,
                                   search_radius, distance_field_name)

        # Check if heatmap is created, then delete the intermediate files

        if arcpy.Exists(out_feature_class):
            arcpy.AddMessage("Created Heatmap, will now delete intermediate files")
            arcpy.Delete_management(target_features)
            arcpy.Delete_management(join_features)
            arcpy.AddMessage("Deleted intermediate files")

        arcpy.AddMessage("View results in ArcMap. Be sure to change symbology to properly represent the heat map.")

        return

class Clip_and_Merge(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Clip and Merge"
        self.description = "Clips a shapefile in two different areas and then merges them into a single shapefile"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_shape_1 = arcpy.Parameter(name="input_shape_1",
                                        displayName="Input First Shapefile (Ex: South_Rhode_Island_Buildings.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Input",  # Input|Output
                                        )
        # input_shape_1.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\South_Rhode_Island_Buildings.shp"  # Default
        params.append(input_shape_1)  # parem[0]

        input_clip = arcpy.Parameter(name="input_clip",
                                     displayName="Input Shapefile to use for First Clipping (Ex: URI_Campus.shp)",
                                     datatype="DEShapefile",
                                     parameterType="Required",
                                     direction="Input",  # Input|Output
                                     )
        # input_clip.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\URI_Campus.shp"  # Default
        params.append(input_clip)  # parem[1]

        clip_1_output = arcpy.Parameter(name="clip_1_output",
                                        displayName="First Clipping Output (Ex: clip_1.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Output",  # Input|Output
                                        )
        # clip_1_output.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\clip_1.shp"  # Default
        params.append(clip_1_output)  # parem[2]

        input_shape_2 = arcpy.Parameter(name="input_shape_2",   # CAN REMOVE THIS ONE
                                        displayName="Input Second Shapefile (Ex: South_Rhode_Island_Buildings.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Input",  # Input|Output
                                        )
        # input_shape_2.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\South_Rhode_Island_Buildings.shp"  # Default
        params.append(input_shape_2)  # parem[3]

        input_clip = arcpy.Parameter(name="input_clip",
                                     displayName="Input Shapefile to use for Second Clipping (Ex: Bay_Campus.shp)",
                                     datatype="DEShapefile",
                                     parameterType="Required",
                                     direction="Input",  # Input|Output
                                     )
        # input_clip.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Bay_Campus.shp"  # Default
        params.append(input_clip)  # parem[4]

        clip_2_output = arcpy.Parameter(name="clip_2_output",
                                        displayName="Second Clipping Output (Ex: clip_2.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Output",  # Input|Output
                                        )
        # clip_2_output.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\clip_2.shp"  # Default
        params.append(clip_2_output)  # parem[5]

        merge_output = arcpy.Parameter(name="merge_output",
                                       displayName="Merge Output (Ex: merge.shp)",
                                       datatype="DEShapefile",
                                       parameterType="Required",
                                       direction="Output",  # Input|Output
                                       )
        # merge_output.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\merge.shp"  # Default
        params.append(merge_output)  # parem[6]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_shape = parameters[0].valueAsText
        input_polygon = parameters[1].valueAsText
        output = parameters[2].valueAsText

        input_shape_2 = parameters[3].valueAsText
        input_polygon_2 = parameters[4].valueAsText
        output_2 = parameters[5].valueAsText

        input_shapes = [parameters[2].valueAsText, parameters[5].valueAsText]
        output_merge = parameters[6].valueAsText

        arcpy.Clip_analysis(in_features=input_shape,
                            clip_features=input_polygon,
                            out_feature_class=output,
                            cluster_tolerance="")
        arcpy.AddMessage("First clipping has been completed.")

        arcpy.Clip_analysis(in_features=input_shape_2,
                            clip_features=input_polygon_2,
                            out_feature_class=output_2,
                            cluster_tolerance="")
        arcpy.AddMessage("Second clipping has been completed.")

        arcpy.Merge_management(inputs=input_shapes,
                               output=output_merge,
                               field_mappings="",
                               add_source="")
        arcpy.AddMessage("Shapefile clippings have been merged.")

        return


# arcpy.env.workspace = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Test"  # dont think i actually need this
arcpy.env.overwriteOutput = True

def main():
    first_tool = Land_Cover_Class_Selection() # i.e. what you have called your tool class: class Clippy(object):
    first_tool.execute(first_tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()

def main():
    second_tool = Species_Heatmap()  # i.e. what you have called your tool class: class Clippy(object):
    second_tool.execute(second_tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()

def main():
    third_tool = Clip_and_Merge()  # i.e. what you have called your tool class: class Clippy(object):
    third_tool.execute(third_tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()
