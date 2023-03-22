"""
This script runs the river fragmentation and regulation data processing workflow.

Created by: Laura Condon and Rachel Spinti
"""
# %%
import pandas as pd, numpy as np, geopandas as gp, bifurcate as bfc, create_basin_csvs as cbc
import datetime, sys
from shapely import wkt
from pathlib import Path

# Select basin/basins to run from list below
basin_ls = ['California', 'Colorado', 'Columbia', 'Great_Basin', 'Great_Lakes',
'Gulf_Coast','Mississippi', 'North_Atlantic', 'Red', 'Rio_Grande','South_Atlantic']
# basin_ls = ['California', 'Colorado', 'Columbia', 'Great_Basin','Rio_Grande']
# basin_ls =  ['Great_Lakes', 'Gulf_Coast','Mississippi', 'North_Atlantic', 'Red', 'Rio_Grande','South_Atlantic']
year = '2012'

# Specify output location
main_directory = 'Spinti_river_fragmentation_data_2022/'
results_folder = main_directory+'analyzed_data/nabd_analyzed/'+str(year)+'/'

# %%
cbc.create_basin_csvs(basin_ls, main_directory, results_folder, year)

t_start = datetime.datetime.now()
for basin in basin_ls:
    # 1. Read  in the segment information for the basin
    segments = pd.read_csv(results_folder + basin + ".csv", index_col='Hydroseq',
                  usecols=['Hydroseq', 'UpHydroseq', 'DnHydroseq',
                            'LENGTHKM', 'StartFlag', 'DamCount',
                            'Coordinates', 'DamID',  'QC_MA', 'Norm_stor',
                            'HUC2', 'HUC4', 'HUC8', 'StreamOrde'])

    segments.QC_MA = (segments.QC_MA * 365 * 24 * 3600 * 0.0283168)/(10**6) #QC_MA = Average flow in cfs 
    segments.Norm_stor = (segments.Norm_stor * 1233.48)/(10**6) #Norm_stor =  normal storage in acre feet
    segments["line_width"] = segments["StreamOrde"]/10  #for graphing high Stream Orders thicker than low orders
    segments["new_width2"] = 'nan'  #for graphing DOR, so high Stream Orders are even thicker
    for i in segments.index:
        if segments.loc[i, 'line_width'] < 0.5:
            segments.loc[i, 'new_width2']=segments.loc[i, 'line_width']/2
        else:
            segments.loc[i, 'new_width2']=segments.loc[i, 'line_width']

    #__________________________________________________________

    # 2. Aggregate segment values by upstream area
    t0 = datetime.datetime.now()
    agg_list = ['Norm_stor', 'DamCount', 'LENGTHKM', 'QC_MA']
    segments_up = bfc.upstream_ag(data=segments, downIDs='DnHydroseq', 
                                agg_value=agg_list)
    
    t1 = datetime.datetime.now()
    print("---- "+basin+" Output"+" ----"+" \n")
    print("Aggregate by Upstream segments:", (t1-t0))

    # Add the resulting upstream aggregates back into segments DF with the upstream_count
    uplist=[i+'_up' for i in agg_list]
    segments[uplist]=segments_up[uplist]
    segments["upstream_count"] = segments_up["upstream_count"]

    #__________________________________________________________
    
    # 3.  Calculate Degree of Regulation 
    t2 = datetime.datetime.now()
    segments['DOR'] = segments.Norm_stor_up /  \
        segments.QC_MA 
    segments.DOR[(segments['QC_MA'] == 0) & (segments['Norm_stor_up'] >0)] = -1
    segments.DOR[segments['Norm_stor_up'] == 0] = 0

    t3 = datetime.datetime.now()
    print("Calculate DOR:", (t3-t2))

    #__________________________________________________________

    # 4. Divide into fragments and get average fragment properties
    t4 = datetime.datetime.now()
    segments = bfc.make_fragments(
        segments, exit_id=52000, verbose=False, subwatershed=True)
    t5 = datetime.datetime.now()
    print("Make Fragments:", (t5-t4))

    fragments = bfc.agg_by_frag(segments)
    fragments.to_csv(results_folder+basin+'_fragments'+'_' + year + '.csv')

    #__________________________________________________________
    
    # 5. Aggregate by HUC
    HUC_vallist=['HUC2','HUC4','HUC8']

    for HUC_val in HUC_vallist:
        HUC_summary = segments.pivot_table(values=['Norm_stor', 'DamCount', 'LENGTHKM'],
                                      index=HUC_val, aggfunc={'Norm_stor': (np.sum, np.max),
                                                                'DamCount': np.sum,
                                                                'LENGTHKM': np.sum})

        HUC_summary.columns = ["_".join((i,j)) for i,j in HUC_summary.columns]
        HUC_summary.reset_index()
        HUC_summaryf = fragments.pivot_table(values=['LENGTHKM'],  index=HUC_val, 
                                         aggfunc={'LENGTHKM': (np.mean, len, np.max)})
        HUC_summaryf.columns = ["_".join((i,j)) for i,j in HUC_summaryf.columns]
        HUC_summaryf.reset_index()
        HUC_summary = pd.concat([HUC_summary, HUC_summaryf], axis=1)

        seg_group = segments.groupby(HUC_val)
        seg_outlet = seg_group.LENGTHKM_up.idxmax() 
        HUC_summary['seg_outlet'] = seg_group.LENGTHKM_up.idxmax() #segment 'outlet'
        column_list = ['Frag', 'LENGTHKM_up', 'DOR', 'Norm_stor_up', 'QC_MA']
        outlet_vals = segments.loc[HUC_summary.seg_outlet, column_list]
        HUC_summary = HUC_summary.join(outlet_vals, on='seg_outlet', rsuffix='_outlet')
        add_suffix = [(i, i+'_outlet') for i in column_list]
        HUC_summary.rename(columns = dict(add_suffix), inplace=True)
        
        HUC_summary.to_csv(results_folder + basin + HUC_val+ "_" + year+'_indices.csv')
        print('Finished writing huc '+HUC_val+' indices to csv')

    #__________________________________________________________

    # 6. Make Segments into a geo dataframe for plotting
    segmentsGeo = segments.copy()
    segmentsGeo.Coordinates = segmentsGeo.Coordinates.astype(str)
    segmentsGeo['Coordinates'] = segmentsGeo['Coordinates'].apply(wkt.loads)
    segmentsGeo = gp.GeoDataFrame(segmentsGeo, geometry='Coordinates')

    segmentsGeo.to_file(basin + '_segGeo'+'_' + year + '.shp')
    #__________________________________________________________


t_end = datetime.datetime.now()
print('Time to run all basins = ', t_end-t_start)

# %%
