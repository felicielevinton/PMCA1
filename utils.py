import numpy as np
from scipy.signal import find_peaks
import os
import json

from scipy.signal import butter, filtfilt



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






def get_mock_psth(data, features, t_pre, t_post, bin_width, good_clusters, condition):
    """
    Pour voir, pour chaque neurone, les psth alignés sur les mocks triggers !
    
    input: 
      -data, features, good_clustersn condition ("tracking" or "playback")
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
                if features[bin]['Mock_change']>0 and features[bin]['Condition']==c :
                    psth_clus.append(data[cluster][bin-int(t_pre/bin_width):bin+int(t_post/bin_width)])
        psth.append(psth_clus)
    return psth




def get_played_frequency(features, t_pre, t_post, bin_width, condition):
    """"
    Fonction pour récupérer la fréquence jouée pour chaque psth défini dans get_psth
    """
    if condition=="tracking":
        c = 0
    elif condition=="playback":
        c=1
    elif condition=="tail":
        c = -1
    elif condition == "mappingchange":
        c = 2
    frequency = []
    for bin in range(len(features)):
        if bin-int(t_pre/bin_width)>0 and bin+int(t_post/bin_width)<len(features):
            if features[bin]['Frequency_changes']>0 and features[bin]['Condition']==c :
                frequency.append(features[bin]['Played_frequency'])
    return frequency




def get_sustained_activity_nan(psth, t_pre, t_post, bin_width):
    """""
    Fonction qui renvoie l'activité moyenne d'un seul psth
    input : un tableau contenant des PSTH
    output : sustained activity pour chaque PSTH
    
    --> dans la cas où on aurait des nan gênants
    
    
    """
    if psth is not np.nan and psth is not None:
    
        return (np.nanmean(psth[0: int(t_pre/bin_width)-5]))
    else:
        return np.nan




def mean_maxima_nan(arr, thresh, t0, t1):
    """
    Renvoie la moyenne des deux points max d'un tableau cont les indices sont compris
    entre t0 et t1
    
    --> cas où on aurait des nan gênants
    """
    # Find peaks in the array
    if arr is not np.nan:
        pics, _ = find_peaks(arr, distance=thresh)

        # Check if there are at least two peaks
        if len(pics) >= 2:
            # Get the indices of the two maximum values
            max_indices = np.argsort(arr[pics])[-2:]

            # Calculate the mean of the two maximum values
            #mean = np.mean(arr[pics][max_indices])
            mean = np.max(arr[pics][max_indices])
            # Get the actual maximum values
            max_values = arr[pics][max_indices]
        else:
            mean = np.nan
            max_values = np.nan
    else:
        mean = np.nan
        max_values = np.nan
        pics=np.nan
        

    return mean, pics, max_values




def get_total_evoked_response(psth, t_pre, t_post, bin_width, thresh, t0, t1):
    """"
    Function qui renvoie la total evoked reponse pour un tableau contenant des psth
    input : un tableau psth contenant des psth
    output : un tableau contenant la total evoked response pour chaque psth
    
    """
    total_evoked_response = []
    for elt in psth:
        total_evoked_response.append(mean_maxima(elt, thresh, t0,t1)[0])
        #total_evoked_response.append(np.max(elt))
    return total_evoked_response







def get_total_evoked_response_individual(psth, t_pre, t_post, bin_width, thresh, t0, t1):
    """"
    Function qui renvoie la total evoked reponse pour un psth individuel
    input : un tableau psth contenant des psth
    output : un tableau contenant la total evoked response pour chaque psth
    
    """
    if psth is not np.nan:
        return mean_maxima(psth, thresh, t0,t1)[0]
    else : 
        return np.nan




def get_sem(neurones):
    """""
    Fonction qui renvoie la sem pour un tableau de format (neurones x bin)
    
    input : un tableau [neurones, bins]
    output: liste [bins] contenant la SEM
    """
    sem = []
    for bin in range(len(neurones[0])):
        sem.append(np.nanstd(np.array(neurones)[:,bin])/np.sqrt(len(neurones)))
    return sem  








def get_plot_coords(channel_number):
    """
    Fonction qui calcule la position en 2D d'un canal sur une Microprobe.
    Retourne la ligne et la colonne.
    """
    if channel_number in list(range(8)):
        row = 3
        col = channel_number % 8

    elif channel_number in list(range(8, 16)):
        row = 1
        col = 7 - channel_number % 8

    elif channel_number in list(range(16, 24)):
        row = 0
        col = 7 - channel_number % 8

    else:
        row = 2
        col = channel_number % 8

    return row, col


def get_better_plot_geometry(good_clusters):
    # Calculate number of rows and columns for subplots
    num_plots = len(good_clusters)
    num_cols = int(np.ceil(np.sqrt(num_plots)))
    num_rows = int(np.ceil(num_plots / num_cols))
    return num_plots, num_rows, num_cols







# Positions functions :



def find_movement(all_pos, integWin = 15,pauseBeforeMovement = 100,  threshold = 2, sweepRefractoryPeriod = 300,preSweepPeriod = 150 ):
    """
    une fonction appelée dans get_positions pour obtenir la vitesse
    Sert aussi pour essayer de détecter des onsets de grands mouvements
    """
    # Calcul des différences
    datadiff = np.diff(all_pos)
    changeIdx = np.where(datadiff != 0)[0]

    # Intégration sur les changements précédents
    integPos = np.zeros(len(all_pos))
    for changeNum in range(integWin, len(changeIdx)):
        idx = changeIdx[changeNum]
        window = changeIdx[changeNum - integWin : changeNum + 1]
        integPos[idx] = np.sum(datadiff[window - 1])  # -1 car datadiff est plus court que data

    # Détection des pics dépassant le seuil
    threshIdx = []
    for signC in [-1, 1]:
        integPos_T = signC * integPos
        threshIdx_T = np.where(integPos_T > threshold)[0].astype(float)  # permet les NaN

        # Vérification de pic local
        for i in range(len(threshIdx_T)):
            idx = int(threshIdx_T[i])
            start = int(max(0, idx - sweepRefractoryPeriod))
            end = int(min(len(integPos_T), idx + sweepRefractoryPeriod + 1))
            if np.any(integPos_T[start:end] > integPos_T[idx]):
                threshIdx_T[i] = np.nan

        threshIdx.extend(threshIdx_T)

    # Nettoyage des indices
    threshIdx = np.array(threshIdx)
    threshIdx = threshIdx[~np.isnan(threshIdx)].astype(int)
    threshIdx = np.sort(threshIdx)

    # Détection des débuts de mouvement
    onsetIdx = []
    for threshNum in range(1, len(threshIdx)):
        peakIdx = threshIdx[threshNum]
        cursorBackInTime = peakIdx
        while cursorBackInTime > threshIdx[threshNum - 1]:
            start = max(0, cursorBackInTime - preSweepPeriod)
            if np.all(all_pos[start:cursorBackInTime + 1] == all_pos[cursorBackInTime]):
                onsetIdx.append((cursorBackInTime, peakIdx))
                break
            cursorBackInTime -= 1
    return integPos, onsetIdx




def get_positions(features, unique_tones):
    """
    input : dictionnaire features, le fichier unique_tones.npy de la session
    output : 
         - vecteur avec les positions en x pour chaque bin
          - vecteur avec la vitesse à chaque bin
    
    """
    pixels = np.linspace(0, 28, len(unique_tones))        # 28 cm
    freq_to_pixel = {tone: pixel for tone, pixel in zip(unique_tones, pixels)}
    
        
    frequency = []
    for bin in features:
        if bin['Condition']==0 or bin['Condition']==0:
            frequency.append(bin['Played_frequency'])
        else:
            frequency.append(bin['Mock_frequency'])


    pos = np.array([freq_to_pixel.get(f, np.nan) for f in frequency])
    integ_pos, onset_idx = find_movement(pos, integWin = 15,pauseBeforeMovement = 100,  threshold = 1.5, sweepRefractoryPeriod = 300,preSweepPeriod = 150 )
    return pos, integ_pos

