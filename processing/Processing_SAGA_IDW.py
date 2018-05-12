#from processing.core.Processing import Processing
#Processing.initialize()
#versionSAGA = processing.algs.saga.SagaUtils.getInstalledVersion()
#print( versionSAGA)
import processing
from qgis.core import QgsProcessingFeedback
from processing.tools.system import getTempFilename
info_extent= '796018.2658206049,796079.989864021, 6674128.609732771,6674254.041102098 [EPSG:2154]'
mon_feedback = QgsProcessingFeedback()
nom_raster_temp = getTempFilename( "sdat")
#raster_temp = QgsProcessingOutputRasterLayer( nom_raster_temp)
#
IDW_SAGA = { 'SHAPES' : '/data/GIS/DATA/DATA_PHY/vecteur_point.shp', 
    'FIELD' : 'DIAM', 'DW_WEIGHTING' : 1,      'DW_IDW_POWER' : 2, 'DW_IDW_OFFSET' : False, 
    'DW_BANDWIDTH' : 1, 'SEARCH_POINTS_ALL' : 0,
    'SEARCH_RANGE' : 0, 'SEARCH_RADIUS' : 10, 
    'SEARCH_POINTS_MIN' : 1, 'SEARCH_POINTS_MAX' : 10, 'SEARCH_DIRECTION' : 0, 
    'OUTPUT_EXTENT' : info_extent, 'TARGET_USER_SIZE' : 1, 'TARGET_DEFINITION' : 0, 'TARGET_USER_FITS' : 0, 
    'TARGET_TEMPLATE' : None, 'TARGET_OUT_GRID' : nom_raster_temp }
#'TARGET_OUT_GRID' : 'D:/GIS/DATA/TARGET_OUT_GRID_NEW.sdat'}
#   'TARGET_OUT_GRID' : '' }    'TARGET_OUT_GRID' : 'C:/Users/Utilisateur/AppData/Local/Temp/processing_30acb258f1ae40db85c6dd6a0f0ab5aa/f17c58dbd75747269ca73df49c2a4b6h/TARGET_OUT_GRID.sdat' }
print( IDW_SAGA)
le_retour = processing.run("saga:inversedistanceweightedinterpolation", IDW_SAGA,  feedback = mon_feedback)
print( le_retour)
