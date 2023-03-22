
import geopandas as gp, pandas as pd, numpy as np

def frag_diff(results_folder):
    natural_frag = gp.read_file(results_folder+"no_dams/huc8_indices_no_dams.shp")
    natural_frag['LENGTHKM_l'].fillna(0,inplace=True)

    #before 1920 bifurcation
    frag_1920 = gp.read_file(results_folder+"1920/huc8_indices_1920.shp")
    frag_1920.fillna(0.0,inplace=True)
    frag_1920["frag_diff"] = frag_1920["LENGTHKM_l"] -  natural_frag["LENGTHKM_l"]
    cfrag_1920 = frag_1920.copy()  #cumulative fragment difference
    cfrag_1920.fillna(0.0,inplace=True)
    cfrag_1920["frag_cudiff"] = frag_1920["LENGTHKM_l"] -  natural_frag["LENGTHKM_l"]

    #before 1950 bifurcation
    frag_1950 = gp.read_file(results_folder+"1950/huc8_indices_1950.shp")
    frag_1950.fillna(0.0, inplace=True)
    frag_1950["frag_diff"] = frag_1950["LENGTHKM_l"] -  frag_1920["LENGTHKM_l"]
    cfrag_1950 = frag_1950.copy()   #cumulative fragment difference
    cfrag_1950.fillna(0.0,inplace=True)
    cfrag_1950["frag_cudiff"] = (frag_1950["LENGTHKM_l"] -  frag_1920["LENGTHKM_l"])+frag_1920["frag_diff"]

    #before 1980 bifurcation
    frag_1980 = gp.read_file(results_folder+"1980/huc8_indices_1980.shp")
    frag_1980.fillna(0.0,inplace=True)
    frag_1980["frag_diff"] = frag_1980["LENGTHKM_l"] -  frag_1950["LENGTHKM_l"]
    cfrag_1980 = frag_1980.copy()   #cumulative fragment difference
    cfrag_1980.fillna(0.0,inplace=True)
    cfrag_1980["frag_cudiff"] = (frag_1980["LENGTHKM_l"] -  frag_1950["LENGTHKM_l"])+frag_1920["frag_diff"]+frag_1950["frag_diff"]

    #2010 bifurcation
    frag_2012 = gp.read_file(results_folder+"2010/huc8_indices_2010.shp")
    frag_2012.fillna(0.0,inplace=True)
    frag_2012["frag_diff"] = frag_2012["LENGTHKM_l"] -  frag_1980["LENGTHKM_l"]
    cfrag_2012 = frag_2012.copy()   #cumulative fragment difference
    cfrag_2012.fillna(0.0,inplace=True)
    cfrag_2012["frag_cudiff"] = (frag_2012["LENGTHKM_l"] -  frag_1980["LENGTHKM_l"])+frag_1920["frag_diff"]+frag_1950["frag_diff"]+frag_1980["frag_diff"]
    
    #Save files
    natural_frag.to_file(results_folder+"no_dams/huc8_no_dams_frag_diff.shp")
    frag_1920.to_file(results_folder+"1920/huc8_1920_frag_diff.shp")
    frag_1950.to_file(results_folder+"1950/huc8_1950_frag_diff.shp")
    frag_1980.to_file(results_folder+"1980/huc8_1980_frag_diff.shp")
    frag_2012.to_file(results_folder+"2010/huc8_2010_frag_diff.shp")
    print("Save fragment difference shapefiles complete")
    cfrag_1920.to_file(results_folder+"1920/huc8_1920_frag_cudiff.shp")
    cfrag_1950.to_file(results_folder+"1950/huc8_1950_frag_cudiff.shp")
    cfrag_1980.to_file(results_folder+"1980/huc8_1980_frag_cudiff.shp")
    cfrag_2012.to_file(results_folder+"2010/huc8_2010_frag_cudiff.shp")
    print("Save fragment cumulative difference shapefiles complete")

def fraglen_density(basin, years,  bin_ls, data_folder):
    bins = np.clip(bin_ls, bin_ls[0], bin_ls[-1])
    labels = [str(x) for x in bins[1:]]
    labels.append('total_frags')

    all_dams_fraglen = pd.DataFrame(0, index=years, columns=labels)
    all_dams_fraglen_diff = pd.DataFrame(0, index=years, columns=labels)
    big_dams_fraglen = pd.DataFrame(0, index=years, columns=labels)
    big_dams_fraglen_diff = pd.DataFrame(0, index=years, columns=labels)
    small_dams_fraglen = pd.DataFrame(0, index=years, columns=labels)

    for year in years:
        all_dams_frags = pd.read_csv(data_folder+"nabd_data/"+year+"/"+basin+"_fragments.csv")
        big_dams_frags = pd.read_csv(data_folder+"grand_data/"+year+"/"+basin+"_fragments.csv")
        
        all_dams_fraglen_diff.loc[year,"total_frags"]=len(all_dams_frags["LENGTHKM"])
        big_dams_fraglen_diff.loc[year,"total_frags"]=len(big_dams_frags["LENGTHKM"])
        totpercent_big = big_dams_fraglen_diff["total_frags"]/all_dams_fraglen_diff["total_frags"]
        totpercent_small = 1 - totpercent_big
        small_dams_fraglen["percent_small"] = totpercent_small
        
        all_dams_frag_bins = pd.cut(all_dams_frags["LENGTHKM"], bins=bins, labels=labels[:-1])
        big_dams_frag_bins = pd.cut(big_dams_frags["LENGTHKM"], bins=bins, labels=labels[:-1])

        for count, value in enumerate(all_dams_fraglen.columns[:-1]):
            all_dams_fraglen.loc[year,value]=all_dams_frag_bins.value_counts()[count]
            big_dams_fraglen.loc[year,value]=big_dams_frag_bins.value_counts()[count]
            if year != "no_dams":
                all_dams_fraglen_diff.loc[year,value] = all_dams_fraglen.loc[year,value]-all_dams_fraglen.loc["no_dams",value]
                big_dams_fraglen_diff.loc[year,value] = big_dams_fraglen.loc[year,value]-big_dams_fraglen.loc["no_dams",value]
            else:
                all_dams_fraglen_diff.loc[year,value]=0
                big_dams_fraglen_diff.loc[year,value]=0
            percent_big = big_dams_fraglen.loc[year,value]/all_dams_fraglen.loc[year,value]
            small_dams_fraglen.loc[year,value] = 1 - percent_big
    small_dams_fraglen["percent_small"]["no_dams"] = 0

    # all_dams_fraglen_diff.to_csv(results_folder+basin+"_all_dams_frag_diff.csv")
    # small_dams_fraglen.to_csv(results_folder+basin+"_small_dams_fraction_frag.csv")
    return all_dams_fraglen_diff, small_dams_fraglen
    