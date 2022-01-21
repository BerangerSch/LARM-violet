# LAUNCH FILES:


## makeMap.launch :
-Le launch file makeMap.launch sert a creer le fichier .Yaml ( enregistrement de map ) pour l'ituliser par AMCL et move_base on , ces deux fichier sont dans le dossier map.

## Challenge3-simulation.launch:

-C'est le launch file de la navigation autonome de notre robot en simulation  quand on place un 2D goal dans r-viz en exploitant le AMCL , move_base et map_server et le .Yaml de map enregistree ( 1er etage )

#  Challenge3-tbot.launch:

-C'est notre launch file principale qui lance notre robot Kuboki , Laser , et la camera Realsense2 aussi nos deux scripts vision.py et marker.py , finalement , la node de gmapping et le move_base
