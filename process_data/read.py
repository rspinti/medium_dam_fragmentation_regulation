import pandas as pd, numpy as np, geopandas as gp
from time import time

def read_lines_dams(main_directory, year):
    """Reads in dams and NHD flowlines for extraction by basin.

    This function is executed if the read_flag in create_csvs.py is False. It reads
    in NABD, then filters the data. Next, GRanD is read in to create the GRanD flag.
    NHD flowlines are read in and filtered to be joined with NABD in extract.py.

    Parameters:
        nabd_dams (pandas.DataFrame): 
            Dataframe providing NABD dam attributes. A unique DamID is added to 
            ID fragments in bifurcate.py. Duplicate dams were dropped.
            columns
                - COMID: Common ID of the NHD flowline, used to like NABD to NHD
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
                - Grand_flag: Identifies dams that are contained with GRanD
        
        dams_to_add (pandas.DataFrame): 
            Dataframe providing info about dams not in NABD. The missing
            dams came from GRanD. join_COMID was renamed COMID.
            columns
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - COMID: Common ID of the NHD flowline, used to like NABD to NHD
                - geometry: Point geometry for dam locations
        
        wrong_id (pandas.DataFrame): 
            Dataframe providing the correct NIDID. 
            columns
                - DAM_NAME: Name of the dam in NID
                - NIDID: Official unique dam ID (string) from NID
                - LONGITUDE: Longitude of the dam location
                - LATITUDE: Latitude of the dam location
                - YEAR_COMPLETED: Year when original dam structure was completed
                - MAX_STORAGE: Maximum storage of the reservoir in ac-ft
                - NORMAL_STORAGE: Normal storage of the reservoir in ac-ft
                - COMID: Common ID of the NHD flowline, used to like NABD to NHD
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - Dam_name: filled with nans
                - NABD_NIDID: Correct NIDID 
        
        grand (pandas.DataFrame):
            Dataframe providing GRanD dam attributes. Used to create a flag.
                - NABD_ID: Official unique dam ID (string) from NID
                - GRAND_ID: Official unique dam ID (string) from GRanD
        
        nabd (pandas.DataFrame): 
            Dataframe providing NABD dam attributes. Created from a join between
            NABD and GRanD to obtain values in Grand_flag.
            columns
                - COMID: Common ID of the NHD flowline, used to like NABD to NHD
                - NIDID: Official unique dam ID (string) from NID
                - Norm_stor: Normal storage of the reservoir in ac-ft
                - Max_stor: Maximum storage of the reservoir in ac-ft
                - Year_compl: Year when original dam structure was completed
                - Purposes: Abbreviations indicate current usage purpose
                - geometry: Point geometry for dam locations
                - DamID: Unique integer ID for each dam to use for fragments
                - Grand_flag: Identifies dams that are contained with GRanD (0:
                        not in GRand, 1: in GRanD)
        
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
                - COMID: Common ID of the NHD flowline
                - WKT: Geometry of flowline stored in WKT format
                - QE_MA: Estimate of actual mean flow
                - QC_MA: Estimate of “natural” mean flow
                - StreamOrde: Strahler stream order of the segment
                - HUC2: 2-digit HUC 
                - HUC4: 4-digit HUC 
                - HUC2: 8-digit HUC
        
        flowlines_nocoast (pandas.DataFrame): 
            Copy of flowlines dataframe to filter out coastlines.
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
                - COMID: Common ID of the NHD flowline
                - WKT: Geometry of flowline stored in WKT format
                - QE_MA: Estimate of actual mean flow
                - QC_MA: Estimate of “natural” mean flow
                - StreamOrde: Strahler stream order of the segment
                - HUC2: 2-digit HUC 
                - HUC4: 4-digit HUC 
                - HUC2: 8-digit HUC

    Returns:
        The dataframes flowlines and nabd for extract.py.
    """ 
 
    t0 = time()

    nabd_dams = gp.read_file(main_directory+"dam_data/nabd_fish_barriers_2012.shp")
    nabd_dams = nabd_dams[['COMID', 'NIDID', 'Norm_stor', 'Max_stor', 'Year_compl', 'Purposes', 'geometry']]
    nabd_dams = nabd_dams.drop_duplicates(subset='NIDID', keep="first")
    #print('Length of raw NABD', len(nabd_dams))

    dams_to_add = gp.read_file(main_directory+'dam_data/dams_to_add.shp')
    dams_to_add = dams_to_add[['NIDID','Norm_stor', 'Max_stor', 'Year_compl', 
                                'Purposes', 'join_COMID', 'geometry']].rename(columns={'join_COMID':'COMID'}) 
    nabd_dams = dams_to_add.append(nabd_dams)
    #print('Length of new NABD', len(nabd_dams))

    wrong_id = pd.read_csv(main_directory+'dam_data/large_dams_wrongID.csv', index_col = 0)
    wrong_id = wrong_id[wrong_id['NABD_NIDID'].notna()]
    wrong_id = wrong_id['NIDID']
    nabd_dams.update(wrong_id)

    nabd_dams['COMID'] = pd.to_numeric(nabd_dams['COMID'])
    nabd_dams["DamID"] = range(len(nabd_dams.COMID))  
    nabd_dams = pd.DataFrame(nabd_dams)
    nabd_dams['Grand_flag'] = np.zeros(len(nabd_dams))

    grand = pd.read_csv(main_directory+"dam_data/grand_dams.csv", 
                            usecols=['GRAND_ID', 'NABD_ID'])  
    grand['NABD_ID'] = grand['NABD_ID'].fillna(0)
    grand = grand[grand['NABD_ID']!=0]

    nabd = pd.merge(nabd_dams, grand, left_on = 'NIDID', right_on = 'NABD_ID', how = 'left')
    nabd['GRAND_ID'] = nabd['GRAND_ID'].fillna(0)
    nabd.loc[nabd.GRAND_ID != 0, 'Grand_flag'] = 1 
    nabd = nabd[nabd['NIDID']!='MI00650']

    #Select GRanD dams
    # nabd = nabd[nabd["GRand_flag"]==1]
    # print('Length of filtered NABD (GRanD)', len(nabd))

    #Filter dams by year_compl (for our case: no_dams, 1920, 1950, 1980, 2012)
    if year == 'no_dams':
        nabd = nabd.drop(columns=['COMID', 'geometry'])
        for col in nabd.columns:
            nabd[col].values[:] = 0
        nabd['COMID'] = nabd_dams['COMID']
        nabd['geometry'] = nabd_dams['geometry']
    elif year != 'no_dams' and int(year) < 2012:
        nabd = nabd[nabd['Year_compl'] < int(year)]
    else:
        nabd = nabd
    
    print("Length of nabd going to extract.py", len(nabd))
   
    t1 = time()

    flowlines = pd.read_csv(main_directory+"nhd/NHDFlowlines.csv",
                                usecols=['Hydroseq', 'UpHydroseq', 'DnHydroseq',
                                        'REACHCODE','LENGTHKM', 'StartFlag', 
                                        'FTYPE','COMID', 'WKT', 'QC_MA',
                                        'StreamOrde'])
    flowlines['HUC2'] = flowlines['REACHCODE']/(10**12) 
    flowlines['HUC4'] = flowlines['REACHCODE']/(10**10)
    flowlines['HUC8'] = flowlines['REACHCODE']/(10**6) 
    flowlines[['HUC2', 'HUC4', 'HUC8']] = flowlines[['HUC2', 'HUC4', 'HUC8']].apply(np.floor) 
    flowlines[['UpHydroseq', 'DnHydroseq', 'Hydroseq']] = flowlines[['UpHydroseq', 
                                                                        'DnHydroseq', 
                                                                        'Hydroseq']].round(decimals=0)
    flowlines_nocoast = flowlines.copy()
    flowlines = flowlines_nocoast[flowlines_nocoast["FTYPE"]!="Coastline"]
    
    t2 = time()

    print("Time to read in dams:", (t1-t0))
    print("Time to read in flowlines:", (t2-t1))

    return flowlines, nabd