temp_mean_june = 14.8#26   #Celcius #took sinnar mean temp from worldweatheronline
humidity = 59         #percentage #took sinnar humidity avg from worldweatheronline
cloud_cover = 3 #65      #percentage
wind_speed_ph = 3.6      #km/hr#took same as paper
wind_speed_pd = 86.4   #km/day#took same as paper
altitude = 169    # m above sea level


ea = 16.8             #table 18 #wrt mean air temperature
ed = ea * humidity*0.01   # unit is m bar # *0.01 when humidity in percentage
print("ed is",ed)

diff_ea_ed = ea - ed    #difference between ea and ed # m bar
print("ea - ed =",diff_ea_ed)

fu = 0.27*(1+wind_speed_pd*0.01)    # wind velocity at height of 2m
print("fu is",fu)

w = 0.625    #table 21 #wrt temp and eleveation #related weighing factor

aero_d_t = (1-w)*fu*diff_ea_ed   #final aero dynamic term 
print("aero dynamic term is","{:.2f}".format(aero_d_t))

import pandas as pd
import math
temp_mean = 14.8#26   #Celcius #took sinnar mean temp from worldweatheronline

def getn_by_N(cc):    
    df = pd.read_csv('n_by_N(oktas).csv')
    print(math.ceil(cc*5))
    return df['n_by_N'][math.ceil(cc*5)]
def get_ea(temp_mean):
    df = pd.read_csv('SaturationVapourPressure.csv')
    if float(temp_mean).is_integer():
        ea = df['ea'][temp_mean]
        return ea
    else:
        index = int(temp_mean)
        read1, read2 = index, index+1
        ea = ((read2*df['ea'][read2])/(read1*df['ea'][read1]))*temp_mean
        return ea
ea = get_ea(temp_mean)
print(ea)

n_by_N = getn_by_N(2.8)
print(n_by_N)


cc = 7.8
df = pd.read_csv('n_by_N(oktas).csv')
print(math.ceil(cc*5))
df['n_by_N'][math.ceil(cc*5)]