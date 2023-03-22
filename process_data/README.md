# Data processing
 
 This repository contains the source code used in the research article by Spinti et al. "How Small Dams Fragment and Regulate Rivers in the United States" at (insert doi here). 
 
 ## Running directions
 Basin(s) and year must be specified in run_workflow.py prior to running. The default setting is to run the all dams analysis (NABD). If running the large dam (GRanD) analysis, uncomment lines 158-159 in read.py.

 ## Script results
  All results are located in the folder that corresponds to the dam and year specified.

 #### extract.py
 *where basin is specified*
 - basin.csv

 #### run_workflow.py
 *where basin, HUC#, and year are specified*
  - basin_fragments_year.csv
  - basinHUC#_year_indices.csv
  - basin_segGeo_year.shp + .shx + .dbf + .prj