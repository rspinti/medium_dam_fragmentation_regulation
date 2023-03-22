# The Evolution of Dam Induced River Fragmentation in the United States
 
 This repository contains the source code used in the research article by Spinti et al. "The Evolution Dam Induced River Fragmentation in the United States" at (insert doi here). 
 
 ## Contents
 The names of the scripts needed to repeat this analysis are listed below. 
 - bifurcate.py
 - create_basin_csvs.py
 - create_csvs.py
 - dam_bar_plots.py
 - extract.py
 - fraglen_analysis.py
 - fraglen_plots.py
 - huc_merge.py
 - read.py
 - run_workflow.py
 - summarize.py

 ## Inputs
 Inputs to the code are available at the following locations.
 - National Anthropogenic Barrier Dataset (NABD): https://www.sciencebase.gov/catalog/item/56a7f9dce4b0b28f1184dabd
    - Download the shapefile
    - Andrea Ostroff, Daniel Wieferich, Arthur Cooper, Dana Infante, and USGS Aquatic GAP Program, 2013, 2012 National Anthropogenic Barrier Dataset (NABD): U.S. Geological Survey - Aquatic GAP Program: Denver, CO. 
 - National Hydrography Dataset Plus Version 2 (NHDPlus V2): https://www.epa.gov/waterdata/nhdplus-national-data
   - Download *NHDPlusV21_NationalData_Seamless_Geodatabase_Lower48_07.7z* and save NHDFlowline_Network as its own csv
 - Revised version of Global Reservoir and Dam Database (GRanD), missing large dams, and large dams with incorrect NABDID available in our Cyverse repository.

## Outputs
 All code outputs are available at (insert Cyverse DOI link here). 

## Python
The analysis was run with following version of Python and libraries. 
- Python 3.8.2
- geopandas 0.6.1
- matplotlib 3.5
- numpy 1.21.2
- pandas 1.3.5
- seaborn 0.11.2
- shapely 1.6.4

## Running directions
After the input data have been acquired, the codes are run in the following order.
1. run_workflow.py
2. summarize.py
3. dam_bar_plots.py
4. fraglen_plots.py
5. weibull_plots.py 

#
For further information on this repository, get in contact with the authors.
Rachel Spinti (rspinti@arizona.edu)
Laura Condon (lecondon@arizona.edu)

