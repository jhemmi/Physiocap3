# QGIS3 Physiocap3 Plugin
_Physiocap plugin helps analysing raw data from Physiocap in QGIS. The documentations available on github are in French only. 
The plugin and TIPS are mainly translated in English and Italian_

La version 3 de l'extension se nomme Physiocap3 et supporte QGIS3 mais ne peut pas tourner sous QGIS 2. Par contre, Physiocap3 permet de conserver des formats de résultats identiques à ceux des versions 1.8.3 de QgisPhysiocapPlugin (compatible avec QGIS 2.14).

L'extension Physiocap pour QGIS permet d'analyser les résultats bruts de Physiocap. Il s'agit de mesures directes de l'expression végétative de la vigne.
Trois métriques sont calculés à partir des données brutes :
* nombre de sarments au mètre
* le diamètre moyen et
* l'indice de biomasse (kg de bois par m2)
	
L'extension permet de choisir plusieurs paramètres pour filtrer les données qui ont un intérêt. Elle réalise une série de calculs aboutissant à :
* une synthèse des métriques moyens des données retenues,
* trois shapefiles qui permettent de visualiser les données mesurées, les points sans mesures et les données retenues (après filtration),
* quatres histogrammes qui décrivent la population des données mesurées (sarment, vitesse et diamètre bruts et diamètre filtré).

Cette version 3 apporte des nouveautés pour l'analyse qualitative des captures (taux de points sans mesure, segment de points cohérents et contigüs, dérive durant l'avancement de la capture, altitude et PDOP données par le GPS).

Dans son module Inter, l'extension réalise une extraction des données filtrés à partir de votre contour de parcelles. Vous obtenez les moyennes Inter parcellaires pour faire un premier diagnostic de chaque entité agronomique.

Cette version permet les interpolations SAGA et GDAL (voir détail dans l'issue 11) et des calculs d'isolignes Intra parcellaire pour affiner l'analyse agronomique. 

*"Physiocap" est déposé par le CIVC.*

L'extension Pysiocap3 intègre le code de calcul du CIVC (PHYSIOCAP_V8). Pysiocap3 est donc sous licence Common Creative CC-BY-NC-SA V4. S'appuyant sur QGIS 3 API elle est aussi sous licence GNU/GPL (voir les détails sous https://github.com/jhemmi/Physiocap3/blob/master/LICENSE). Physiocap3 Plugin est un logiciel libre mais aussi un bien commun qui cherche :
* à diffuser le traitement de ses données au plus près de l'utilisateur,
* à favoriser l'utilisation de QGIS 3 dans le monde viticole,
* plus généralement à "Valoriser vos données"

La documentation de la version 3 se trouve dans le Wiki https://github.com/jhemmi/Physiocap3/wiki. La documentation utilisateur est disponible sous https://drive.google.com/file/d/1l0cjwrqVe4PaROBVw7XpPlOK2Qdos_5X/view.

La version 3.10.4 LTR est déposée sous QGIS 3 (accessible directement dans QGIS 3 depuis le Menu "Extension").

La numérotation de l'extension suit le numéro des versions LTR de QGIS3 (3.4, 3.10).

**Attention, ce dépot GitHub contient la aussi dernière version en cours d'évolution (la 3.16.0 - Fev 2021 https://github.com/jhemmi/Physiocap3/releases) **

**Warning, this GitHub repo contains last evolution version (Version 3.16.0 - february 2021 https://github.com/jhemmi/Physiocap3/releases) **
