#from processing.core.Processing import Processing
#Processing.initialize()
#versionSAGA = processing.algs.saga.SagaUtils.getInstalledVersion()
#print( versionSAGA)
from qgis.core import ( Qgis,  QgsProcessingFeedback)
#, \
#    QgsProcessingOutputRasterLayer,  QgsProcessingParameterRasterDestination)
import processing

info_extent= '795825.2212942,796084.9317131,6674126.9668843,6674710.7083225 [EPSG:2154]'
mon_feedback = QgsProcessingFeedback()

print( "Version QGIS" + Qgis.QGIS_VERSION )
from processing.tools.system import   getTempDirInTempFolder #  getTempFilename
nom_temp_dir = getTempDirInTempFolder().replace("\\", "/") 
nom_raster_temp = nom_temp_dir + "/" + "TARGET_OUT_GRID.sdat"
# JHJH 
#layerURI_nettoye = nom_raster_temp.replace("\\", "/")
#raster_temp = QgsProcessingOutputRasterLayer( nom_raster_temp)
#destination_raster_temp = QgsProcessingParameterRasterDestination( raster_temp) 
#
IDW_SAGA = { 'SHAPES' : 'D:/GIS/DATA/POINTS.shp', 
    'FIELD' : 'DIAM', 'DW_WEIGHTING' : 1,      'DW_IDW_POWER' : 2, 'DW_IDW_OFFSET' : False, 
    'DW_BANDWIDTH' : 1, 'SEARCH_POINTS_ALL' : 0,
    'SEARCH_RANGE' : 0, 'SEARCH_RADIUS' : 100, 
    'SEARCH_POINTS_MIN' : 1, 'SEARCH_POINTS_MAX' : 10, 'SEARCH_DIRECTION' : 0, 
    'OUTPUT_EXTENT' : info_extent, 'TARGET_USER_SIZE' : 10, 'TARGET_DEFINITION' : 0, 'TARGET_USER_FITS' : 0, 
    'TARGET_TEMPLATE' : None, 
    'TARGET_OUT_GRID' : nom_raster_temp }
    # KOs - 1   'TARGET_TEMPLATE' : ''  ==> Génère une erreur  "AttributeError: 'NoneType' object has no attribute 'source'
    # KOs - 2   'TARGET_OUT_GRID' : nom_raster_temp (sdat)  ==> Génère un fichier prj mais pas de raster sdat + message Inverse Distance Weighted: could not initialize data objects
    # KOs - 2bis   'TARGET_OUT_GRID' : nom_raster_temp (sgrd)  ==> Génère un fichier prj mais pas de raster sdat + message Inverse Distance Weighted: could not initialize data objects
    # KOs - 3  'TARGET_OUT_GRID' : 'memory:' ==> Génère un probleme de droit d'acces et could not initialize data objects
    # KOs - 4  'TARGET_OUT_GRID' : None  ==> Message valeur incorrecte
    # KOs - 5  sans 'TARGET_OUT_GRID' message explicite  : parametre manquant
    # KOs - 6   'TARGET_OUT_GRID' : nom_temp_dir  ==> Génère un fichier prj mais pas de raster sdat + message Inverse Distance Weighted: could not initialize data objects
print( IDW_SAGA)
#processing.algorithmHelp("saga:inversedistanceweightedinterpolation")
#processing.algorithmHelp("native:extractvertices")
print( "================== PROCESSING ================================")
le_retour = processing.run("saga:inversedistanceweightedinterpolation", IDW_SAGA,  feedback=mon_feedback)
print( le_retour)
print( "================== FIN PROCESSING ================================")
