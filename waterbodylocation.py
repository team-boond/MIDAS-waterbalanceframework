import rasterio
from rasterio.features import shapes
from shapely.geometry import shape, Point
import geojson
import geopandas as gp


#convert raster to vector(GeoJSON)
def pointArea(lat,lon,loc):
    
    mask = None
    with rasterio.Env():
        with rasterio.open(loc) as src:#input the classified image
            image = src.read(1) # first band
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(
                shapes(image, mask=mask, transform=src.transform)))



        
    geoms = list(results)

    #input the coordinates of the point. must be utm coordinates
    point = Point(lat, lon)
    gpd  = gp.GeoDataFrame.from_features(geoms)
    gpd.crs = {'init' :'epsg:32643'}
    water_pol=gpd.loc[gpd['raster_val'] == 1]
    water_pol.crs = {'init' :'epsg:32643'}
    water_pol["area"] = water_pol['geometry'].area


    #save the geojson to a location.
    water_pol.to_file("C:/Users/risha/waterbudgeting/water_pol_konambe.geojson", driver="GeoJSON")

    #read geojson
    with open("C:/Users/risha/waterbudgeting/water_pol_konambe.geojson") as f:
        js = geojson.load(f)


    #find polygon which contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            print('Water area:', feature['properties']['area'])
            return feature['properties']['area']