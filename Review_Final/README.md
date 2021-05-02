# NRS 528 Final Project Info

These tools are part of an ArcPro Python Script Toolbox and has been coded for use inside ArcPro.  Each tool has user inputs required.  These tools are used to narrow down specific areas for study, merging selected areas into one shapefile, and creating a heatmap of the distribution of a species.  Sample data has been provided to use as an example with each tool.

- Land Cover Class Selection
  - A tool for selecting land cover classifications and narrowing down the target region.  Requires 2 shapefiles: a county shapefile with town feature classes, and a land cover classification shapefile.

- Species Heatmap
  - A tool for creating a heatmap of where a species was found from a CSV file.  Only works on CSV files with 1 species.

- Clip and Merge
  - A tool for clipping 2 target areas from a single shapefile and then merging them into 1 shapefile.  Only merges 2 areas.  Requires 3 shapefiles: 2 shapefiles to clip the target areas, and the shapefile that will be clipped.
