



def get_psth(data, features, t_pre, t_post, bin_width, good_clusters, condition):
    """
    Pour voir, pour chaque neurone, les psth
    
    input: 
      -data, features, good_clustersn condition ("tracking" or "playback)
    output : 
     - une liste contenant le psth moyen par cluster pour chaque changement de fréquence en playback [neurones x chgt de freq x [t_pre, t_post] ]
    """
    if condition=="tracking":
        c = 0
    elif condition == "playback" : 
        c=1
    elif condition== "tail":
        c = -1
    elif condition =="mapping change":
        c = 2
    
    
    psth=[] 
    for cluster in good_clusters:
        psth_clus = []
        for bin in range(len(features)):
            #print(diff)
            if bin-int(t_pre/bin_width)>0 and bin+int(t_post/bin_width)<len(features):
                if features[bin]['Frequency_changes']>0 and features[bin]['Condition']==c :
                    psth_clus.append(data[cluster][bin-int(t_pre/bin_width):bin+int(t_post/bin_width)])
        psth.append(psth_clus)
    return psth
