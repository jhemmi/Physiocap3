import processing
info_extent= '795825.2212942,796084.9317131,6674126.9668843,6674710.7083225 [EPSG:2154]'

from processing.tools.system import getTempFilename
nom_raster_temp = getTempFilename( "tif")
from qgis.core import QgsProcessingOutputRasterLayer
raster_temp = QgsProcessingOutputRasterLayer( nom_raster_temp)
print( raster_temp)
print( raster_temp.name())
# saga { 'SHAPES' : 'D:/GIS/DATA/POINTS_L93.shp', 
#    'FIELD' : 'DIAM', 'DW_WEIGHTING' : 1,      'DW_IDW_POWER' : 2, 'DW_IDW_OFFSET' : False, 
#    'DW_BANDWIDTH' : 1, 'SEARCH_POINTS_ALL' : 0,
#    'SEARCH_RANGE' : 0, 'SEARCH_RADIUS' : 100, 
#    'SEARCH_POINTS_MIN' : 1, 'SEARCH_POINTS_MAX' : 10, 'SEARCH_DIRECTION' : 0, 
#    'OUTPUT_EXTENT' : info_extent, 'TARGET_USER_SIZE' : 100, 'TARGET_DEFINITION' : 1, 
#    'TARGET_USER_FITS' : 0, 
#    'TARGET_TEMPLATE' : 'D:\GIS\DATA\TARGET_OUT_GRID.sdat', 'TARGET_OUT_GRID' : nom_raster_temp }
#'TARGET_OUT_GRID' : 'D:/GIS/DATA/TARGET_OUT_GRID_NEW.sdat'}

temp_dir = "/tmp/processing_57ba05b6d2ff4b339c37717268eceb9e/ce32f1a2880a433e9789536d25d02b80/"
temp_file = temp_dir + "OUTPUT2.tif"
shape_point = "/data/GIS/DATA/DATA_PHY/SORTIE_PHY/PHY3/vecteur/PHY3_POINTS_SANS_0_L93.shp"
shape_point_attr = shape_point + ",0,10,0"
IDW_QGIS = {'INTERPOLATION_DATA': shape_point_attr, 
'DISTANCE_COEFFICIENT':5, \
'COLUMNS':650,'ROWS':418,
'EXTENT':'795825.2212942,796084.9317131,6674126.9668843,6674710.7083225 [EPSG:2154]',
'OUTPUT' : nom_raster_temp 
}

print( IDW_QGIS)
retour_idw = processing.run("qgis:idwinterpolation", IDW_QGIS)
print( "Fin IDW QGIS {0}".format( retour_idw))
