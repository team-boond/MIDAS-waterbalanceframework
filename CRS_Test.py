import sys
import fiona
#import rasterio as r
import geopandas as gpd

shp=gpd.read_file('C:/Python27/QGIS/Konambe/Konambe_village.shp')
vector= fiona.open('C:/Python27/QGIS/Konambe/Konambe_village.shp',mode='r')
vector=shp.to_crs({'init': 'epsg:32643'})
vector.to_file('C:/Python27/QGIS/Konambe/abcd.shp')
