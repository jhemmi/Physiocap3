import processing
info_extent= '795825.2212942,796084.9317131,6674126.9668843,6674710.7083225 [EPSG:2154]'

from processing.tools.system import getTempFilename
nom_raster_temp = getTempFilename( "tif")
from qgis.core import QgsProcessingOutputRasterLayer
raster_temp = QgsProcessingOutputRasterLayer( nom_raster_temp)
print( raster_temp)
print( raster_temp.name())

shape_point = "/data/GIS/DATA/DATA_PHY/SORTIE_PHY/PHY3/vecteur/PHY3_POINTS_SANS_0_L93.shp"

IDW_GDAL = { 'INPUT' : shape_point, 
    'Z_FIELD' : 'DIAM', 'POWER' : 2, 
    'SMOOTHING' : 0, 
    'RADIUS_1' : 3, 'RADIUS_2' : 3, 'ANGLE' : 0, 
    'MAX_POINTS' : 1, 'MIN_POINTS' : 1, 
    'NODATA' : -9999, 
    'OPTIONS' : '', 'DATA_TYPE' : 5, 
    'OUTPUT' : nom_raster_temp 
    }
#IDW_QGIS = {'INTERPOLATION_DATA': shape_point_attr, 
#'DISTANCE_COEFFICIENT':5, \
#'COLUMNS':650,'ROWS':418,
#'EXTENT':'795825.2212942,796084.9317131,6674126.9668843,6674710.7083225 [EPSG:2154]',
#'OUTPUT' : nom_raster_temp 
#}

print( IDW_GDAL)
retour_idw = processing.run("gdal:gridinversedistance", IDW_GDAL)
print( "Fin IDW GDAL {0}".format( retour_idw))

# exemple gdal Warp
#
#{ 'INPUT' : '/tmp/processing_57ba05b6d2ff4b339c37717268eceb9e/46fd4e1f601d4d91945167ade6f9ad9a/OUTPUT.tif', 'MASK' : '/data/GIS/DATA/DATA_PHY/data/Contour_L93.shp', 'NODATA' : -9999, 'ALPHA_BAND' : False, 'CROP_TO_CUTLINE' : True, 'KEEP_RESOLUTION' : False, 'OPTIONS' : '', 'DATA_TYPE' : 5, 'OUTPUT' : '/tmp/processing_57ba05b6d2ff4b339c37717268eceb9e/487dbca5177c47d8871fc817e791212b/OUTPUT.tif' }
#
#GDAL command:
#gdalwarp -ot Float32 -of GTiff -cutline /data/GIS/DATA/DATA_PHY/data/Contour_L93.shp -crop_to_cutline -dstnodata -9999.0 /tmp/processing_57ba05b6d2ff4b339c37717268eceb9e/46fd4e1f601d4d91945167ade6f9ad9a/OUTPUT.tif /tmp/processing_57ba05b6d2ff4b339c37717268eceb9e/487dbca5177c47d8871fc817e791212b/OUTPUT.tif
