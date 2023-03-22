#%%
import geopandas as gp, pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as mtick, seaborn as sns
from numpy.core.fromnumeric import size
from decimal import Decimal, getcontext
sns.set_style("ticks", {"axes.facecolor": ".8"})
# %%
# Specify input locations
main_directory = 'Spinti_river_fragmentation_data_2022/'
data_folder = main_directory+'processed_data/'
results_folder = main_directory+'analyzed_data/'

#Inputs to plots
basin_ls = ['Great_Basin', 'Colorado', 'Rio_Grande', 'California', 'Gulf_Coast', 'Red', 
'Mississippi', 'Columbia', 'South_Atlantic', 'Great_Lakes', 'North_Atlantic']
# basin_ls = ['Great_Basin', 'Colorado', 'Rio_Grande']
basin_abr = ["GB", "CO", "RG", "CA", "GC", "RE", "MI", "CB", "SA", "GL", "NA"]
c_all_dams = ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fff66f', '#d1ef77', '#79ce6b', '#5bbb9d', '#3288bd', '#3952aa', '#4f438e']
c_big_dams = ['#740030', '#842532', '#9a422a', '#98683a', '#afa94c', '#86994c', '#416e39', '#326857', '#1b4c69', '#213063', '#2a244e']

# %%
#Plotting
fig, axs = plt.subplots(4, 1, sharex=True, sharey=False, figsize=(25, 30))
fig.subplots_adjust(hspace=0.05, wspace=0.2)
fig.patch.set_alpha(0)
pad=5

for count, basin in enumerate(basin_ls):
    big_dams = gp.read_file(data_folder+"grand_data/2010/"+basin+"_segGeo.shp", index_col='Hydroseq',
                    usecols=['Hydroseq', 'DamID','Norm_stor'])
    all_dams = gp.read_file(data_folder+"nabd_data/2010/"+basin+"_segGeo.shp", index_col='Hydroseq',
                    usecols=['Hydroseq', 'DamID', 'Norm_stor'])
    big_dams = big_dams[big_dams["DamID"]!=0]
    all_dams = all_dams[all_dams["DamID"]!=0]

    #Total # of dams plot
    all_dams_bar=axs[0].bar(basin,len(all_dams), label=basin, color = c_all_dams[count])
    axs[0].bar(basin,len(big_dams), label=basin, color = c_big_dams[count])
    all_dams_bar2 = axs[1].bar(basin,len(all_dams), label=basin, color = c_all_dams[count])
    axs[1].bar(basin,len(big_dams), label=basin, color = c_big_dams[count])

    ##Label and axes formatting
    axs[0].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    axs[0].yaxis.get_offset_text().set_fontsize(70)
    axs[0].tick_params(axis = 'both', which = 'major', labelsize = 70)
    axs[0].set_ylim(23000,25000)
    axs[1].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    axs[1].tick_params(axis = 'both', which = 'major', labelsize = 70)
    axs[1].set_ylim(0,10000)
    axs[1].set_xticklabels(basin_abr)
    fig.text(0.0001,0.76, "Total number of dams", ha="center", va="center", size = 72, weight='bold', rotation=90)

    ##Split the axis
    axs[0].spines.bottom.set_visible(False)
    axs[0].xaxis.tick_top()
    axs[0].tick_params(labeltop=False)
    axs[1].spines.top.set_visible(False)
    axs[1].xaxis.tick_bottom()
    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    axs[0].plot([0, 1], [0, 0], transform=axs[0].transAxes, **kwargs)
    axs[1].plot([0, 1], [1, 1], transform=axs[1].transAxes, **kwargs)

    ##Adding the percent contribution of small dams
    fraction = 1-(len(big_dams)/len(all_dams))
    rfraction = Decimal(str(round(fraction, 3)))
    getcontext().prec = 3
    for rect in all_dams_bar:
        height = rect.get_height()
        if height < 20000:
            axs[1].text(rect.get_x() + rect.get_width()/1.6, 1.01*height,
                    str(rfraction*100)+"%", ha='center', va='bottom', rotation=0, size=38)
        else:
            axs[0].text(rect.get_x() + rect.get_width()/1.6, 1*height,
                    str(rfraction*100)+"%", ha='center', va='bottom', rotation=0, size=38)    

    #Total storage plot
    all_dams_sbar = axs[2].bar(basin,sum(all_dams.Norm_stor), color = c_all_dams[count])
    axs[3].bar(basin,sum(all_dams.Norm_stor), color = c_all_dams[count])
    axs[2].bar(basin,sum(big_dams.Norm_stor), color = c_big_dams[count])
    axs[3].bar(basin,sum(big_dams.Norm_stor), color = c_big_dams[count])
    
    ##Label and axes formatting
    axs[2].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    axs[2].yaxis.get_offset_text().set_fontsize(70)
    axs[2].tick_params(axis = 'both', which = 'major', labelsize = 70)
    axs[2].set_ylim(180000,200000)
    axs[3].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    axs[3].tick_params(axis='both', which='major', labelsize=70)
    axs[3].set_ylim(0,130000)
    axs[3].set_xlabel("Basin", size=72, weight='bold')
    fig.text(0.0000001,0.3, "Total storage (MCM)", ha="center", va="center", size = 72, weight = 'bold', rotation=90)

    ##Adding the percentage of small dams
    all_dams_stor= sum(all_dams.Norm_stor)
    big_dams_stor = sum(big_dams.Norm_stor)
    fraction2 = round(1-(big_dams_stor/all_dams_stor), 3)
    rfraction2 = Decimal(str(fraction2))
    if rfraction2 > 0.08:
        getcontext().prec = 3
    else:
        getcontext().prec = 2
    
    for rec in all_dams_sbar:
        height = rec.get_height()
        if height < 180000:
            axs[3].text(rec.get_x() + rec.get_width()/1.6, 1.01*height,
                    str(rfraction2*100)+"%", ha='center', va='bottom', rotation=0, size=38)
        else:
            axs[2].text(rec.get_x() + rec.get_width()/1.6, 1*height,
                    str(rfraction2*100)+"%", ha='center', va='bottom', rotation=0, size=38)  

    ##Hide the spines between axes
    axs[2].spines.bottom.set_visible(False)
    axs[3].spines.top.set_visible(False)
    axs[2].xaxis.tick_top()
    axs[3].tick_params(labeltop=False)
    axs[2].xaxis.tick_bottom()
    d = .5
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    axs[2].plot([0, 1], [0, 0], transform=axs[2].transAxes, **kwargs)
    axs[3].plot([0, 1], [1, 1], transform=axs[3].transAxes, **kwargs)

    plt.tight_layout(rect=[0.05, 0, 0.95, 1])
    # plt.savefig(results_folder+"bar_plots/together.png", bbox_inches='tight')
# %%
