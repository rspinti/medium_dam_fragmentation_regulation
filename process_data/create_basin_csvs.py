
import pandas as pd, numpy as np, geopandas as gp, os
import datetime, read, extract as ex
from pathlib import Path

def create_basin_csvs(basin_ls, main_directory, results_folder, year):
    """Determines if a basin csv exists and create it if needed.

        This function passes in a list of basins and determines if a csv with each
        basin name exists. If the csv does not exist, it is created with read.py.
        The read_flag ensures that read.py is only executed once.

        Parameters:
            basin_ls (List):
                List of basins to be analyzed.
            folder (string):
                Folder where csvs will be saved.
            read_flag (boolean): 
                If False, flowlines and dams will be read in with read.py.
                If True, flowlines and dams will not be read in because they
                    already have been.
            flowlines (pandas.DataFrame):
                Dataframe containing all NHD flowlines from read.py.
            dams (pandas.DataFrame):
                Dataframe containing all dams from read.py.
                
        
        Returns:
            Csvs for each of the basins listed in basin_ls in a specified folder.
    """   
    ## If the specified basin csv does not exist, extract it
    os.chdir(results_folder)
    read_flag = False

    for basin in basin_ls:
        if os.path.isfile(basin+'.csv'):  #does it exist?
            #Read specified basin 
            print(basin + ': Exists')

        else:
            if read_flag == False:
                flowlines, dams = read.read_lines_dams(main_directory, year)
                read_flag = True
            print('\n', basin +  ': Does not exist')
            ex.join_dams_flowlines(basin, flowlines, dams)
            