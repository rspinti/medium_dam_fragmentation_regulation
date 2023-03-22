# %%
from matplotlib import pyplot as plt
import pandas as pd, numpy as np, geopandas as gp, os
from pathlib import Path

# Specify inputs locations
main_directory = 'Spinti_river_fragmentation_data_2022/'
data_folder = main_directory+'processed_data/'
results_folder = main_directory+'analyzed_data/'

basins = ['Great_Basin', 'Rio_Grande', 'Gulf_Coast', 'Columbia', 'Great_Lakes', 'all_basins']
dam_dict = {'no_dams':['nabd_data', 'no_dams'],'all_dams':['nabd_data', '2010'],'large_dams':['grand_data', '2010']}

c_all_dams = ['#9e0142', '#f46d43', '#fff66f', '#5bbb9d','#3952aa', '#a5a5a5']
c_big_dams = ['#740030', '#9a422a', '#afa94c', '#326857', '#213063', '#636262']
c_no_dams = ['black']
color_dict = {z[0]: list(z[1:]) for z in zip(basins, c_all_dams, c_big_dams)}
# %%
for basin, c in color_dict.items():
    fig = plt.figure()
    ax = fig.add_subplot()
    for k,v in dam_dict.items():
        basin_frags = pd.read_csv(gdrive+data_folder+v[0]+"/"+v[1]+"/"+basin+"_fragments.csv")
        frag_weibull = basin_frags[["LENGTHKM", "Frag_Index"]].copy()
        frag_weibull['rank'] = frag_weibull['LENGTHKM'].rank(method='dense', ascending=False)
        frag_weibull['weibull'] = frag_weibull['rank']/len(frag_weibull['LENGTHKM']+1)
        if k == 'no_dams':
            k = k.replace("_", " ")
            plt.scatter(frag_weibull["weibull"], frag_weibull["LENGTHKM"], label=k, color='black')
        elif k == 'all_dams':
            k = k.replace("_", " ")
            plt.scatter(frag_weibull["weibull"], frag_weibull["LENGTHKM"], label=k, color=c[0])
        else:
            k = k.replace("_", " ")
            plt.scatter(frag_weibull["weibull"], frag_weibull["LENGTHKM"], label=k, color=c[1])
     
    ax.set_xscale('log')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.yaxis.get_offset_text().set_fontsize(12)
    plt.xlabel("Exceedance probability", size =14)
    plt.ylabel("Fragment length (km)", size=14)
    basin = basin.replace("_", " ")
    if basin != 'all basins':
        plt.title(basin, size=15)
        plt.legend()
        plt.tight_layout()
        fig.show()
        fig.savefig(gdrive+results_folder+'weibull/'+basin+'_weibull.png', dpi = 150)
    else:
        basin = 'CONUS'
        plt.title(basin, size=15)
        plt.legend()
        plt.tight_layout()
        fig.show()
        fig.savefig(gdrive+results_folder+'weibull/'+basin+'_weibull.png', dpi = 150)

# %%
