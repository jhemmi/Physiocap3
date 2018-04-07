import processing
info_extent= '796018.2658206049,6674128.609732771,796079.989864021,6674254.041102098 [EPSG:2154]'
from processing.tools.system import getTempFilename
nom_raster_temp = getTempFilename( "sdat")
IDW_SAGA={ 'SHAPES' : '/data/GIS/DATA/DATA_PHY/SORTIE_PHY/PHY3/vecteur/PHY3_POINTS_SANS_0_L93.shp',
'FIELD' : 'DIAM', 'NPMIN' : 3, 
'NPMAX' : 20, 'NPPC' : 5, 'K' : 140, 
'OUTPUT_EXTENT' : '795825.2212942,796084.9317131,6674126.9668843,6674710.7083225 [EPSG:2154]', 
'TARGET_USER_SIZE' : 100, 'TARGET_USER_FITS' : 0, 'TARGET_OUT_GRID' :'/tmp/processing_7d21d13f385c482c9d0e8c84b92e4203/5ac7e1a1c89744.sdat'}
processing.run("saga:grid_spline", IDW_SAGA)