# Final project for NRS 528
# Python Toolbox for ArcPro that has 3 different tools in it
#     Land_Cover_Class_Selection: A tool for selecting land cover classifications and narrowing down the target region.
#     Species_Heatmap: A tool for creating a heatmap of where a species was found from a CSV file.  Only works on CSV files with 1 species.
#     Clip_and_Merge: A tool for clipping target areas from a shapefile and then merging them into 1 shapefile.  Only merges 2 areas.

import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Land_Cover_Class_Selection,Species_Heatmap, Clip_and_Merge]

class Land_Cover_Class_Selection(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Land Cover Class Selection"
        self.description = "Selects a county from a shapefile of multiple counties and uses that as the clipping region for when selecting a land cover class"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []  # List of parameters
        input_workspace = arcpy.Parameter(name="input_workspace",
                                          displayName="Input Workspace (Select a folder)",
                                          datatype="DEFolder",
                                          parameterType="Required",
                                          direction="Input",
                                          )
        params.append(input_workspace)  # This is parameters[0].  Workspace required for part of heatmap creation process.

        input_shapefile = arcpy.Parameter(name="input_shapefile",  # Name of parameter
                                     displayName="Input Counties Shapefile (Ex: Towns_Washington.shp)",  # What will be seen when filling inputs/outputs
                                     datatype="DEShapefile",  # Limits what can be put into the parameter
                                     parameterType="Required",  # Makes it so the parameter has to be filled to be able to use the tool
                                     direction="Input",  # Input/Output
                                     )
        params.append(input_shapefile)  # This is parameters[1].  This is the shapefile that the town will be selected from.

        input_string = arcpy.Parameter(name="input_string",
                                    displayName="Input Township Name In Uppercase (Ex: SOUTH KINGSTOWN)",
                                    datatype="GPString",
                                    parameterType="Required",
                                    direction="Input",
                                    )
        params.append(input_string)  # This is parameters[2].  This is the name of the town used in the select tool.

        output_shapefile = arcpy.Parameter(name="output_shapefile",
                                    displayName="Selected Town Output (Ex: Township.shp)",
                                    datatype="DEShapefile",
                                    parameterType="Required",
                                    direction="Output",
                                    )
        params.append(output_shapefile)  # This is parameters[3].  This is output for the first select tool.  Also used for as the clip feature.

        input_land_class_shapefile = arcpy.Parameter(name="input_land_class_shapefile",
                                      displayName="Input Land Class Shapefile (Ex: Land_Cover_2011_RI_State_Plane_reduced.shp)",
                                      datatype="DEShapefile",
                                      parameterType="Required",
                                      direction="Input",
                                      )
        params.append(input_land_class_shapefile)  # This is parameters[4].  This is the land cover class shapefile input for the clip tool.

        output_clip_shapefile = arcpy.Parameter(name="output_clip_shapefile",
                                 displayName="Clipped Land Cover Class Output (Ex: Town_land_cover.shp)",
                                 datatype="DEShapefile",
                                 parameterType="Required",
                                 direction="Output",
                                 )
        params.append(output_clip_shapefile)  # This is parameters[5].  This is output for the clip tool.  Will be used in the select tool.

        input_string_2 = arcpy.Parameter(name="input_string_2",
                                       displayName="Input A Land Cover Type (Ex: Water)",
                                       datatype="GPString",
                                       parameterType="Required",
                                       direction="Input",
                                       )
        params.append(input_string_2)  # This is parameters[6].  This is the name of the land class type used in the select tool.

        input_string_3 = arcpy.Parameter(name="input_string_3",
                                         displayName="Input An Additional Land Cover Type (Ex: Wetland)",
                                         datatype="GPString",
                                         parameterType="Required",
                                         direction="Input",
                                         )
        params.append(input_string_3)  # This is parameters[7].  This is the name of an additional land class type used in the select tool.

        output_final_select = arcpy.Parameter(name="output_final_select",
                                 displayName="Output Final Shapefile (Ex: Town_water.shp)",
                                 datatype="DEShapefile",
                                 parameterType="Required",
                                 direction="Output",
                                 )
        params.append(output_final_select)  # This is parameters[8].  The final output.  Should be just the selected land cover class within that target region.

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
        arcpy.env.workspace = workspace  # Sets the workspace

        # First, selecting the target region from the towns within the county
        input_shape = parameters[1].valueAsText  # Parameters be converted and saved as strings
        input_string = parameters[2].valueAsText
        output_shape = parameters[3].valueAsText

        expression = "NAME = " + "'" + input_string + "'"  # Creates the expression used for selecting the town from the counties
        arcpy.AddMessage("The expression used for the select tool is: " + expression)  # Prints a message of what the expression is

        arcpy.Select_analysis(in_features=input_shape,   # Selects the township from the county
                              out_feature_class=output_shape,
                              where_clause=expression
                              )
        arcpy.AddMessage("Done selecting township.")

        #  Next is to use the selected town as the clip feature
        input_shape_2 = parameters[4].valueAsText
        output_2 = parameters[5].valueAsText

        arcpy.Clip_analysis(in_features=input_shape_2,   # Narrows down the land types to only use the ones within the township
                            clip_features=output_shape,
                            out_feature_class=output_2,
                            cluster_tolerance=""
                            )
        arcpy.AddMessage("Done clipping town land cover classes.")

        input_string_2 = parameters[6].valueAsText
        input_string_3 = parameters[7].valueAsText
        output_select = parameters[8].valueAsText

        # Last is to select the land cover class types so that all will remain is the selected land cover within the clipped area
        expression = "Descr_2011 = " + "'" + input_string_2 + "'" + " Or " + "Descr_2011 = " + "'" + input_string_3 + "'"  # Expression for selecting which land cover types
        arcpy.AddMessage("The expression used for the select tool is: " + expression)

        arcpy.Select_analysis(in_features=output_2,  # Selects the chosen land cover types
                              out_feature_class=output_select,
                              where_clause=expression
                              )
        arcpy.AddMessage("Done selecting land cover.")

        # Checks if the last Select output has been created, then deletes the intermediate files
        if arcpy.Exists(output_select):
            arcpy.AddMessage("Created merged shapefile, will now delete intermediate files")
            arcpy.Delete_management(output_shape)
            arcpy.Delete_management(output_2)
            arcpy.AddMessage("Deleted intermediate files")

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
                                   parameterType="Required",
                                   direction="Input",
                                   )
        params.append(input_workspace)  # This is parameters[0].  Workspace required for part of heatmap creation process.

        input_csv = arcpy.Parameter(name="input_csv_file",
                                     displayName="Input Single Species CSV File (Ex: Cepphus_grylle.csv)",
                                     datatype="DEFile",
                                     parameterType="Required",
                                     direction="Input",
                                     )
        # input_csv.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Cepphus_grylle.csv"
        params.append(input_csv)  # This is parameters[1]. Species data in CVS format.

        input_string = arcpy.Parameter(name="input_string",
                                    displayName="Input Single Species Name (No Spaces; Ex: Cepphus_grylle)",
                                    datatype="GPString",
                                    parameterType="Required",
                                    direction="Input",
                                    )
        # input_string.value = "Cepphus_grylle"
        params.append(input_string)  # This is parameters[2].  Needs the species name for file creation

        output_file = arcpy.Parameter(name="output_file",
                                    displayName="Species Heatmap Output (Ex: HeatMap_Cepphus_grylle.shp)",
                                    datatype="DEShapefile",
                                    parameterType="Required",
                                    direction="Output",
                                    )
        # output_file.value = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Projects\Final\Data\Output\HeatMap_Cepphus_grylle.shp"
        params.append(output_file)  # This is parameters[3].  User created output name.

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
        arcpy.env.workspace = workspace  # Sets the workspace

        input_file = parameters[1].valueAsText
        input_string = parameters[2].valueAsText
        output_file = parameters[3].valueAsText

        output_temp = input_string + '_output.shp'  # Creates an object to use as a temporary output file

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

        # Checks if the heatmap has been created, then deletes the intermediate files
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
        input_workspace = arcpy.Parameter(name="input_workspace",
                                          displayName="Input Workspace (Select a folder)",
                                          datatype="DEFolder",
                                          parameterType="Required",
                                          direction="Input",
                                          )
        params.append(input_workspace)  # This is parameters[0].  Workspace required for part of heatmap creation process.

        input_shape = arcpy.Parameter(name="input_shape",
                                        displayName="Input First Shapefile (Ex: South_Rhode_Island_Buildings.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Input",
                                        )
        params.append(input_shape)  # This is parameters[1].  This is the data that will be clipped and then merged together

        input_clip_1 = arcpy.Parameter(name="input_clip_1",
                                     displayName="Input Shapefile to use for First Clipping (Ex: URI_Campus.shp)",
                                     datatype="DEShapefile",
                                     parameterType="Required",
                                     direction="Input",
                                     )
        params.append(input_clip_1)  # This is parameters[2].  Polygon of the area used for the first clipping

        clip_1_output = arcpy.Parameter(name="clip_1_output",
                                        displayName="First Clipping Output (Ex: clip_1.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Output",
                                        )
        params.append(clip_1_output)  # This is parameters[3].  Output of the for clipping

        input_clip_2 = arcpy.Parameter(name="input_clip_2",
                                     displayName="Input Shapefile to use for Second Clipping (Ex: Bay_Campus.shp)",
                                     datatype="DEShapefile",
                                     parameterType="Required",
                                     direction="Input",
                                     )
        params.append(input_clip_2)  # This is parameters[4]. Polygon of the area used for the second clipping

        clip_2_output = arcpy.Parameter(name="clip_2_output",
                                        displayName="Second Clipping Output (Ex: clip_2.shp)",
                                        datatype="DEShapefile",
                                        parameterType="Required",
                                        direction="Output",
                                        )
        params.append(clip_2_output)  # This is parameters[5].  Output of the second clipping

        merge_output = arcpy.Parameter(name="merge_output",
                                       displayName="Merge Output (Ex: merge.shp)",
                                       datatype="DEShapefile",
                                       parameterType="Required",
                                       direction="Output",
                                       )
        params.append(merge_output)  # This is parameters[6].  Output of the merge

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
        arcpy.env.workspace = workspace  # Sets the workspace

        input_shape = parameters[1].valueAsText
        input_polygon = parameters[2].valueAsText
        output = parameters[3].valueAsText

        input_polygon_2 = parameters[4].valueAsText
        output_2 = parameters[5].valueAsText

        input_shapes = [output, output_2]  # List of inputs for the merge tool using the outputs of both clip tools
        output_merge = parameters[6].valueAsText

        # First Clip
        arcpy.Clip_analysis(in_features=input_shape,
                            clip_features=input_polygon,
                            out_feature_class=output,
                            cluster_tolerance="")
        arcpy.AddMessage("First clipping has been completed.")

        # Second Clip
        arcpy.Clip_analysis(in_features=input_shape,
                            clip_features=input_polygon_2,
                            out_feature_class=output_2,
                            cluster_tolerance="")
        arcpy.AddMessage("Second clipping has been completed.")

        # Merge
        arcpy.Merge_management(inputs=input_shapes,
                               output=output_merge,
                               field_mappings="",
                               add_source="")
        arcpy.AddMessage("Shapefile clippings have been merged.")

        # Checks if the merge file has been created, then deletes the intermediate files
        if arcpy.Exists(output_merge):
            arcpy.AddMessage("Created merged shapefile, will now delete intermediate files")
            arcpy.Delete_management(output)
            arcpy.Delete_management(output_2)
            arcpy.AddMessage("Deleted intermediate files")

        return
