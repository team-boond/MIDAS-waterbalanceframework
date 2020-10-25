import calendar
import pandas as pd



crop = ['Onion-dry']
sowdates = ['1-10-2020']
area_crop = [1]
print("Hello")
def cropreq(crop, sowdates, area_crop):#crop_name, sow_date
    tot_requirement=0
    monthly_list=[]
    total_list=[]
    parent_dir='C:/Users/Rishabh/waterbudgeting/Nashik/Sinnar/Konambe/'
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

        df = pd.read_csv('days_crop.csv')
        days_scrop = []#will contain the growth stages of the crop

        for j in range(0,len(df)):
            if df['crop'][j] == name:
                days_scrop.append(df['initial_stage'][j])
                days_scrop.append(df['dev_stage'][j])
                days_scrop.append(df['mid_stage'][j])
                days_scrop.append(df['late_stage'][j])
        crop_grow=days_scrop# extract dynamically from the database, this is the growth stage of the crop
        kc_scrop = []
        df = pd.read_csv('kc_val.csv')
        for j in range(0,len(df)):
            if df['crop'][j] == crop[i]:
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
        start_date=int(date[0])
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
            i=i+1
        #end of the while loop
        #print(kc_calibrate)
        #loop to calculate the total water required for each crop per month
        #print('**************************************************************************************')
        print(kc_calibrate)
        for i in range(0,12):
            if kc_calibrate[i] != 0:
                monthly_water_req[i] = ((area*10000)*(et_2002[i]/1000)*kc_calibrate[i]*m[y_t][i])/1000
                print('Water required for', name,'in', m_name[i], 'is', (monthly_water_req[i]), 'TCM')
        print('Total water required for', name,'in', area,'hectares of land','is', (sum(monthly_water_req)), 'TCM')
        #print('**************************************************************************************')
        monthly_list.append(monthly_water_req)
        tot_requirement=tot_requirement+int(sum(monthly_water_req))
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
    et_2002 = [3.73, 4.74, 5.71, 6.5, 6.46, 5.27, 4.42, 4.06, 4.37, 4.77, 4.15, 3.78]
    return et_2002

cropreq(crop,sowdates,area_crop)
#cropreq(['Bajra','Tomato'], ['10-02-2020','10-02-2019'], [1,1])