# PMCA1
Les données sur les sessions sont ici : https://docs.google.com/spreadsheets/d/1sFatSTXO0j3OONKstz7YN-mM04kNMjk_r7zo951yicU/edit?gid=871786168#gid=871786168
Il y a les infos sur le nom de la session, le type de session 'type', si elle est utilisable ou non ('use') et des commentaires. 


Données neurales : 
 - fichier data_005.npy :  
0.005 : taille des bins
Ce fichier est de taille n_neurons x n_bins. Il comporte toujours les 32 canaux.

Features expérimentales: 
 - features_0.005.npy
0.005 : taille des bins
C'est un dictionnaire de taille n_bins. A chaque bin, il contient les informations suivantes:
  - Played_frequency : la fréquence jouée (et entendue par le furet)
  - Condition : (-1 pour warmup, 0 pour tracking et 1 pour playback)
  - Block : le numéro du block
  - Frequency_changes : contient True s'il y a eu un changement de fréquence dans ce bin, sinon False
  - Mock_frequency : la fréquence qui auarit dû être jouée dans la condition playback (en tracking c'est 0 sinon - mais pas un vrai 0, c'est juste que ca n'existe pas)
  - Mock_change : contient True s'il y a eu un changement de mock fréquence dans ce bin, sinon False


good_clusters.npy contient les numéros des channels dans data qui ont passé le test statistique: donc ce sont ces channels qu'on garde pour les analyses. 

