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

L'extension Physiocap3 intègre le code de calcul du CIVC (PHYSIOCAP_V8 datant de 2015). Pysiocap3 est donc sous licence Common Creative CC-BY-NC-SA V4. S'appuyant sur QGIS 3 API elle est aussi sous licence GNU/GPL (voir les détails sous https://github.com/jhemmi/Physiocap3/blob/master/LICENSE). Physiocap3 Plugin est un logiciel libre mais aussi un bien commun qui cherche :
* à diffuser le traitement de ses données au plus près de l'utilisateur,
* à favoriser l'utilisation de QGIS 3 dans le monde viticole,
* plus généralement à "Valoriser vos données"

La documentation de la version 3 se trouve dans le Wiki https://github.com/jhemmi/Physiocap3/wiki. La documentation utilisateur est disponible sous https://drive.google.com/file/d/1l0cjwrqVe4PaROBVw7XpPlOK2Qdos_5X/view.

La version 3.16.15 LTR est déposée sous QGIS 3 (accessible directement dans QGIS 3 depuis le Menu "Extension").

La version 3.34.1 LTR sera déposée sous QGIS 3 pour 3.28.11 LTR et 3.34.1 future LTR (accessible directement dans QGIS 3 depuis le Menu "Extension").

La numérotation de l'extension suit le numéro des versions LTR de QGIS3 (3.22, 3.28, 3.34 ...).
La sous version x est la version QGIS pour laquelle les tests ont été effectués.

**Attention, ce dépot GitHub contient la aussi dernière version en cours de test (la 3.34.x - décembre 2022 https://github.com/jhemmi/Physiocap3/releases) **

**Warning, this GitHub repo contains last evolution version (Version 3.34.x - december 2023 https://github.com/jhemmi/Physiocap3/releases) ** 
