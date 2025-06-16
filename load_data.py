import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import scipy.io
import json
import numpy as np
from format_data import *
from utils import *
import pickle
import tqdm

t_pre = 0.3#0.2
t_post = 0.30#0.300
bin_width = 0.02
# Créer les bins de temps"
psth_bins = np.arange(-t_pre, t_post, bin_width)




hs_aone = 0
hs_pmc = 1

session = 'HERCULE_20250605_SESSION_00/'
path = '/auto/data6/eTheremin/HERCULE/'+ session 

features_aone = np.load(path+f'/headstage_{hs_aone}/features_{bin_width}.npy', allow_pickle=True)
data_aone = np.load(path +f'/headstage_{hs_aone}/data_{bin_width}.npy', allow_pickle=True)

features_pmc = np.load(path+f'/headstage_{hs_pmc}/features_{bin_width}.npy', allow_pickle=True)
data_pmc = np.load(path +f'/headstage_{hs_pmc}//data_{bin_width}.npy', allow_pickle=True)

unique_tones = np.load(path+f'/headstage_{hs_aone}/unique_tones.npy', allow_pickle=True)


gc_aone = np.load(path+f'/headstage_{hs_aone}/good_clusters.npy', allow_pickle=True)
gc_pmc = np.arange(0,31)


if len(features_aone) >= len(features_pmc):
    features = features_aone
else:
    features = features_pmc

# pour récupérer les psth alignés sur les changements de fréquence : 

tracking_pmc = get_psth(data_pmc, features, t_pre, t_post, bin_width, gc_pmc, 'tracking')
playback_pmc = get_psth(data_pmc, features, t_pre, t_post, bin_width, gc_pmc, 'playback')

tracking_aone = get_psth(data_aone, features, t_pre, t_post, bin_width, gc_aone, 'tracking')
playback_aone = get_psth(data_aone, features, t_pre, t_post, bin_width, gc_aone, 'playback')

# pour récupérer les psth alignés sur les mock changements de fréquence (donc un uniquement en playback, c'est un changement de fréquence qui n'a pas eu lieu acoustiquement mais qui aurait dû avoir eu lieu si on couplait encore le mouvement à au son)
playback_mock_pmc = get_mock_psth(data_pmc, features, t_pre, t_post, bin_width, gc_pmc, 'playback')
playback_mock_aone = get_mock_psth(data_aone, features, t_pre, t_post, bin_width, gc_aone, 'playback')


