# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Physiocap_var_exception
                                 A QGIS 3 plugin

 Le module Exception contient les variables et les définitions des exceptions
                             -------------------
        begin                : 2015-11-04
        git sha              : $Format:%H$
        email                : jean@jhemmi.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 * Physiocap plugin créé par jhemmi.eu et CIVC est issu de :               *
 *- PSPY : PHYSIOCAP SCRIPT PYTHON VERSION 8.0 10/11/2014                  *
 *   CREE PAR LE POLE TECHNIQUE ET ENVIRONNEMENT DU CIVC                   *
 *   MODIFIE PAR LE CIVC ET L'EQUIPE VIGNOBLE DE MOËT & CHANDON            *
 *   AUTEUR : SEBASTIEN DEBUISSON, MODIFIE PAR ANNE BELOT ET MANON MORLET  *
 *   Physiocap plugin comme PSPY sont mis à disposition selon les termes   *
 *   de la licence Creative Commons                                        *
 *   CC-BY-NC-SA http://creativecommons.org/licenses/by-nc-sa/4.0/         *
 *- Plugin builder et QGIS 3 API et à ce titre porte aussi la licence GNU    *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *   http://www.gnu.org/licenses/gpl-2.0.html                              *
 *                                                                         *
***************************************************************************/
"""
import os 
import platform

# ###########################
# VARIABLES GLOBALES DE PHYSIOCAP
# ###########################

# Ces variables sont nommées en Francais par compatibilité avec la version physiocap_V8
# Pour reconnaitre si Windows ou Linux
MACHINE = platform.system()
if MACHINE == "Linux":
    LE_MODE_PROD = "NO"
else:
    LE_MODE_PROD = "YES"
print( 'Mode production vaut ' + LE_MODE_PROD)
LISTE_PROFIL= [ 'Standard', 'Champagne', 'Fronton', 'IFV Bordeaux']
    
# LIVRAISON : supprimer en Prod
#LE_MODE_PROD = "NO"

# En prod CENTROIDES vaut NO
CENTROIDES = "NO"  # CENTROIDES YES est pour voir les centroides dans la synthese
# Listes de valeurs pour la trace
TRACE_TOUT = "Traces complètes"
TRACE_MINI = "Traces minimales"
TRACE_PAS  = "Pas de trace"
MODE_TRACE = [ TRACE_TOUT,  TRACE_MINI, TRACE_PAS]
MODE_PHY_ID = [ "ID_PHY vaut PHY_numérique",  "ID_PHY contient un texte sans blanc, sans cote"]
TRACE_INTRA  = "Intra"
TRACE_TOOLS  = "Tools"
TRACE_MIN_MAX  = "Min-Max-Iso"
TRACE_SEGMENT  = "Segment"
TRACE_SEGMENT_DECOUPES  = "Découpe"
TRACE_PG  = "POSTGRES"

REPERTOIRE_DONNEES_BRUTES = "Choisissez votre chemin"
PHYSIOCAP_NOM = "Physiocap"
PHYSIOCAP_NOM_3 = "Physiocap3"
PHYSIOCAP_UNI = u"\u03D5"
PHYSIOCAP_WARNING = u"\u26A0"
PHYSIOCAP_INFO = u"\U0001F6C8"
PHYSIOCAP_STOP = u"\U0001F6AB"
PHYSIOCAP_2_ETOILES = "**"
PHYSIOCAP_2_EGALS = "=="
PHYSIOCAP_LOG_ERREUR = PHYSIOCAP_WARNING + " " + PHYSIOCAP_UNI + " Erreurs"

# Test de robustesse de la gestion des unicodes
PHYSIOCAP_TEST1 = "ȧƈƈḗƞŧḗḓ ŧḗẋŧ ƒǿř ŧḗşŧīƞɠ"
PHYSIOCAP_TEST2 = "ℛℯα∂α♭ℓℯ ♭ʊ☂ η☺т Ѧ$☾ℐℐ"

POSTGRES_NOM = "postgres"
CSVT_NOM = "CSV avec WKT"
CSVT_DRIVER = "CSVT"
GEOJSON_NOM = "GeoJSON"
GEOJSON_DRIVER = "GeoJSON"  # mes choix  RFC7946=YES  WRITE_BBOX=YES  « GeoJSON - Newline Delimited »  defaut COORDINATE_PRECISION=15
"""
 Quand vous exportez des couches vers GeoJSON, vous sont proposées des Options de couche spécifiques. Ces options proviennent de GDAL 
 qui est responsable de l’écriture du fichier:

    COORDINATE_PRECISION le nombre maximum de chiffres après le séparateur décimal pour écrire en coordonnées. 
    La valeur par défaut est 15 (remarque: pour les coordonnées de Lat Lon, 6 est considéré comme suffisant). Une troncature se produira pour supprimer les zéros de fin.

    RFC7946 par défaut GeoJSON 2008 sera utilisé. S’il est défini sur OUI, la norme RFC 7946 mise à jour sera utilisée. 
    La valeur par défaut est NO (donc GeoJSON 2008). Voir https://gdal.org/drivers/vector/geojson.html#rfc-7946-write-support 
    pour les principales différences, en bref : seul EPSG: 4326 est autorisé, les autres SCR seront transformés, 
    les polygones seront écrits comme pour suivre la règle de droite pour l’orientation, 
    les valeurs d’un tableau « bbox » sont [ouest, sud, est, nord], pas [minx, miny, maxx, maxy]. 
    Certains noms d’extension sont interdits dans les objets FeatureCollection, Feature et Geometry, la précision des coordonnées par défaut
    est de 7 chiffres décimaux

    WRITE_BBOX défini sur YES pour inclure la boîte englobante des géométries au niveau de l’entité et de la collection d’entités

Outre GeoJSON, il existe également une option d’exportation vers « GeoJSON - Newline Delimited » (voir https://gdal.org/drv_geojsonseq.html). Au lieu d’une FeatureCollection avec des entites, vous pouvez diffuser un type (probablement uniquement des entites) séparés séquentiellement avec des retours à la ligne.

GeoJSON - Newline Delimited propose également des options de couche spécifiques:

    COORDINATE_PRECISION voir ci-dessus (comme pour GeoJSON)

    RS s’il faut commencer les enregistrements avec le caractère RS = 0x1E. La différence réside dans la façon dont les entités sont séparées: 
    uniquement par un caractère de nouvelle ligne (LF) (JSON délimité par une nouvelle ligne, geojsonl) ou 
    en ajoutant également un caractère séparateur d’enregistrement (RS) (donnant des séquences de texte GeoJSON, geojsons). 
    Par défaut à NO. Les fichiers reçoivent l’extension .json si l’extension n’est pas fournie.
"""
GEOPACKAGE_NOM = "GéoPackage"
GEOPACKAGE_DRIVER = "GPKG"
SHAPEFILE_NOM = "ESRI Shapefile"
SHAPEFILE_DRIVER = "ESRI Shapefile"

SEPARATEUR_ ="_"
NOM_PROJET = "PHY" + SEPARATEUR_ # + PHYSIOCAP_TEST4 + SEPARATEUR_

FORMAT_VECTEUR = [ SHAPEFILE_NOM] #,  POSTGRES_NOM] # "memory"]
#TODO: prod à trancher
if MACHINE == "Linux":
    FORMAT_VECTEUR_V3 = [ SHAPEFILE_NOM,  CSVT_NOM, GEOJSON_NOM, GEOPACKAGE_NOM] #,  "memory"] # POSTGRES_NOM] 
else:
    FORMAT_VECTEUR_V3 = [ SHAPEFILE_NOM, GEOPACKAGE_NOM] #,  "memory"] # POSTGRES_NOM] 
    
# Répertoires des sources et de concaténation en fichiers texte
FICHIER_RESULTAT = "resultat.txt"
REPERTOIRE_SOURCES = "fichiers_sources"
REPERTOIRE_SOURCE_V3 = "Copie_MID"
SUFFIXE_BRUT_CSV = SEPARATEUR_ + "RAW.csv"
EXTENSION_MID = "*.MID"
NB_VIRGULES = 58

EXTENSION_CSV = ".csv"
EXTENSION_CSVT = ".csvt"
EXTENSION_GEOJSON = ".geojson"
EXTENSION_SHP = ".shp"
EXTENSION_PRJ = ".prj"
EXTENSION_GPKG= ".gpkg"
SEPARATEUR_GPKG= "|layername="

REPERTOIRE_TEXTES = "fichiers_texte"
REPERTOIRE_TEXTES_V3 = "csv"
# Pour aide gpkg & histo
REPERTOIRE_HELP = os.path.join( os.path.dirname(__file__),"help")
REPERTOIRE_MODELE_GPKG = os.path.join( os.path.dirname(__file__),"modeleGPKG")
MODELE_CONTOUR_NOM = "contour" 
MODELE_CONTOUR_GPKG = MODELE_CONTOUR_NOM + EXTENSION_GPKG
#MODELE_POINT_SHAPE = "point" + EXTENSION_SHP
#MODELE_POINT_GPKG="point"+EXTENSION_GPKG
#MODELE_SEGMENT_GPKG="segment"+EXTENSION_GPKG

FICHIER_HISTO_NON_CALCULE = os.path.join( REPERTOIRE_HELP, 
    "Histo_non_calcule.png")
SUFFIXE_HISTO = ".png"
REPERTOIRE_HISTOS = "histogrammes"
REPERTOIRE_HISTO_V3 = "Histogramme"
FICHIER_HISTO_SARMENT = "histogramme_SARMENT_RAW" + SUFFIXE_HISTO
FICHIER_HISTO_DIAMETRE = "histogramme_DIAMETRE_RAW"  + SUFFIXE_HISTO
FICHIER_HISTO_VITESSE= "histogramme_VITESSE_RAW"  + SUFFIXE_HISTO
FICHIER_HISTO_DIAMETRE_FILTRE = "histogramme_DIAM_FILTERED" +  SUFFIXE_HISTO

REPERTOIRE_SHAPEFILE = "shapefile"

# TODO : à Vérifier Pas d'affichage des VRT Pas de creation de png sous Linux
#if MACHINE == "Linux":
#    EXTENSION_RASTER_SANS_POINT = "png"
#else:
EXTENSION_RASTER_SANS_POINT = "tiff"
EXTENSION_RASTER = "." + EXTENSION_RASTER_SANS_POINT
EXTENSION_RASTER_SAGA_SANS_POINT = "sdat"
EXTENSION_RASTER_SAGA = "." + EXTENSION_RASTER_SAGA_SANS_POINT

EXTENSION_QML = ".qml"

EXTENSION_AVEC_ZERO_V2 = SEPARATEUR_ + "0"
# Nom plus explicite pour V3
EXTENSION_SANS_ZERO= SEPARATEUR_ + "SANS_0"
EXTENSION_AVEC_ZERO = SEPARATEUR_ + "AVEC_0"
EXTENSION_ZERO_SEUL = SEPARATEUR_ + "0_SEUL"

# SRC trouve dans EPSG
PROJECTION_L93 = "L93"
PROJECTION_GPS = "GPS"
PROJECTION_CC45 = "L93-CC45"

EPSG_NUMBER_L93 = 2154
EPSG_NUMBER_GPS = 4326
EPSG_NUMBER_CC45 = 3945
EPSG_TEXT_L93 = "EPSG:"+str(EPSG_NUMBER_L93)
EPSG_TEXT_GPS = "EPSG:"+str(EPSG_NUMBER_GPS)
EPSG_TEXT_CC45 = "EPSG:"+str(EPSG_NUMBER_CC45)
SPHEROID_L93 = "GRS80" #"GRS_1980"
SPHEROID_GPS = "WGS84" # "WGS_1984"
SPHEROID_CC45 = "GRS80" 
LISTE_EPSG=[      EPSG_NUMBER_L93, EPSG_NUMBER_GPS, EPSG_NUMBER_CC45]
LISTE_PROJECTION=[PROJECTION_L93,  PROJECTION_GPS,  PROJECTION_CC45]

# FICHIER .prj
EPSG_DESCRIPTION_L93 = 'PROJCS["RGF93 / Lambert-93", \
GEOGCS["RGF93",DATUM["D_RGF_1993", \
SPHEROID["GRS_1980",6378137,298.257222101]], \
PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]], \
PROJECTION["Lambert_Conformal_Conic"], \
PARAMETER["standard_parallel_1",49], \
PARAMETER["standard_parallel_2",44], \
PARAMETER["latitude_of_origin",46.5], \
PARAMETER["central_meridian",3], \
PARAMETER["false_easting",700000], \
PARAMETER["false_northing",6600000],UNIT["Meter",1]]'

EPSG_DESCRIPTION_GPS =  'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984", \
SPHEROID["WGS_1984",6378137,298.257223563]], \
PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'

EPSG_DESCRIPTION_CC45 = 'PROJCS["RGF93 / CC45", \
GEOGCS["RGF93",DATUM["D_RGF_1993", \
SPHEROID["GRS_1980",6378137,298.257222101]], \
PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]], \
PROJECTION["Lambert_Conformal_Conic"], \
PARAMETER["standard_parallel_1",44.25], \
PARAMETER["standard_parallel_2",45.75], \
PARAMETER["latitude_of_origin",45], \
PARAMETER["central_meridian",3], \
PARAMETER["false_easting",1700000], \
PARAMETER["false_northing",4200000],UNIT["Meter",1]]'

# CHAMP pour nommer les entités 
CHAMP_NOM_PHY = "NOM_PHY"
CHAMP_NOM_ID = "ID_PHY"
# KO sous windows NOM_CHAMP_ID = PHYSIOCAP_UNI + "_ID"
NOM_CHAMP_ID = "PHY_ID"

# Champ des INFO DES SEGMENT FILTRE
DATE_DEBUT = "Date debut"
DATE_FIN = "Date fin"
NUM_SEG = "Numéro segment"
NOMBRE = "Longueur segment"
DERIVE = "Derive moyenne"
PDOP = "Pdop moyen"
GID_TROU = "Points manquants vs précedent"
GID_GARDE = "Points gardés"
GID_SANS_MESURE = "Points du segment sans mesure"

# Inter PARCELLAIRE
#SHAPE_CONTOURS = '/home/jhemmi/Documents/GIS/SCRIPT/QGIS/PhysiocapAnalyseur/data Cap/Contour.shp'
SEPARATEUR_NOEUD = "~~"
NOM_MOYENNE = SEPARATEUR_ + "MOYENNE" + SEPARATEUR_
VIGNETTES_INTER = "INTER_PARCELLAIRE"
REPERTOIRE_INTER_V3 = "Inter_Parcellaire"
#REPERTOIRE_POINTS_V3 = "Point"
REPERTOIRE_SEGMENT_V3 = "Segment"
NOM_POINTS = SEPARATEUR_ + "POINTS"
NOM_SEGMENTS = SEPARATEUR_ + "SEGMENTS"
NOM_SEGMENTS_SUITE_DETAILS = SEPARATEUR_ + "BRISES"
NOM_INTER = SEPARATEUR_ + "INTER"

CONSOLIDATION = "CONSOLIDATION"

# Intra PARCELLAIRE
if MACHINE == "Linux":
    MON_TEMP="/tmp"
else:
    # MON_TEMP="C:\\Utilisateurs\\Utilisateur\\AppData\\Local\\Temp"
    MON_TEMP="C:/Users/Utilisateurs/AppData/Local/Temp"
    
VIGNETTES_INTRA = "INTRA_PARCELLAIRE"
REPERTOIRE_INTRA_V3 = "Interpolation"
NOM_INTRA = SEPARATEUR_ + "INTRA"
REPERTOIRE_RASTERS = "INTRA_PARCELLAIRE"
REPERTOIRE_RASTER_V3 = "Raster"
REPERTOIRE_ISO_V3 = "Isoligne"
ATTR_CONTINUE = ["Arrêt si une interpolation existe", \
    "Ne pas re-créer si une interpolation existe dejà"] #, \
  #  "Nouveau groupe d'interpolation"]    # Ceci evite les creations de [1] au niveaux des rasters ou iso
ATTRIBUTS_INTRA = ["DIAM", "NBSARM", "BIOM"]
# Interpolation étendue aux nouveaux attributs de V3
ATTRIBUTS_V3_INTRA = ["VITESSE", "ALTITUDE", "PDOP", "DISTANCE", "NBSART"]
ATTRIBUTS_INTRA_DETAILS = ["NBSARMM2", "NBSARCEP","BIOMM2", "BIOMGM2", "BIOMGCEP"]
# si QGIS & version 3 verifier que ces index n'ont pas bougé avec les nouveau attributs 
# ATTRIBUTS_INTRA_INDEX = {"DIAM" : 4 ,"NBSARM" : 3 ,"BIOM" : 5,  "NBSARMM2":6, "NBSARCEP":7,"BIOMM2":8, "BIOMGM2":9, "BIOMGCEP":10}
CHEMIN_TEMPLATES = [ "modeleQgis/Physiocap3", "project_templates/Physiocap3"]

# Exceptions Physiocap à partir de 30 erreurs sur un fchier mid
TAUX_LIGNES_ERREUR= 30

CEPAGES = [ 'Inconnu', 'Airen', 'Alicante', 'Aligote', \
'Barbera', 'Blaufrankisch', 'Bobal', \
'Cabernet Franc', 'Cabernet Sauvignon', 'Castelao', 'Catarratto', 'Cayetana', 'Chardonnay', \
'Chasselas', 'Chenin', 'Cinsaut', 'Colombard', 'Concord', 'Cot', 'Criolla Grande', \
'Douce Noire', 'Doukkali', 'Fernao Pires', 'Feteasca', \
'Gamay', 'Garganega', 'Grasevina', 'Grenache', 'Gruner Veltliner', 'Isabella', \
'Listan Prieto', 'Macabeo', 'Mazuelo', 'Melon', 'Mencia', 'Merlot', 'Monastrell', \
'Montepulciano', 'Muscat', 'Muëller Thurgau', \
'Negroamaro', 'Niagara', 'Négrette', \
'Palomino Fino', 'Pamid', 'Pedro Gimenez', 'Pinot Blanc', 'Pinot Meunier', 'Pinot Noir', \
'Prokupac', 'Riesling', 'Rkatsiteli', \
'Sangiovese', 'Sauvignon', 'Semillon', 'Sultaniye', 'Syrah', \
'Tempranillo', 'Trebbiano', 'Trebbiano Romagnolo', 'Tribidrag', 'Zinfandel']

TAILLES = [ "Inconnue", "Chablis", "Cordon de Royat", "Cordon libre", "Guyot simple", "Guyot double"]

# TODO: vérifier liste Spécifique du profil Fronton
COMMUNES_FRONTON=["Fronton", "Villaudric", "Vacquiers", "Villematier", "Castelnau d'estrétefond", "Pompignan","Grisolles", "Campsas", \
    "Labastide", "Nohic", "Orgueuil"]
    
# TODO trier unique dans CRUS et REGIONS_CHAMPAGNE
# Spécifique du profil Champagne
# TODO sauver en V3
CHEMIN_TEMPLATES_CIVC="modeleQgis/CIVC_V2"
#CRUs et régions dans le groupebox informations agronomiques ___Nadia___
CRUS=["AILLEVILLE","ALLEMANT","AMBONNAY","ARCIS-LE-PONSART","ARCONVILLE","ARGANCON", \
"ARRENTIERES","ARSONVAL","AUBILLY","AVENAY-VAL-D'OR","AVIREY-LINGEY","AVIZE","AY","AZY-SUR-MARNE", \
"BAGNEUX-LA-FOSSE","BALNOT-SUR-LAIGNES","BAR-SUR-AUBE","BAR-SUR-SEINE","BARBONNE-FAYEL","BAROVILLE", \
"BARZY-SUR-MARNE","BASLIEUX-SOUS-CHATILLON","BASSU","BASSUET","BAULNE-EN-BRIE","BAYE","BEAUMONT-SUR-VESLE", \
"BEAUNAY","BELVAL-SOUS-CHATILLON","BERGERES","BERGERES-LES-VERTUS","BERGERES-SOUS-MONTMIRAIL","BERRU", \
"BERTIGNOLLES","BETHON","BEZANNES","BEZU-LE-GUERY","BILLY-LE-GRAND","BINSON-ET-ORQUIGNY","BISSEUIL", \
"BLESMES","BLIGNY","BLIGNY","BONNEIL","BOUILLY","BOULEUSE","BOURSAULT","BOUZY","BRAGELOGNE-BEAUVOIR", \
"BRANSCOURT","BRASLES","BRIMONT","BROUILLET","BROUSSY-LE-GRAND","BROYES","BRUGNY-VAUDANCOURT","BUXEUIL", \
"BUXIERES-SUR-ARCE","CAUROY-LES-HERMONVILLE","CELLES-LES-CONDE","CELLES-SUR-OURCE","CERNAY-LES-REIMS", \
"CHACENAY","CHALONS-SUR-VESLE","CHAMBRECY","CHAMERY","CHAMPIGNOL-LEZ-MONDEVILLE","CHAMPILLON", \
"CHAMPLAT-ET-BOUJACOURT","CHAMPVOISY","CHANGY","CHANNES","CHANTEMERLE","CHARLY-SUR-MARNE","CHARTEVES", \
"CHATEAU-THIERRY","CHATILLON-SUR-MARNE","CHAUMUZY","CHAVOT-COURCOURT","CHENAY","CHERVEY","CHEZY-SUR-MARNE", \
"CHIERRY","CHIGNY-LES-ROSES","CHOUILLY","CITRY","COIZARD-JOCHES","COLOMBE-LA-FOSSE","COLOMBE-LE-SEC", \
"COLOMBEY-LES-DEUX-EGLISES","CONGY","CONNIGIS","CORMICY","CORMONTREUIL","CORMOYEUX","COULOMMES-LA-MONTAGNE", \
"COURCELLES-SAPICOURT","COURJEONNET","COURMAS","COURTAGNON","COURTEMONT-VARENNES","COURTERON","COURTHIEZY", \
"COURVILLE","COUVIGNON","COUVROT","CRAMANT","CREZANCY","CROUTTES-SUR-MARNE","CRUGNY","CUCHERY","CUIS","CUISLES", \
"CUMIERES","CUNFIN","DAMERY","DIZY","DOLANCOURT","DOMPTIN","DORMANS","ECUEIL","EGUILLY-SOUS-BOIS","ENGENTE", \
"EPERNAY","ESSOMES-SUR-MARNE","ESSOYES","ETAMPES-SUR-MARNE","ETOGES","ETRECHY","FAVEROLLES-ET-COEMY", \
"FEREBRIANGES","FESTIGNY","FLEURY-LA-RIVIERE","FONTAINE","FONTAINE-DENIS-NUISY","FONTAINE-SUR-AY","FONTETTE", \
"FOSSOY","FRAVAUX","GERMAINE","GERMIGNY","GIVRY-LES-LOISY","GLAND","GLANNES","GRAUVES","GUEUX","GYE-SUR-SEINE", \
"HAUTVILLERS","HERMONVILLE","HOURGES","IGNY-COMBLIZY","JANVRY","JAUCOURT","JAULGONNE","JONCHERY-SUR-VESLE", \
"JONQUERY","JOUY-LES-REIMS","LA CELLE-SOUS-CHANTEMERLE","LA CHAPELLE-MONTHODON","LA NEUVILLE-AUX-LARRIS", \
"LA VILLE-SOUS-ORBAIS","LAGERY","LANDREVILLE","LE BREUIL","LE MESNIL-SUR-OGER","LES MESNEUX","LES RICEYS", \
"LEUVRIGNY","LHERY","LIGNOL-LE-CHATEAU","LISSE-EN-CHAMPAGNE","LOCHES-SUR-OURCE","LOISY-EN-BRIE","LOISY-SUR-MARNE", \
"LOUVOIS","LUDES","MAILLY-CHAMPAGNE","MANCY","MARDEUIL","MAREUIL-LE-PORT","MAREUIL-SUR-AY","MARFAUX","MERFY", \
"MERLAUT","MERREY-SUR-ARCE","MERY-PREMECY","MEURVILLE","MEZY-MOULINS","MONDEMENT-MONTGIVROUX","MONT-SAINT-PERE", \
"MONTBRE","MONTGENOST","MONTGUEUX","MONTHELON","MONTHUREL","MONTIER-EN-L'ISLE","MONTIGNY-SUR-VESLE", \
"MONTREUIL-AUX-LIONS","MORANGIS","MOSLINS","MOUSSY","MUSSY-SUR-SEINE","MUTIGNY","NANTEUIL-LA-FORET", \
"NANTEUIL-SUR-MARNE","NESLE-LE-REPONS","NESLES-LA-MONTAGNE","NEUVILLE-SUR-SEINE","NOE-LES-MALLETS", \
"NOGENT-L'ABBESSE","NOGENT-L'ARTAUD","NOGENTEL","OEUILLY","OGER","OIRY","OLIZY","ORBAIS-L'ABBAYE","ORMES", \
"OYES","PARGNY-LES-REIMS","PASSY-GRIGNY","PASSY-SUR-MARNE","PAVANT","PEVY","PIERRY","PLAINES-SAINT-LANGE", \
"POILLY","POLISOT","POLISY","PONTFAVERGER-MORONVILLIERS","POUILLON","POURCY","PROUILLY","PROVERVILLE","PUISIEULX", \
"REIMS","REUIL","REUILLY-SAUVIGNY","RILLY-LA-MONTAGNE","RIZAUCOURT-BUCHEY","ROMENY-SUR-MARNE","ROMERY","ROMIGNY", \
"ROSNAY","ROUVRES-LES-VIGNES","SAACY-SUR-MARNE","SACY","SAINT-AGNAN","SAINT-AMAND-SUR-FION", \
"SAINT-EUPHRAISE-ET-CLAIRIZET","SAINT-GILLES","SAINT-LUMIER-EN-CHAMPAGNE","SAINT-MARTIN-D'ABLOIS","SAINT-THIERRY", \
"SAINT-USAGE","SAINTE-GEMME","SARCY","SAUDOY","SAULCHERY","SAULCY","SAVIGNY-SUR-ARDRES","SELLES","SERMIERS", \
"SERZY-ET-PRIN","SEZANNE","SILLERY","SOULIERES","SPOY","TAISSY","TALUS-SAINT-PRIX","TAUXIERES-MUTRY","THIL", \
"TOURS-SUR-MARNE","TRAMERY","TRANNES","TRELOU-SUR-MARNE","TREPAIL","TRESLON","TRIGNY","TROIS-PUITS","TROISSY", \
"UNCHAIR","URVILLE","VAL-DE-VIERE","VAL-DES-MARAIS","VANAULT-LE-CHATEL","VANDEUIL","VANDIERES","VAUCIENNES", \
"VAUDEMANGE","VAVRAY-LE-GRAND","VAVRAY-LE-PETIT","VENTEUIL","VERNEUIL","VERPILLIERES-SUR-OURCE","VERT-TOULON", \
"VERTUS","VERZENAY","VERZY","VILLE-DOMMANGE","VILLE-EN-TARDENOIS","VILLE-SUR-ARCE","VILLENAUXE-LA-GRANDE", \
"VILLENEUVE-RENNEVILLE-CHEVIGNY","VILLERS-ALLERAND","VILLERS-AUX-NOEUDS","VILLERS-FRANQUEUX","VILLERS-MARMERY", \
"VILLERS-SOUS-CHATILLON","VILLEVENARD","VILLIERS-SAINT-DENIS","VINAY","VINCELLES","VINDEY","VITRY-EN-PERTHOIS", \
"VITRY-LE-CROISE","VIVIERS-SUR-ARTAUT","VOIGNY","VOIPREUX","VRIGNY"]

REGIONS_CHAMPAGNE=["BAR SUR AUBOIS","REGION DE SEZANNE","REGION DE BOUZY AMBONNAY","VALLEE DE L'ARDRE","BAR SUR AUBOIS", \
"BAR SUR AUBOIS","BAR SUR AUBOIS","BAR SUR AUBOIS","VALLEE DE L'ARDRE","GRANDE VALLEE DE LA MARNE","BAR SEQUANNAIS", \
"COTE DES BLANCS","GRANDE VALLEE DE LA MARNE","REGION DE L'AISNE","BAR SEQUANNAIS","BAR SEQUANNAIS","BAR SUR AUBOIS", \
"BAR SEQUANNAIS","REGION DE SEZANNE","BAR SUR AUBOIS","REGION DE L'AISNE","VALLEE DE LA MARNE RIVE DROITE", \
"REGION DE VITRY LE FRANCOIS","REGION DE VITRY LE FRANCOIS","REGION DE L'AISNE","LES COTEAUX DU PETIT MORIN", \
"REGION DE VERZY VERZENAY","LES COTEAUX DU PETIT MORIN","VALLEE DE LA MARNE RIVE DROITE","BAR SUR AUBOIS", \
"COTE DES BLANCS","LES COTEAUX DU PETIT MORIN","REGION DE VILLERS MARMERY TREPAIL","BAR SEQUANNAIS","REGION DE SEZANNE", \
"MONTAGNE OUEST","REGION DE L'AISNE","REGION DE VILLERS MARMERY TREPAIL","VALLEE DE LA MARNE RIVE DROITE", \
"GRANDE VALLEE DE LA MARNE","REGION DE L'AISNE","BAR SUR AUBOIS","VALLEE DE L'ARDRE","REGION DE L'AISNE", \
"MONTAGNE OUEST","VALLEE DE L'ARDRE","VALLEE DE LA MARNE RIVE GAUCHE","REGION DE BOUZY AMBONNAY","BAR SEQUANNAIS", \
"MONTAGNE OUEST","REGION DE L'AISNE","MASSIF DE SAINT THIERRY","VALLEE DE L'ARDRE","LES COTEAUX DU PETIT MORIN", \
"REGION DE SEZANNE","REGION D'EPERNAY","BAR SEQUANNAIS","BAR SEQUANNAIS","MASSIF DE SAINT THIERRY","REGION DE L'AISNE", \
"BAR SEQUANNAIS","REGION DE VILLERS MARMERY TREPAIL","BAR SEQUANNAIS","MASSIF DE SAINT THIERRY","VALLEE DE L'ARDRE", \
"MONTAGNE OUEST","BAR SUR AUBOIS","GRANDE VALLEE DE LA MARNE","VALLEE DE LA MARNE RIVE DROITE","REGION DE L'AISNE", \
"REGION DE VITRY LE FRANCOIS","BAR SEQUANNAIS","REGION DE SEZANNE","REGION DE L'AISNE","REGION DE L'AISNE", \
"REGION DE L'AISNE","VALLEE DE LA MARNE RIVE DROITE","VALLEE DE L'ARDRE","REGION D'EPERNAY","MASSIF DE SAINT THIERRY", \
"BAR SEQUANNAIS","REGION DE L'AISNE","REGION DE L'AISNE","REGION DE CHIGNY LES ROSES","COTE DES BLANCS","REGION DE L'AISNE", \
"LES COTEAUX DU PETIT MORIN","BAR SUR AUBOIS","BAR SUR AUBOIS","BAR SUR AUBOIS","LES COTEAUX DU PETIT MORIN", \
"REGION DE L'AISNE","MASSIF DE SAINT THIERRY","REGION DE CHIGNY LES ROSES","VALLEE DE LA MARNE RIVE GAUCHE", \
"MONTAGNE OUEST","MONTAGNE OUEST","LES COTEAUX DU PETIT MORIN","MONTAGNE OUEST","VALLEE DE L'ARDRE","REGION DE L'AISNE", \
"BAR SEQUANNAIS","REGION DE L'AISNE","VALLEE DE L'ARDRE","BAR SUR AUBOIS","REGION DE VITRY LE FRANCOIS","COTE DES BLANCS", \
"REGION DE L'AISNE","REGION DE L'AISNE","VALLEE DE L'ARDRE","VALLEE DE LA MARNE RIVE DROITE","COTE DES BLANCS", \
"VALLEE DE LA MARNE RIVE DROITE","GRANDE VALLEE DE LA MARNE","BAR SEQUANNAIS","VALLEE DE LA MARNE RIVE GAUCHE", \
"GRANDE VALLEE DE LA MARNE","BAR SUR AUBOIS","REGION DE L'AISNE","VALLEE DE LA MARNE RIVE DROITE","MONTAGNE OUEST", \
"BAR SEQUANNAIS","BAR SUR AUBOIS","REGION D'EPERNAY","REGION DE L'AISNE","BAR SEQUANNAIS","REGION DE L'AISNE", \
"LES COTEAUX DU PETIT MORIN","LES COTEAUX DU PETIT MORIN","VALLEE DE L'ARDRE","LES COTEAUX DU PETIT MORIN", \
"VALLEE DE LA MARNE RIVE GAUCHE","VALLEE DE LA MARNE RIVE GAUCHE","BAR SUR AUBOIS","REGION DE SEZANNE","REGION DE BOUZY AMBONNAY", \
"BAR SEQUANNAIS","REGION DE L'AISNE","BAR SUR AUBOIS","VALLEE DE L'ARDRE","MONTAGNE OUEST","LES COTEAUX DU PETIT MORIN", \
"REGION DE L'AISNE","REGION DE VITRY LE FRANCOIS","COTE DES BLANCS","MONTAGNE OUEST","BAR SEQUANNAIS","GRANDE VALLEE DE LA MARNE", \
"MASSIF DE SAINT THIERRY","VALLEE DE L'ARDRE","VALLEE DE LA MARNE RIVE GAUCHE","MONTAGNE OUEST","BAR SUR AUBOIS", \
"REGION DE L'AISNE","MONTAGNE OUEST","VALLEE DE LA MARNE RIVE DROITE","MONTAGNE OUEST","REGION DE SEZANNE","REGION DE L'AISNE", \
"VALLEE DE LA MARNE RIVE DROITE","REGION DE L'AISNE","VALLEE DE L'ARDRE","BAR SEQUANNAIS","REGION DE L'AISNE","COTE DES BLANCS", \
"MONTAGNE OUEST","BAR SEQUANNAIS","VALLEE DE LA MARNE RIVE GAUCHE","VALLEE DE L'ARDRE","BAR SUR AUBOIS", \
"REGION DE VITRY LE FRANCOIS","BAR SEQUANNAIS","LES COTEAUX DU PETIT MORIN","REGION DE VITRY LE FRANCOIS", \
"REGION DE BOUZY AMBONNAY","REGION DE CHIGNY LES ROSES","REGION DE VERZY VERZENAY","REGION D'EPERNAY", \
"VALLEE DE LA MARNE RIVE GAUCHE","VALLEE DE LA MARNE RIVE GAUCHE","GRANDE VALLEE DE LA MARNE","VALLEE DE L'ARDRE", \
"MASSIF DE SAINT THIERRY","REGION DE VITRY LE FRANCOIS","BAR SEQUANNAIS","VALLEE DE L'ARDRE","BAR SUR AUBOIS", \
"REGION DE L'AISNE","LES COTEAUX DU PETIT MORIN","REGION DE L'AISNE","REGION DE CHIGNY LES ROSES","REGION DE SEZANNE", \
"BAR SEQUANNAIS","REGION D'EPERNAY","REGION DE L'AISNE","BAR SUR AUBOIS","MASSIF DE SAINT THIERRY","REGION DE L'AISNE", \
"REGION D'EPERNAY","REGION D'EPERNAY","REGION D'EPERNAY","BAR SEQUANNAIS","GRANDE VALLEE DE LA MARNE","VALLEE DE L'ARDRE", \
"REGION DE L'AISNE","VALLEE DE LA MARNE RIVE GAUCHE","REGION DE L'AISNE","BAR SEQUANNAIS","BAR SEQUANNAIS", \
"REGION DE VILLERS MARMERY TREPAIL","REGION DE L'AISNE","REGION DE L'AISNE","VALLEE DE LA MARNE RIVE GAUCHE", \
"COTE DES BLANCS","COTE DES BLANCS","VALLEE DE LA MARNE RIVE DROITE","REGION DE L'AISNE","MONTAGNE OUEST", \
"LES COTEAUX DU PETIT MORIN","MONTAGNE OUEST","REGION DE L'AISNE","REGION DE L'AISNE","REGION DE L'AISNE", \
"MASSIF DE SAINT THIERRY","REGION D'EPERNAY","BAR SEQUANNAIS","VALLEE DE L'ARDRE","BAR SEQUANNAIS","BAR SEQUANNAIS", \
"REGION DE VILLERS MARMERY TREPAIL","MASSIF DE SAINT THIERRY","VALLEE DE L'ARDRE","MASSIF DE SAINT THIERRY", \
"BAR SUR AUBOIS","REGION DE VERZY VERZENAY","REGION DE CHIGNY LES ROSES","VALLEE DE LA MARNE RIVE DROITE", \
"REGION DE L'AISNE","REGION DE CHIGNY LES ROSES","BAR SUR AUBOIS","REGION DE L'AISNE","VALLEE DE LA MARNE RIVE GAUCHE", \
"VALLEE DE LA MARNE RIVE DROITE","MONTAGNE OUEST","BAR SUR AUBOIS","REGION DE L'AISNE","MONTAGNE OUEST","REGION DE L'AISNE", \
"REGION DE VITRY LE FRANCOIS","MONTAGNE OUEST","VALLEE DE L'ARDRE","REGION DE VITRY LE FRANCOIS","REGION D'EPERNAY", \
"MASSIF DE SAINT THIERRY","BAR SEQUANNAIS","REGION DE L'AISNE","VALLEE DE L'ARDRE","REGION DE SEZANNE", \
"REGION DE L'AISNE","BAR SUR AUBOIS","VALLEE DE L'ARDRE","REGION DE VILLERS MARMERY TREPAIL","MONTAGNE OUEST", \
"VALLEE DE L'ARDRE","REGION DE SEZANNE","REGION DE VERZY VERZENAY","LES COTEAUX DU PETIT MORIN","BAR SUR AUBOIS", \
"REGION DE CHIGNY LES ROSES","LES COTEAUX DU PETIT MORIN","REGION DE BOUZY AMBONNAY","MASSIF DE SAINT THIERRY", \
"REGION DE BOUZY AMBONNAY","VALLEE DE L'ARDRE","BAR SUR AUBOIS","REGION DE L'AISNE","REGION DE VILLERS MARMERY TREPAIL", \
"VALLEE DE L'ARDRE","MASSIF DE SAINT THIERRY","REGION DE CHIGNY LES ROSES","VALLEE DE LA MARNE RIVE GAUCHE", \
"VALLEE DE L'ARDRE","BAR SUR AUBOIS","REGION DE VITRY LE FRANCOIS","COTE DES BLANCS","REGION DE VITRY LE FRANCOIS", \
"VALLEE DE L'ARDRE","VALLEE DE LA MARNE RIVE DROITE","VALLEE DE LA MARNE RIVE GAUCHE","REGION DE VILLERS MARMERY TREPAIL", \
"REGION DE VITRY LE FRANCOIS","REGION DE VITRY LE FRANCOIS","VALLEE DE LA MARNE RIVE GAUCHE","REGION DE L'AISNE", \
"BAR SEQUANNAIS","LES COTEAUX DU PETIT MORIN","COTE DES BLANCS","REGION DE VERZY VERZENAY","REGION DE VERZY VERZENAY", \
"MONTAGNE OUEST","VALLEE DE LA MARNE RIVE DROITE","BAR SEQUANNAIS","REGION DE SEZANNE","COTE DES BLANCS", \
"REGION DE CHIGNY LES ROSES","MONTAGNE OUEST","MASSIF DE SAINT THIERRY","REGION DE VILLERS MARMERY TREPAIL", \
"VALLEE DE LA MARNE RIVE DROITE","LES COTEAUX DU PETIT MORIN","REGION DE L'AISNE","REGION D'EPERNAY","REGION DE L'AISNE", \
"REGION DE SEZANNE","REGION DE VITRY LE FRANCOIS","BAR SEQUANNAIS","BAR SEQUANNAIS","BAR SUR AUBOIS","COTE DES BLANCS","MONTAGNE OUEST"]
TYPE_APPORTS=["engrais organique","engrais mineral","engrais organo-mineral","amendements","pas d'apport","AUTRES"]
ENTRETIEN_SOL=[ "enherbement permanent tous les rangs","enherbement permanent un rang sur deux","couvert hivernal","travail du sol","sol nu","autres"]

# ###########################
# Exceptions Physiocap
# ###########################
class physiocap_exception( BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
# FILTRER    
class physiocap_exception_rep( physiocap_exception):
    pass
class physiocap_exception_fic( physiocap_exception):
    pass
class physiocap_exception_csv( physiocap_exception):
    pass
class physiocap_exception_err_csv( physiocap_exception):
    pass
class physiocap_exception_trop_err_csv( physiocap_exception):
    pass
class physiocap_exception_mid( physiocap_exception):
    pass
class physiocap_exception_no_mid( physiocap_exception):
    pass
class physiocap_exception_no_transform( physiocap_exception):
    pass
class physiocap_exception_no_gpkg( physiocap_exception):
    pass
class physiocap_exception_vecteur_type_inconnu( physiocap_exception):
    pass
class physiocap_exception_calcul_segment_invalid( physiocap_exception):
    pass
class physiocap_exception_stop_user( physiocap_exception):
    pass  

#INTER
class physiocap_exception_vignette_exists( physiocap_exception):
    pass
class physiocap_exception_points_invalid( physiocap_exception):
    pass
class physiocap_exception_segment_invalid( physiocap_exception):
    pass    
    
# INTRA
class physiocap_exception_interpolation( physiocap_exception):
    pass
class physiocap_exception_no_processing( physiocap_exception):
    pass
class physiocap_exception_no_saga( physiocap_exception):
    pass
class physiocap_exception_project_contour_incoherence( physiocap_exception):
    pass
class physiocap_exception_attribut_multiple_incoherent( physiocap_exception):
    pass
class physiocap_exception_project_point_incoherence( physiocap_exception):
    pass
class physiocap_exception_windows_saga_ascii( physiocap_exception):
    pass
class physiocap_exception_windows_value_ascii( physiocap_exception):
    pass
class physiocap_exception_pg( physiocap_exception):
    pass
class physiocap_exception_raster_sans_iso( physiocap_exception):
    pass
class physiocap_exception_no_choix_raster_iso( physiocap_exception):
    pass
class physiocap_exception_probleme_caractere_librairie( physiocap_exception):
    pass
class physiocap_exception_iso_manquant( physiocap_exception):
    pass
class physiocap_exception_raster_manquant( physiocap_exception):
    pass
class physiocap_exception_raster_ou_iso_existe_deja( physiocap_exception):
    pass
