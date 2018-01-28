# QGIS3 Physiocap3 Plugin
_Physiocap plugin helps analysing raw data from Physiocap in QGIS. The documentations available on github are in French only. 
The plugin and TIPS are available in English_

L'extension Physiocap pour QGIS permet d'analyser les résultats bruts de Physiocap. Il s'agit de mesures directes de la vigueur et de l'expression végétative de la vigne.
Trois métriques sont calculés à partir des données brutes :
* nombre de bois au mètre
* le diamètre moyen et
* l'indice de biomasse (kg de bois par m2)
	
L'extension permet de choisir plusieurs paramètres pour filtrer les données qui ont un intérêt. Elle réalise une série de calculs aboutissant à :
* une synthèse des métriques moyens des données retenues,
* deux shapefiles qui permettent de visualiser les données mesurées et les données retenues (après filtration),
* trois histogrammes qui décrivent la population des données mesurées (sarment et diamètre).

A partir de sa version 1.2.3 Inter, l'extension réalise une extraction des données filtrés à partir de votre contour de parcelles. Vous obtenez les moyennes Inter parcellaires pour faire un premier diagnostic de chaque entité agronomique.

Avec la 1.3.1, l'extension permet des interpolations et des alculs d'isolignes Intra parcellaire pour affiner l'analyse agronomique.

La version 1.3.2 de l'extension apporte la trduction anglaise et une meilleures gestions des messages et exceptions

Avec la version 1.4.0, apparition de TIPS contextuels et amélioration de la version anglaise.

La version 1.7.0 CONSOLIDATION permet de regrouper plusieurs jeux de données pour les traiter ensemble.

La version 1.8.3 apporte une traduction italienne. Elle précise dans le traitement Intra les ecarts type et les médianes. Plus anecdotique, elle permet les saisies d'écartements inter rang et inter pied compatible ave l'hémispère Sud.

*"Physiocap" est déposé par le CIVC.*

L'extension QgisPysiocapPlugin intègre le code de calcul du CIVC (PHYSIOCAP_V8). QgisPysiocapPlugin est donc sous licence Common Creative CC-BY-NC-SA V4. S'appuyant sur QGIS elle est aussi sous licence GNU/GPL (voir les détails sous https://github.com/jhemmi/QgisPhysiocapPlugin/blob/master/LICENSE). QgisPysiocapPlugin est un logiciel libre qui cherche :
* à diffuser le traitement de ses données au plus près de l'utilisateur,
* à favoriser l'utilisation de QGIS dans le monde viticole,
* plus généralement à "Valoriser vos données"

La documentation se trouve dans le Wiki
https://github.com/jhemmi/QgisPhysiocapPlugin/wiki/Qgis-Physiocap-Plugin-usage-&-installation

La 1.8.3 est publiée dans le dépot standard de Qgis et donc accessible directement dans Qgis depuis le Menu "Extension".
- 
**Attention, ce dépot GitHub contient la version en cours d'évolution (la 1.8.3 est version stable - Octobre 2017 https://github.com/jhemmi/QgisPhysiocapPlugin/releases) **

**Warning, this GitHub repo contains last evolution version ( 1.8.3 version is the stable one - October 2017 https://github.com/jhemmi/QgisPhysiocapPlugin/releases) **
