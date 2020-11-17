import math
import calendar
from datetime import date
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

def getMonth(i):
    m=[[31,28,31,30,31,30,31,31,30,31,30,31], [31,29,31,30,31,30,31,31,30,31,30,31]]#write a code for leap year too
    current_date=date.today()
    year=current_date.year
    y_t=0
    if(calendar.isleap(year)):
        y_t=1
    else:
        y_t=0
    month=m[y_t]
    return month[i]
def getLatitude():
    #latitude in degrees of Sinnar
    return 19.84
def getElevation(lat):
    #elvation of Konambe village in m
    return 561
def getTemperature():
    return[29.5,16]

def evapotrans():
    i=0
    lat=getLatitude()
    month=getMonth(i)
    z=getElevation(lat)
    [Tmax,Tmin]=getTemperature()
    Tmean=(Tmax+Tmin)/2
    ea=get_ea((Tmax+Tmin)/2)
    ea=ea*0.1#Converting ea in mbar to kPa
    rn=getRadiation(lat,month,z,Tmax,Tmin,ea)
    #psychometric constanst
    gamma=getGamma(z)
    u2=getWind()
    #saturation vapor pressure at the mean daily maximum air temperature [kPa]
    eTmax=geteTmax(Tmax)
    #saturation vapor pressure at the mean daily minimum air temperature [kPa]
    eTmin=geteTmax(Tmin)
    es=getMeanSaturationVP(eTmax,eTmin)
    #slope vapor pressure curve [kPa/°C]
    delta=getdelta((Tmax+Tmin)/2)
    et0=(0.408*delta*(rn)+((gamma*900*u2*(es-ea))/(Tmean+273)))/(delta+gamma*(1+0.34*u2))
    print("Evapotranspiration is ",et0)
def getdelta(Tmean):
    delta=4098*(0.6108*math.exp((17.27*Tmean)/(Tmean+237.3)))/(math.pow(Tmean+237.3,2))
    return delta
def geteTmax(Tmax):
    eTmax=0.6108*math.exp((17.27*Tmax)/(Tmax+237.3))
    return eTmax
def getMeanSaturationVP(eTmax,eTmin):
    es=(eTmax+eTmin)/2
    return es
def getWind():
    #wind speed at 10 m above sea level, 10m is taken as per google
    h=10
    uz=0.447
    u2=uz*(4.87/(math.log(67.8*h-5.42)))
    return u2
def getGamma(z):
    #atmosperic pressure
    p=101.3*math.pow((293-0.0065*z)/293,5.26)
    gamma=p*0.665*math.pow(10,-3)
    return gamma
def getRadiation(lat,month,z,Tmax,Tmin,ea):
    #latitude in radians
    phi=(math.pi/180)*(lat)
    #inverse relative distance earth-sun
    dr=1+0.033*math.cos(2*math.pi*month/365)
    #solar declination(rad)
    dell=0.409*math.sin((2*math.pi*month/365)-1.39)
    #sunset hour angle(rad)
    omega=math.acos(-math.tan(phi)*math.tan(dell))
    #Solar constant
    Gsc=0.0820
    #Extraterrestial radiation MJ/m2/day
    Ra=(1440/math.pi)*Gsc*dr*((omega*math.sin(phi)*math.sin(dell)+math.cos(phi)*math.cos(dell)*math.sin(omega)))
    #Clear sky solar radiation MJ/m2/day
    Rso=(0.75+2*math.pow(10,-5)*z)*Ra
    #Solar radiation
    Rs=0.16*math.sqrt(Tmax-Tmin)*Ra
    #boltzman constant MJ/K^-4/m2/day
    bc=4.903*math.pow(10,-9)
    #K maximum absolute temperature during the 24-hour period [K = °C + 273.16]
    Tmaxk=Tmax+273.16
    #K minimum absolute temperature during the 24-hour period [K = °C + 273.16]
    Tmink=Tmin+273.16
    #net long wave radiation
    Rnl=bc*((math.pow(Tmaxk,4)+math.pow(Tmink,4))/2)*(0.34-0.14*math.sqrt(ea))*((1.35*(Rs/Rso))-0.35)
    #Net solar or net shortwave radiation
    Rns=(1-0.23)*Rs
    #Net radiation
    Rn=Rns-Rnl
    return Rn
evapotrans()