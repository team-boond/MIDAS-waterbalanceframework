MIDAS water accounting platform

Some of our main files are below

Konambe folder- contains the shapefiles of the village boundaries

Nashik folder- contains all the data in .csv format of the village which includes 
               crop details, Water conservation structures present in the village etc

b3_clip.tif,b4_clip.tif,b8_clip.tif,b11_clip.tif- various frames of remote sensing data for ET calc

crop_water_req.py- contains the code to calculate the crop water requirement of various crops

days_crop_temp.csv- contains the growth stages of the crop without WALMI calibration

days_crop.csv- contains the growth stages of the crop with WALMI calibration

et_calc.py- contains the code to calculate the evapotranspiration using the pennman method.

indices.py- Algorithm for water body extraction and ET calculation using satellite data

kc_val_temp.csv- contains the crop coefficient as per the growth stages of the crop without WALMI calibration

kc_val.csv- contains the crop coefficient as per the growth stages of the crop with WALMI calibration

total_rainfall.py- code returns the rainfall measured in a village

Total_runoff.py- code compute the runoff generated in the village

waterbodylocation.py- code returns the location the water body extracted in indices.py

waterbudgeting.py- the main code containing the water balance framework and calling the above functions
