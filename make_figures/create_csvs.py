
import pandas as pd, numpy as np, geopandas as gp, os
from pathlib import Path
            
def combined_huc_csv(basin_ls, results_folder, huc):
    """Combines all the basins together into one csv by HUC.

        This function takes a list of basins and creates a combined csv. The 
        list of basins is used to read in each corresponding csv, which are 
        concatenated into the same dataframe. That combined dataframe is then 
        printed out to csv.

        Parameters:
            basin_ls (List):
                List of basins whose csvs will be read in.
            folder (string):
                Folder on the Google Drive where csv are be saved.
            huc (string):
                HUC value to be evaluated.
            extension (string):
                Csv extension that varies by HUC value.
            HUC_summary_list (List):
                List of basin names with their HUC extension added.
            combined_csv (pandas.DataFrame):
                Dataframe that contains all basins.
                columns
                    add columns here with descriptions
    

        Returns:
            A single csv containing all the data from each basin csv.
    """        
    os.chdir(results_folder)

    # Make list of names of files to be read in (by basin and HUC value)
    extension = huc+'_indices.csv'
    HUC_summary_list = [i+extension for i in basin_ls]

    # Combine all basin csvs together into a dataframe
    combined_csv = pd.concat([pd.read_csv(f) for f in HUC_summary_list])

    # Export to csv 
    combined_csv.to_csv(results_folder+huc+"_summary.csv", index=False, encoding='utf-8-sig')
    
    
def combined_segGeo_csv(basin_ls, results_folder, year):
    """Combines all the basins together into one csv.

        This function takes a list of basins and creates a combined csv. The 
        list of basins is used to read in each corresponding csv, which are 
        concatenated into the same dataframe. That combined dataframe is then 
        printed out to csv.

        Parameters:
            basin_ls (List):
                List of basins whose csvs will be read in.
            folder (string):
                Folder on the Google Drive where csv are be saved.
            huc (string):
                HUC value to be evaluated.
            extension (string):
                Csv extension that varies by HUC value.
            HUC_summary_list (List):
                List of basin names with their HUC extension added.
            combined_csv (pandas.DataFrame):
                Dataframe that contains all basins.
                columns
                    add columns here with descriptions
    

        Returns:
            A single csv containing all the data from each basin csv.
    """        
    os.chdir(results_folder)

    # Make list of names of files to be read in (by basin and HUC value)
    extension = '_segGeo.shp'
    basin_summary_list = [i+extension for i in basin_ls]

    # Combine all basin csvs together into a dataframe
    combined_csv = pd.concat([gp.read_file(b) for b in basin_summary_list])
    print("all basins added")
    
    os.chdir(results_folder)
    # Export to shp 
    # combined_csv.to_csv("all_basins_segGeo.csv", index=False, encoding='utf-8-sig')
    combined_csv.to_file("all_basins_segGeo_"+year+".shp")
    print("combined shapefile written")
    # print(type(combined_csv))

    return combined_csv
    
def combined_frag_csv(basin_ls, results_folder, year):
    """Combines all the basins together into one csv.

        This function takes a list of basins and creates a combined csv. The 
        list of basins is used to read in each corresponding csv, which are 
        concatenated into the same dataframe. That combined dataframe is then 
        printed out to csv.

        Parameters:
            basin_ls (List):
                List of basins whose csvs will be read in.
            folder (string):
                Folder on the Google Drive where csv are be saved.
            huc (string):
                HUC value to be evaluated.
            extension (string):
                Csv extension that varies by HUC value.
            HUC_summary_list (List):
                List of basin names with their HUC extension added.
            combined_csv (pandas.DataFrame):
                Dataframe that contains all basins.
                columns
                    add columns here with descriptions
    

        Returns:
            A single csv containing all the data from each basin csv.
    """        
    os.chdir(results_folder)

    # Make list of names of files to be read in (by basin and HUC value)
    extension = '_fragments.csv'
    basin_summary_list = [i+extension for i in basin_ls]

    # Combine all basin csvs together into a dataframe
    combined_csv = pd.concat([pd.read_csv(b) for b in basin_summary_list])
    print("all basins added")
    
    os.chdir(results_folder)
    # Export to shp 
    # combined_csv.to_csv("all_basins_segGeo.csv", index=False, encoding='utf-8-sig')
    combined_csv.to_csv("all_basins_frags_"+year+".csv")
    print("combined fragment csv written")
    # print(type(combined_csv))

    return combined_csv

