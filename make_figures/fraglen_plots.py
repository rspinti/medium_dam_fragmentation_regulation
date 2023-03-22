
import geopandas as gp, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
import fraglen_analysis as fla
from matplotlib.pyplot import cm

sns.set_style("ticks", {"axes.facecolor": ".8"})

# Specify input locations
main_directory = 'Spinti_river_fragmentation_data_2022/'
data_folder = main_directory+'processed_data/'
results_folder = main_directory+'analyzed_data/'
plot_folder = main_directory+'analyzed_data/len_analysis/'
huc2 = gp.read_file(main_directory+"hucs/huc2_clipped.shp")

basin_ls = ['Great_Basin', 'Colorado', 'Rio_Grande', 'California', 'Gulf_Coast', 'Red', 
'Mississippi', 'Columbia', 'South_Atlantic', 'Great_Lakes', 'North_Atlantic', 'all_basins']

#Number of fragments per HUC 8
fla.frag_diff(results_folder)

#Plotting by fragment length over time
years = ["no_dams", "1920", "1950", "1980", "2010"]
bin_ls = [0, 10, 100, 1000, 10000]
lengths = bin_ls[1:]
length_dict={10: '0 - 10 km', 100: '10 - 100 km', 1000: '100 - 1,000 km', 10000: '1,000 - 10,000 km'}

##Plot labels
xlabels =["PD", "1920", "1950", "1980", "2010"]
basin_abr = ["GB", "CO", "RG", "CA", "GC", "RE", "MI", "CB", "SA", "GL", "NA", "CONUS"]
colors = ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fff66f', '#d1ef77', '#79ce6b', '#5bbb9d', '#3288bd', '#3952aa', '#4f438e', 'black']
basin_ls2 = [i.replace("_", " ") for i in basin_ls]
basins_dict = {z[0]: list(z[1:]) for z in zip(basin_ls2, basin_abr, colors)}

##Make figures
fig, axes = plt.subplots(4, 2, figsize=(25, 30))
pad=5
fig2, axes2 = plt.subplots(1, 2, figsize=(25, 10))
fig2.patch.set_alpha(0)
for count, basin in enumerate(basin_ls):
    #Categorized fragment lengths figure 
    fraglen_df =fla.fraglen_density(basin, years, bin_ls, data_folder)
    for row, l in enumerate(lengths):
        if basin != 'all_basins':
            basin = basin.replace("_", " ")
            area = sum(huc2[huc2['basin']==basin].AreaSqKm)
            axes[row,0].plot(fraglen_df[0].index, fraglen_df[0][str(l)]/area, label = basin, color=basins_dict[basin][1], marker='o', lw=4, ms=15)
            axes[row,1].plot(fraglen_df[1][1:].index, fraglen_df[1][str(l)][1:], label = basin, color=basins_dict[basin][1], marker= 'o', lw=4, ms=15)
       
        else:
            area = sum(huc2.AreaSqKm)
            basin = basin.replace("_", " ")
            axes[row,0].plot(fraglen_df[0].index, fraglen_df[0][str(l)]/area, label = basin, color=basins_dict[basin][1], linestyle='--', marker='o', lw=4, ms=15)
            axes[row,1].plot(fraglen_df[1][1:].index, fraglen_df[1][str(l)][1:], label = basin, color=basins_dict[basin][1], linestyle='--', marker= 'o', lw=4, ms=15)
            basin = basin.replace(" ", "_")
        
        #All dams subplot   
        axes[0,0].set_title("Fragment density\nfor all dams", weight="bold", size=32)
        axes[row,0].set_xticklabels(xlabels)
        axes[row,0].annotate(length_dict[l], xy=(0, 0.5), xytext=(-axes[row,0].yaxis.labelpad - pad, 0),
                xycoords=axes[row,0].yaxis.label, textcoords='offset points',
                size=30, weight='bold', ha='right', va='center', rotation=90)
        axes[row, 0].tick_params(axis = 'both', which = 'major', labelsize = 28, width=2.5, length=5)
        axes[row, 0].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        axes[row, 0].yaxis.get_offset_text().set_fontsize(28)

        #Small dams subplot
        axes[0,1].set_title("Fraction of fragments\nfrom medium dams", weight="bold", size=32)
        axes[row,1].set_ylim(0, 1)
        axes[row,1].set_xticklabels(xlabels[1:])
        axes[row, 1].tick_params(axis = 'both', which = 'major', labelsize = 28, width=2.5, length=5)
    
    #Total fragments figure
    if basin != 'all_basins':
        print(basin)
        basin = basin.replace("_", " ")
        area = sum(huc2[huc2['basin']==basin].AreaSqKm)
        axes2[0].plot(fraglen_df[0].index, fraglen_df[0]["total_frags"]/area, label = basins_dict[basin][0], color=basins_dict[basin][1], marker='o', lw=4, ms=15)
        axes2[1].plot(fraglen_df[1].index[1:], fraglen_df[1]["percent_small"][1:], label = basins_dict[basin][0], color=basins_dict[basin][1], marker='o', lw=4, ms=15)
        basin = basin.replace(" ", "_")
    else:
        basin = basin.replace("_", " ")
        area = sum(huc2.AreaSqKm)
        axes2[0].plot(fraglen_df[0].index, fraglen_df[0]["total_frags"]/area, label = basins_dict[basin][0], color=basins_dict[basin][1], linestyle='--', marker='o', lw=4, ms=15)
        axes2[1].plot(fraglen_df[1].index[1:], fraglen_df[1]["percent_small"][1:], label = basins_dict[basin][0], color=basins_dict[basin][1],linestyle='--', marker='o', lw=4, ms=15)
        basin = basin.replace(" ", "_")
    
    #Figure 2 labelling
    axes2[0].set_ylabel("Total fragment density per km$^2$", weight="bold", size=34)
    axes2[1].set_ylabel("Relative change from medium dams", weight="bold", size=34)
    axes2[0].set_xticklabels(xlabels)
    axes2[1].set_xticklabels(xlabels[1:])
    axes2[0].set_ylim(0, 0.017)
    axes2[1].set_ylim(0, 1)
    axes2[0].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    axes2[0].yaxis.get_offset_text().set_fontsize(32)
 
plt.legend(bbox_to_anchor=(1, 0.99, 0.1, 0), fontsize=32)
axes2[0].tick_params(axis = 'both', which = 'major', labelsize = 32, width=2.5, length=5)
axes2[1].tick_params(axis = 'both', which = 'major', labelsize = 32, width=2.5, length=5)

plt.tight_layout(rect=[0, 0, 0.94, 1])  
fig.savefig(plot_folder+"tot_frags1x2_dens_conus.png", dpi=300)
fig2.savefig(plot_folder+"frag_len_dens_conus.png", dpi=300)
# plt.savefig()


