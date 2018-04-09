# QGIS3 Physiocap3 Plugin
_Physiocap plugin helps analysing raw data from Physiocap in QGIS. The documentations available on github are in French only. 
The plugin and TIPS are available in English and Italian_

La version 3 de l'extension supporte QGIS3 mais n'est pas compatible avec QGIS 2.

L'extension Physiocap pour QGIS permet d'analyser les résultats bruts de Physiocap. Il s'agit de mesures directes de l'expression végétative de la vigne.
Trois métriques sont calculés à partir des données brutes :
* nombre de bois au mètre
* le diamètre moyen et
* l'indice de biomasse (kg de bois par m2)
	
L'extension permet de choisir plusieurs paramètres pour filtrer les données qui ont un intérêt. Elle réalise une série de calculs aboutissant à :
* une synthèse des métriques moyens des données retenues,
* trois shapefiles qui permettent de visualiser les données mesurées, les points sans mesures et les données retenues (après filtration),
* quatres histogrammes qui décrivent la population des données mesurées (sarment, diamètre, segment de points contigües).

Cette version apporte des nouveautés pour l'analyse qualitative des captures (taux de points sans mesure, segment de points cohérents et contigüs, dérive durant l'avancement de la capture, altitude et PDOP données par le GPS).

Dans son module Inter, l'extension réalise une extraction des données filtrés à partir de votre contour de parcelles. Vous obtenez les moyennes Inter parcellaires pour faire un premier diagnostic de chaque entité agronomique.

Cette version permet les interpolations et des calculs d'isolignes Intra parcellaire pour affiner l'analyse agronomique avec la librarie GDAL. Le module INTRA SAGA de V3 est en cours de développement.

*"Physiocap" est déposé par le CIVC.*

L'extension QgisPysiocapPlugin intègre le code de calcul du CIVC (PHYSIOCAP_V8). QgisPysiocapPlugin est donc sous licence Common Creative CC-BY-NC-SA V4. S'appuyant sur QGIS 3 API elle est aussi sous licence GNU/GPL (voir les détails sous https://github.com/jhemmi/Physiocap3/blob/master/LICENSE). Physiocap3 Plugin est un logiciel libre qui cherche :
* à diffuser le traitement de ses données au plus près de l'utilisateur,
* à favoriser l'utilisation de QGIS 3 dans le monde viticole,
* plus généralement à "Valoriser vos données"

La documentation de la version 2 se trouve dans le Wiki
https://github.com/jhemmi/QgisPhysiocapPlugin/wiki/Qgis-Physiocap-Plugin-usage-&-installation
La documentation de la version 3 n'est pas encore disponible.

La version 3.0.8-INTRA-BETA est publiée dans le dépot github. 
La 3.0.3 est déposéé sous QGIS 3 (accessible directement dans QGIS 3 depuis le Menu "Extension").

**Attention, ce dépot GitHub contient la version en cours d'évolution (la 3.0.8 est déposée pour des tests. Elle est encore instable - Mars 2018 https://github.com/jhemmi/Physiocap3/releases) **

**Warning, this GitHub repo contains last evolution version (Version 3.0.8 is for test purpose only and not stable - March 2018 https://github.com/jhemmi/Physiocap3/releases) **
