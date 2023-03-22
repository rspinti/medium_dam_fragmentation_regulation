
import numpy as np, pandas as pd
from time import time


def join_dams_flowlines(basin, flowlines, nabd):
    """Creates a new filtered dataset from the dams and flowlines.

    This function obtains and filters NHDPlus V2 and NABD for analysis in 
    bifurcate.py. The NHD flowlines are split into major U.S. river basins by 
    their HUC 2 for processing. Dams are then joined to each basin by COMID.

    Parameters:
        flowlines (pandas.DataFrame): 
            Dataframe containing NHD flowline attributes necessary for processing.
            Each data entry is considered a flowline segment.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - UpHydroseq: Unique segment ID for the upstream segment
                - DnHydroseq: Unique segment ID for the downstream segment
                - REACHCODE: 14-digit Hydrologic Unit Code (HUC) from the USGS
                - LENGTHKM: Length of segment in km
                - StartFlag: Flag to indicate if segment is a headwater (0 = not
                headwater, 1 = headwater)
                - FTYPE: Type of flowline
                - COMID: Common ID of the NHD flowline, used to link NABD to NHD
                - WKT: Line geometry of flowlines stored in WKT format
                - QE_MA: Estimate of actual mean flow
                - QC_MA: Estimate of “natural” mean flow
                - StreamOrde: Strahler stream order of the segment
                - HUC2: 2-digit HUC 
                - HUC4: 4-digit HUC 
                - HUC2: 8-digit HUC 
                
        nabd (pandas.DataFrame): 
            Dataframe providing dam attributes. A unique DamID is added to ID
            fragments in bifurcate.py. Duplicate dams were dropped.
            columns
                - COMID: Common ID of the NHD flowline, used to link NABD to NHD
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
                
        basin (string):
            Specified in the main script to run a particular basin. Major river 
            basins include:
            'California', 'Colorado', 'Columbia', 'Great Basin', 'Great Lakes',
            'Gulf Coast','Mississippi', 'North Atlantic', 'Red', 'Rio Grande',
            'South Atlantic'
                
        major_basins (list): 
            List of the major U.S. river basins that correspond to the basin.
            HUC 2 values are used to filter flowlines into major river 
            basin groupings.
            
        nabd_nhd_join (pandas.DataFrame):
            Dataframe containing dam and flowline attributes related by COMID.
            The data is joined using the merge function and takes its queue 
            from the NABD COMID.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - UpHydroseq: Unique segment ID for the upstream segment
                - DnHydroseq: Unique segment ID for the downstream segment
                - HUC2: 2-digit HUC 
                - LENGTHKM: Length of segment in km
                - StartFlag: Flag to indicate if segment is a headwater (0 = not
                headwater, 1 = headwater)
                - FTYPE: Type of flowline
                - WKT: Line geometry of flowlines stored in WKT format
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
                
        storage_sum (pandas.DataFrame):
            Dataframe created from the groupby function. The data is grouped
            by Hydroseq and Norm_stor summed among each Hydroseq. This accounts
            for storage values of multiple dams lying on one segment.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - Norm_stor: Normal storage of the reservoir in ac-ft
            
        dam_count (pandas.Dataframe):
            Dataframe obtained from a pandas pivot table. The data was grouped
            by Hydroseq and then the number of occurences of each Hydroseq was
            summed to get the Dam_Count for each segment.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - Dam_Count: Indicates the number of dams along a segment
        
        count_sum_merge (pandas.DataFrame): 
            Dataframe that contains the Dam_Count and Norm_stor values from
            storage_sum and dam_count. Hydroseq was used to merge storage_sum
            and dam_count.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines 
                in hydrologic order
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Dam_Count: Indicates the number of dams along a segment

        nabd_nhd_filtered (pandas.DataFrame): 
            GeoDataframe that filters out the Norm_stor and Dam_Count columns as 
            well as duplicate entries. This allows us to merge in the data from
            count_sum_merge.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - UpHydroseq: Unique segment ID for the upstream segment
                - DnHydroseq: Unique segment ID for the downstream segment
                - HUC2: 2-digit HUC 
                - LENGTHKM: Length of segment in km
                - StartFlag: Flag to indicate if segment is a headwater (0 = not
                headwater, 1 = headwater)
                - FTYPE: Type of flowline
                - WKT: Line geometry of flowlines stored in WKT format
                - NIDID: Official unique dam ID (string) from NID
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
            
        nabd_nhd_df (geopandas.geodataframe.GeoDataFrame):
            GeoDataframe that contains the filtered Hydroseq, Norm_stor, and 
            Dam_count values. It also contains all prior attributes that are 
            needed for bifurcate.py.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - UpHydroseq: Unique segment ID for the upstream segment
                - DnHydroseq: Unique segment ID for the downstream segment
                - HUC2: 2-digit HUC 
                - LENGTHKM: Length of segment in km
                - StartFlag: Flag to indicate if segment is a headwater (0 = not
                headwater, 1 = headwater)
                - FTYPE: Type of flowline
                - WKT: Line geometry of flowlines stored in WKT format
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
                - Dam_Count: Indicates the number of dams along a segment

        segments_df (geopandas.geodataframe.GeoDataFrame):
            GeoDataframe that contains the filtered Hydroseq, Norm_stor, and 
            Dam_count values for a specific basin. It also contains all prior 
            attributes that are needed for bifurcate.py.
            columns
                - Hydroseq: Unique segment ID for current segment, places flowlines
                in hydrologic order
                - UpHydroseq: Unique segment ID for the upstream segment
                - DnHydroseq: Unique segment ID for the downstream segment
                - HUC2: 2-digit HUC 
                - LENGTHKM: Length of segment in km
                - StartFlag: Flag to indicate if segment is a headwater (0 = not
                headwater, 1 = headwater)
                - FTYPE: Type of flowline
                - WKT: Line geometry of flowlines stored in WKT format
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
                - Dam_Count: Indicates the number of dams along a segment 
        
    Returns:
        segments_df (geopandas.geodataframe.GeoDataFrame): A dataframe with filtered dam and 
        flowline attributes.
        'basin'+.csv (csv): csv file to be read into the main script
    
    """
    major_basins = {'California' : [18],
                    'Colorado' : [14, 15],
                    'Columbia' : [17],
                    'Great_Basin' : [16], 
                    'Great_Lakes' : [4],
                    'Gulf_Coast' : [12],
                    'Mississippi' : [5, 6, 7, 8, 10, 11],
                    'North_Atlantic' : [1, 2],
                    'Red' : [9],
                    'Rio_Grande' : [13],
                    'South_Atlantic' : [3]}
    
    t1 = time()
    if basin == 'California':
        california = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])] 
        nabd_nhd_join = nabd.merge(california, how= 'right', on='COMID') 
    
    if basin == 'Colorado':
        colorado = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])| 
        (flowlines['HUC2'] == major_basins[basin][1])]
        nabd_nhd_join = nabd.merge(colorado, how= 'right', on='COMID') 
    
    if basin == 'Columbia':
        columbia = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(columbia, how= 'right', on='COMID')
    
    if basin == 'Great_Basin':
        great_basin = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(great_basin, how= 'right', on='COMID')
    
    if basin == 'Great_Lakes':
        great_lakes = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(great_lakes, how= 'right', on='COMID')
    
    if basin == 'Gulf_Coast':
        gulf_coast = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(gulf_coast, how= 'right', on='COMID') 
        
    if basin == 'Mississippi':
        mississippi = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])|
        (flowlines['HUC2'] == major_basins[basin][1]) |
        (flowlines['HUC2'] == major_basins[basin][2]) |
        (flowlines['HUC2'] == major_basins[basin][3]) | 
        (flowlines['HUC2'] == major_basins[basin][4]) |
        (flowlines['HUC2'] == major_basins[basin][5])]
        nabd_nhd_join = nabd.merge(mississippi, how= 'right', on='COMID')
        
    if basin == 'North_Atlantic':
        north_atlantic = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])|
        (flowlines['HUC2'] == major_basins[basin][1])]
        nabd_nhd_join = nabd.merge(north_atlantic, how= 'right', on='COMID')
    
    if basin == 'Red':
        red = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(red, how= 'right', on='COMID')
    
    if basin == 'Rio_Grande':
        rio_grande = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(rio_grande, how= 'right', on='COMID')
    
    if basin == 'South_Atlantic':
        south_atlantic = flowlines.loc[(flowlines['HUC2'] == major_basins[basin][0])]
        nabd_nhd_join = nabd.merge(south_atlantic, how= 'right', on='COMID') 
    
    t2 = time()
    
    nabd_nhd_join.insert(5, "step", np.zeros(len(nabd_nhd_join)), True)
    storage_sum = nabd_nhd_join.groupby(['Hydroseq'])['Norm_stor'].sum().reset_index()
    nabd_nhd_join['DamCount'] = np.zeros(len(nabd_nhd_join)) 
    dam_count = nabd_nhd_join.pivot_table(index=['Hydroseq'], aggfunc={'DamCount':'size'}).reset_index() 
    count_sum_merge = storage_sum.merge(dam_count, how= 'left', on='Hydroseq')
  
    nabd_nhd_filtered = nabd_nhd_join.drop_duplicates(subset='Hydroseq', keep="last") 
    nabd_nhd_filtered = nabd_nhd_filtered.drop(columns=['Norm_stor', 'DamCount'])

    nabd_nhd_df = nabd_nhd_filtered.merge(count_sum_merge, how= 'left', on='Hydroseq')
    nabd_nhd_df['DamID'] = nabd_nhd_df['DamID'].fillna(0)
    nabd_nhd_df.loc[nabd_nhd_df.DamID==0, 'DamCount'] = 0 
    nabd_nhd_df = nabd_nhd_df.set_index('Hydroseq')
    nabd_nhd_df = nabd_nhd_df.rename(columns={'WKT': 'Coordinates'})
    
    t3 = time()
  
    segments_df = nabd_nhd_df.copy()
    segments_df.to_csv(basin+'.csv')  
    print('Finished writing segments_df to csv..........')
    
    t4 = time() 
    print("---- "+basin+" TIMING SUMMARY -----")
    print('Select basin', t2-t1)
    print('Filtering', t3-t2)
    print('Write to csv', t4-t3)
    
    return segments_df

