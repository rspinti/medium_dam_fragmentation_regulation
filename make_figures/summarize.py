# %%
import geopandas as gp, pandas as pd, numpy as np
import create_csvs as crc, huc_merge as hm
# %%
#Specifying inputs
basin_ls = ['California', 'Colorado', 'Columbia', 'Great_Basin', 'Great_Lakes',
'Gulf_Coast','Mississippi', 'North_Atlantic', 'Red', 'Rio_Grande','South_Atlantic']
years = ['no_dams', '1920', '1950', '1980', '2010']
main_directory = 'Spinti_river_fragmentation_data_2022/'
results_folder = main_directory+'analyzed_data/'

for year in years:
    results_folder2 = results_folder+year+'/'
    print("---------------"+year+"---------------")

    #HUC analysis
    HUC_list=['HUC2','HUC4','HUC8']

    ## Create combined csv
    for huc in HUC_list:
        crc.combined_huc_csv(basin_ls, results_folder2, huc)

    ## Merge the combined csvs with HUC shapefiles
    huc2 = hm.HUC2_indices_merge(results_folder2, year)  #HUC2
    print("HUC 2 indices finished")
    huc4 = hm.HUC4_indices_merge(results_folder2, year)  #HUC4
    print("\n"+"HUC 4 indices finished")
    huc8 = hm.HUC8_indices_merge(results_folder2, year)    #HUC8
    print("\n" +"HUC 8 indices finished")

    #Create combined basin files
    crc.combined_segGeo_csv(basin_ls, results_folder2, year)
    crc.combined_frag_csv(basin_ls, results_folder2, year)
    print("\n" +"Create combined csvs finished")

print("\n"+"** Summarize by HUC and all_basins complete **")
# %%
