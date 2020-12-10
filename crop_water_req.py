#Work pending
#Introduce the cwr of grapes 
#link the ET code with this code
#Create the data base for all the excel sheets

import calendar
import pandas as pd

import datetime

#crop = ['Wheat']
#sowdates = ['30-11-2020']
#area_crop = [27]
#print("Hello")
def cropreq(crop, sowdates, area_crop,t,village):#crop_name, sow_date
    tot_requirement=0
    monthly_list=[]
    total_list=[]
    for i in range(0,len(crop)):
        df = pd.read_csv('days_crop.csv')
        name = crop[i]
        sowdate = sowdates[i]
        area = area_crop[i]
        monthly_water_req = [0.0 for i in range(0,12)]

        et_2002=getET()#function to extract the Et value
        
        #The month days and month name is stored for printing purposes
        m=[[31,28,31,30,31,30,31,31,30,31,30,31], [31,29,31,30,31,30,31,31,30,31,30,31]]#write a code for leap year too
        m_name = ['January','February','March','April','May','June','July','August','September','October','November','December'] 
        year = int(sowdate[6:])

        #df = pd.read_csv('days_crop_max.csv')
        df = pd.read_csv('days_crop_min.csv')
        days_scrop = []#will contain the growth stages of the crop

        for j in range(0,len(df)):
            #if df['crop'][j]==name:
            if name in df['crop'][j]:
                days_scrop.append(df['initial_stage'][j])
                days_scrop.append(df['dev_stage'][j])
                days_scrop.append(df['mid_stage'][j])
                days_scrop.append(df['late_stage'][j])
        crop_grow=days_scrop# extract dynamically from the database, this is the growth stage of the crop
        kc_scrop = []
        #df = pd.read_csv('kc_val_temp.csv')
        df = pd.read_csv('kc_val.csv')
        for j in range(0,len(df)):
            #if df['crop'][j]==crop[i]:
            if crop[i] in df['crop'][j]:
                kc_scrop.append(df['initial_stage'][j])
                kc_scrop.append(df['dev_stage'][j])
                kc_scrop.append(df['mid_stage'][j])
                kc_scrop.append(df['late_stage'][j])
        kc_crop=kc_scrop#[0.45,0.75,1.15,0.8]# extract dynamically from the database, this is the kc value of the crop
        kc_calibrate=[0,0,0,0,0,0,0,0,0,0,0,0]
        y_t = 0
        if(calendar.isleap(year)):
            y_t=1
        else:
            y_t=0
        
        #loop intializations
        month=m[y_t]
        date=sowdate.split('-')
        start_month=int(date[1])
        start_date=int(date[0])-1
        month[start_month-1]=month[start_month-1]-start_date
        #print(month[start_month-1])
        i=0
        j=start_month-1
        c=start_month-1
        kc=0
        count=0
        flag=0
        #algorithm to calibrate the kc value per month
        #print('crop growth stages',crop_grow)
        while(i<len(crop_grow)):
            d=crop_grow[i]
            j=c
            #print(kc_crop[i])
            while(j<len(month)):
                
                if(d>=(month[j]-count)):

                    kc=kc+((month[j]-count)*kc_crop[i])/month[j]
                    
                    kc_calibrate[j]=kc
                    kc=0
                    flag=1
                    d=d-(month[j]-count)
                    count=0
                    if(j==len(month)-1):
                        if(calendar.isleap(year+1)):
                            month=m[1]
                        else:
                            month=m[0]
                        j=0
                    else:
                        j=j+1
                elif(d<(month[j]-count)):
                    if(count!=0):
                        kc=kc+((d*kc_crop[i])/month[j])
                        count=count+d

                    else:
                        count=d
                        kc=kc+((count*kc_crop[i])/month[j])
                        

                    flag=0
                    d=0
                    c=j
                    j=j+1
                    break

            if((i==len(crop_grow)-1) and flag==0):
                kc_calibrate[c]=kc_crop[i]
            #print(c)
            i=i+1
        
        #end of the while loop
        #print(kc_calibrate)
        #loop to calculate the total water required for each crop per month
        #print('**************************************************************************************')
        #print(kc_calibrate)
        

        for i in range(0,12):
            if kc_calibrate[i] != 0:
                if(start_month==i+1):
                    monthly_water_req[i] = (((area*10000)*(et_2002[i]/1000)*kc_calibrate[i]*m[y_t][i])/1000)*0.10
                    #monthly_water_req[i] = (((area*10000)*(et_2002[i]/1000)*kc_calibrate[i])/1000)*0.1
                #elif(i==c):
                #    monthly_water_req[i] = (((area*10000)*(et_2002[i]/1000)*kc_calibrate[i]*m[y_t][i])/1000)*0.10
                else:
                    monthly_water_req[i] = ((area*10000)*(et_2002[i]/1000)*kc_calibrate[i]*m[y_t][i])/1000
                    #monthly_water_req[i] = ((area*10000)*(et_2002[i]/1000)*kc_calibrate[i])/1000
                if(name=='Tomato' and t=='Rabi' and village=='Konambe'):
                    monthly_water_req[i]=monthly_water_req[i]-monthly_water_req[i]*0.42*0.9
                if(name=='Cabbage'and t=='Rabi' and village=='Konambe'):
                    monthly_water_req[i]=monthly_water_req[i]-monthly_water_req[i]*0.68*0.2
                if(name=='Onion-dry'and t=='Rabi' and village=='Konambe'):
                    monthly_water_req[i]=monthly_water_req[i]-monthly_water_req[i]*0.30*0.1
                if(name=='Carrot'and t=='Rabi' and village=='Konambe'):
                    monthly_water_req[i]=monthly_water_req[i]-monthly_water_req[i]*0.40*0.2
                print('Water required for', name,'in', m_name[i], 'is', ((monthly_water_req[i])), 'TCM')
        print('Total water required for', name,'in', area,'hectares of land','is', ((sum(monthly_water_req))), 'TCM')
        #print('**************************************************************************************')
        monthly_list.append(monthly_water_req)
        tot_requirement=tot_requirement+(sum(monthly_water_req))
        total_list.append(sum(monthly_water_req))
        '''tot_consum = (tot_consum + kc_calibrate[i]*m[y_t][i]*et_2002[i]) #unit = mm
        total_area = tot_consum*area*10000 #unit = mm*m*m
        total_area_cubic_meter = total_area/1000 #unit = m*m*m
        print(total_area_cubic_meter)'''

        #Compute the crop water requirement :
        # Procedure:
        #1) Fetch the evapotransipiration for that location
        #2) multiply it with the calibrated kc value
        #3) mutiply it with number of days
        #4) you will get the total crop requirement for the each month
        #return the crop requirement for every month as a list

        '''name="Bajra"#input from the user, should be a list of crops
        sowdate="01-02-2020"#input from the user, should be the sow date corresponding to the crop
        area='88'#input from the user in ha. should be the area corresponding to the crop 
        #for loop
        cropreq(name,sowdate)
        #multiply the crop requirement you have returned with the area for total crop requirement computation and display the list of crops along with its total consumption
        '''
        #end of the main for loop
    return tot_requirement,monthly_list,total_list
    #end of function

#function to extract ET
def getET():
    import et_calc as et_dyn
    et_2002=et_dyn.evapotrans()
    #et_2002 = [3.73, 4.74, 5.71, 6.5, 6.46, 5.27, 4.42, 4.06, 4.37, 4.77, 4.15, 3.78]
    #et_2019 = [32, 27, 10.1, 10.5, 2.6, 55.7, 80.2, 81.4, 77.5, 77.4, 55, 34.5]
    return et_2002
import xlrd
import math
#cropreq(crop,sowdates,area_crop,'Kharif','Konambe')
#cropreq(['Bajra','Tomato'], ['10-02-2020','10-02-2019'], [1,1])
def kc_correction(name,kc_scrop,days_scrop,sow_date):
    loc='C:/Users/Rishabh/waterbudgeting/PadaliHMSfinal.xlsx'
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(1)
    #print('Hello',sheet.cell_value(5,1))
    crop_height={'Rice':0.8,'Maize-sweet':1.5,'Millet':1.5,'Soybean':0.6,'Groundnut':0.4,'Lentils':0.4}
    if(name in crop_height):
        height=crop_height[name]
    else:
        height=0
    date_1 = datetime.datetime.strptime(sow_date, "%d-%m-%y")
    start_date_mid = (date_1 + datetime.timedelta(days=(days_scrop[0]+days_scrop[1]))).timetuple().tm_yday
    start_date_end = (date_1 + datetime.timedelta(days=(days_scrop[0]+days_scrop[1]+days_scrop[2]))).timetuple().tm_yday
    humidity_mid=0
    windspeed_mid=0
    for i in range(start_date_mid+1,start_date_mid+1+(days_scrop[2]*2)):
        #print('excel',sheet.cell_value(i,1))
        windspeed_mid=windspeed_mid+sheet.cell_value(i,2)
        humidity_mid=humidity_mid+sheet.cell_value(i,1)
    humidity_mean_mid=humidity_mid/(days_scrop[2]*2)
    windspeed_mean_mid=windspeed_mid/(days_scrop[2]*2)

    humidity_end=0
    windspeed_end=0
    for i in range(start_date_end+1,start_date_end+1+(days_scrop[3]*2)):
        #print('excel',sheet.cell_value(i,1))
        windspeed_end=windspeed_end+sheet.cell_value(i,2)
        humidity_end=humidity_end+sheet.cell_value(i,1)
    humidity_mean_end=humidity_end/(days_scrop[2]*2)
    windspeed_mean_end=windspeed_end/(days_scrop[2]*2)
    kc_crop=[]
    for i in range(0, len(kc_scrop)):
        if(i==2):
            kc=kc_scrop[i]+(0.04*(windspeed_mean_mid-2)-0.004*(humidity_mean_mid-45))*math.pow(height/3,0.3)
            kc_crop.append(kc)
        elif(i==3):
            kc=kc_scrop[i]+(0.04*(windspeed_mean_end-2)-0.004*(humidity_mean_end-45))*math.pow(height/3,0.3)
            kc_crop.append(kc)
        else:
            kc_crop.append(kc_scrop[i])
    print(kc_crop)

    #print(start_date_mid)

kc_correction('Maize-sweet',[0.4,0.8,1.15,1],[20,30,50,10],'10-06-20')
