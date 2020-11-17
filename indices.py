# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 20:15:10 2020

@author: DELL
"""

import rasterio as r
import rasterio.plot
import numpy as np
#import matplotlib.pyplot as plt
import os
from rasterio import plot
import rasterio.mask
import fiona
import copy

from rasterio.features import shapes
import geopandas as gpd
from geojson import FeatureCollection
#import geopandas.clip

#Required when I have the full image
l=os.listdir()
#print(l)
b3=r.open(l[3])
b4=r.open(l[4])
b8=r.open(l[5])
b11=r.open(l[2])
#use reproject code and use output of reproject in the vect variable
#check the projection of the shapefile. must be EPSG:32643
#lat=input("Enter the latitude of the WCS")
#lon=input("Enter the longitude of the WCS")
shp=gpd.read_file('C:/Users/Rishabh/waterbudgeting/Konambe/Konambe_village.shp')
vector1= fiona.open('C:/Users/Rishabh/waterbudgeting/Konambe/Konambe_village.shp',mode='r')
vect=shp.to_crs({'init': 'epsg:32643'})
#vector1.to_file('C:/Users/risha/waterbudgeting/Konambe/Konambe_village_vector.shp')

#print(vector1.crs)
def clip(raster,out):
    

    img = raster
    vector= fiona.open(vect,mode='r')
    geom = [feature["geometry"] for feature in vector]
    oimg, otns = rasterio.mask.mask(img,geom, crop=True)
    ometa = img.meta
    ometa.update({"driver": "GTiff",
                 "height": oimg.shape[1],
                 "width": oimg.shape[2],
                 "transform": otns})
    with rasterio.open(out, "w", **ometa) as dest:
        dest.write(oimg)
    return(r.open(out))


#clipb3=clip(b3,'b3_clip.tif')
#clipb4=clip(b4,'b4_clip.tif')
#clipb8=clip(b8,'b8_clip.tif')
#clipb11=clip(b11,'b11_clip.tif')

#After clipping(do not clip since you have clipped images. ust input them below.)

def Evapotranspiration():

    clipb4=r.open('b4_clip.tif')
    clipb8=r.open('b8_clip.tif' )  





    red = clipb4.read(1).astype('float32')
    nir = clipb8.read(1).astype('float32')


    ndvi=(nir-red)/(nir+red)



    ndviImage = rasterio.open('C:/Users/Rishabh/waterbudgeting/ndvi.tif','w',driver='Gtiff',
                              width=clipb4.width, 
                              height = clipb4.height, 
                              count=1, crs=clipb4.crs, 
                              transform=clipb4.transform, 
                              dtype='float32')
    ndviImage.write(ndvi,1)
    ndviImage.close()
    n=r.open('C:/Users/Rishabh/waterbudgeting/ndvi.tif')
    #ndvi_clip=clip(n,'ndvi_clip.tif')

    ndvi_rc=copy.copy(ndvi)
    ndvi_rc[np.where((ndvi>0.1) & (ndvi<=0.75))] = 2
    ndvi_rc[np.where(ndvi<=0.1)] = 1


    ndvi_rc[np.where(ndvi>0.75)] = 3
    np.unique(ndvi_rc)
    barren=np.count_nonzero(ndvi_rc==1)
    #print('barren',barren*100)
    #barren_et=((barren*100)-5883000)*0.05
    barren_et=12598100*0.05
    shrubs=np.count_nonzero(ndvi_rc==2)
    #print('shrubs',shrubs*100)
    #shrubs_et=shrubs*100*0.2
    shrubs_et=4642200*0.3
    forest=np.count_nonzero(ndvi_rc==3)
    #forest_et=forest*100*0.8
    forest_et=295200*0.8
    #print('forest',forest*100)
    et=[barren_et,shrubs_et,forest_et] #et in m^3
    return et  



#water 
def extent_of_water_area(latcoordinate, longcoordinates):

    clipb3=r.open('b3_clip.tif')
    clipb8=r.open('b8_clip.tif' ) 
    clipb11=r.open('b11_clip.tif' )

    n3 = clipb3.read(1).astype('float32')
    n8 = clipb8.read(1).astype('float32')
    n11 = clipb11.read(1).astype('float32')


    #ndbi=(n11-n8)/(n11+n8)
    #ndwi=(n3-n8)/(n3+n8)

    #w1 =np.ones_like(ndbi)
    #w2 =np.zeros_like(ndbi)
    w1 =np.ones_like(n11)
    w2 =np.zeros_like(n11)


    w=(np.logical_and(n11<0.1,n8<0.1))

    #w=(np.logical_and(ndbi<0,ndwi>0))
    water =np.where(w,w1,w2)
    water_body=np.count_nonzero(water==1)
    water_area=water_body*100 #water area
    print(water_area)
    water_bodyImage = rasterio.open('C:/Users/Rishabh/waterbudgeting/water_body.tif','w',driver='Gtiff',
                              width=clipb3.width, 
                              height = clipb3.height, 
                              count=1, crs=clipb3.crs, 
                              transform=clipb3.transform, 
                              dtype='float32')
    water_bodyImage.write(water,1)
    water_bodyImage.close()
    loc='C:/Users/Rishabh/waterbudgeting/water_body.tif'
    import waterbodylocation as wbl
    water_area=wbl.pointArea(latcoordinate,longcoordinates,loc)
    
    return water_area


def storage_tanks(storage,area):#village unlinedfarm ponds
    water_area=0.6*area
    days_monsoon=90
    
    infilteration=(water_area*days_monsoon*1.44/1000)/1000#seepage during monsoon
    
    surface_water=storage-(infilteration)
    return infilteration,surface_water
def KT_weir(storage,area):# K T weir
    water_area=0.6*area
    days_monsoon=90
    infilteration=(water_area*days_monsoon*1.44/1000)#seepage during monsoon
    #evaporation_monsoon=(water_area*days_monsoon*1.44/1000)#evaporation during monsoon considered as 1.44mm/day
    surface_water=storage-(infilteration)#surface water available after monsoon
    return infilteration,surface_water
def dam(storage,area):# minor irrigation project
    water_area=0.6*area*2
    days_monsoon=90
    days_nonmon=275
    infilteration=(water_area*days_monsoon*1.44/1000)#seepage during monsoon
    infilteration_nonmon=(water_area*days_nonmon*1.44/1000)#seepage during monsoon
    #evaporation_monsoon=(water_area*days_monsoon*1.44/1000)#evaporation during monsoon considered as 1.44mm/day
    surface_water=storage-(infilteration)#surface water available after monsoon
    return infilteration,surface_water,infilteration_nonmon

def WCS(storage):#for ENB, CNB, percolation tanks, Gabion and Recharge shaft
    fillings=2
    infilteration=fillings*storage*.5
    return infilteration
def CCT(storage):
    fillings =37#number of rainy
    infilteration=fillings*storage*0.1/1000
    soil_mois=fillings*storage*0.55/1000#10% seepage,35% evaporation rest soil moisture
    return infilteration,soil_mois
def shaft(storage):
    #fillings =70#number of rainy
    infilteration=storage*0.8
    return infilteration
    

#def farm_pondsstorage()

#et=Evapotranspiration()
#print("Total water lost in barren is ", et[0],'m3') 
#print("Total water lost in shrubs is ", et[1],'m3') 
#print("Total water lost in forest is ", et[2],'m3') 
#lat=386003
#lon=2186809
#area=extent_of_water_area(lat,lon)
#print(area)

#et=Evapotranspiration()













