
import os
import pandas as pd
import indices as ind
def main():
    a=input(("Press one for first time user and two for registered user"))
    if(int(a) ==1):
        enter_primary_Details()
    else:
        district_name=input("Enter the district name")
        tehsil_name=input("Enter the tehsii name")
        village_name=input("Enter the village name")
        show_water_budget(district_name,tehsil_name,village_name)

def enter_primary_Details():
    print()
    parent_dir="C:/Users/Rishabh/waterbudgeting/"
    print("Basic village details")
    district_name=input("Enter the district name")
    directory=district_name
    path = parent_dir+directory
    os.mkdir(path)
    tehsil_name=input("Enter the tehsii name")
    directory=directory+"/"+tehsil_name
    path = parent_dir+directory
    os.mkdir(path)
    village_name=input("Enter the village name")
    directory=directory+"/"+village_name
    path = parent_dir+directory
    os.mkdir(path)
    
    

    print()
    print("Enter the domestic details")
    human_pop=int(input("Enter the population of villagers"))
    cattle_pop=int(input("Enter the cattle population"))
    sheep_pop=int(input("Enter the sheep/goats population"))
    poultry_pop=int(input("Enter the poultry population"))
    dict_pop={'Human pop':human_pop,'cattle pop':cattle_pop,'sheep pop':sheep_pop,'poultry pop':poultry_pop}
    df=pd.DataFrame(dict_pop,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+village_name+'_primary.csv',index=False)

    print()
    print("Enter the cropping details")
    print("Enter kharif crops detais")
    crop_kharif=[]
    sow_kharif=[]
    area_kharif=[]
    while(True):
        crop_kharif.append(input('Enter crop name : '))
        sow_kharif.append(input('Enter sow date : '))
        area_kharif.append(int(input('Enter area grown :')))
        a=input("Enter 1 to continue")
        if(int(a)!=1):
            break
    dict_kharif={'Kharif crop':crop_kharif,'Sow date':sow_kharif,'Area':area_kharif}
 
    df=pd.DataFrame(dict_kharif)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'Kharif_crops.csv',index=False)
    print()
    print("Enter rabi crops detais")
    crop_rabi=[]
    sow_rabi=[]
    area_rabi=[]
    while(True):
        crop_rabi.append(input('Enter crop name : '))
        sow_rabi.append(input('Enter sow date : '))
        area_rabi.append(int(input('Enter area grown :')))
        a=input("Enter 1 to continue")
        if(int(a)!=1):
            break
    dict_rabi={'Rabi crop':crop_rabi,'Sow date':sow_rabi,'Area':area_rabi}
    df=pd.DataFrame(dict_rabi)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'Rabi_crops.csv',index=False)

    print()
    
    print("Enter the water conservation structures details")
    i=0
    name=[]
    depth=[]
    area=[]
    storage_cap=[]
    number_struct=[]
    while(True):

        name.append(input("Enter the name of the water conservation structure"))
        if(name[i]=='CCT'):
            number_struct.append(int(input("Enter running meter of CCT")))
            width=0.5#in m
            depth.append(fetch_depth(name[i]))
            storage_cap.append(width*depth[i]*number_struct[i])
            area.append(width*depth[i])
        else:
            number_struct.append(int(input("Enter number of structure")))
            coordinates=fetch_loc(name[i])
            depth.append(fetch_depth(name[i]))
            storage_cap.append(getStorageTemp(name[i]))
            area.append(storage_cap[i]/depth[i])#temporary function
        
        #area.append(ind.extent_of_water_area(coordinates[0],coordinates[1]))
        #storage_cap.append(area[i]*depth[i]/1000)
        #print(area[i])
        print("Storage of the single structure ", name[i], " is ",storage_cap[i],"TCM")
        b1=input("Press 1 to continue")
        i=i+1
        if(int(b1)!=1):
            break
    dict_struct={'Structure name':name,'Area':area,'Storage capacity':storage_cap,'Number':number_struct}
    df=pd.DataFrame(dict_struct)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'WCS_details.csv',index=False)

    print()
    print("Enter the village farm ponds details")
    number_lined=int(input("Enter the number of lined farm ponds in the village"))
    avg_area_lined=int(input("Enter the average area of the lined farm ponds"))
    depth_farmpond=3#depth of the farm pond is considered to be 1m
    storage_farmpondlined=avg_area_lined*depth_farmpond/1000
    dict_farml={'Lined farm pond':number_lined,'Area':avg_area_lined,'Capacity':storage_farmpondlined}
    df=pd.DataFrame(dict_farml,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'farmponds_lined.csv',index=False)
    print()
    depth_farmpond_unlined=9#depth of the farm pond is considered to be 2 m
    number=int(input("Enter the number of non lined farm ponds in the village"))
    
    avg_area=int(input("Enter the average area of the non lined farm ponds"))
    storage_farmpond=avg_area*depth_farmpond_unlined/1000

    dict_farm={'Non Lined farm pond':number,'Area':avg_area,'Capacity':storage_farmpond}
    df=pd.DataFrame(dict_farm,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'farmponds.csv',index=False)

    print()
    c=input("Do you want to see the water budget")
    if(c=='y' or c=='Y'):
        show_water_budget(district_name,tehsil_name,village_name)
    else:
        print("Thank you for entering in the details")

def show_water_budget(d,t,v):
    print()
    village_area=getArea(v,t,d)
    import total_rainfall as tr
    rainfall_avail=tr.rainfall(village_area)
    import Total_runoff as run
    [tot_runoff,worthy_area]=run.runoff()
    
    #tot_runoff=1000#dummy needs to be calculated
    infilteration_village=rainfall_avail-tot_runoff


    print("The amount of water available from rainall is ",rainfall_avail," TCM")
    print("Total runoff is ",tot_runoff," TCM")
    print()
    print("Amount of water for domestic details")
    parent_dir="C:/Users/Rishabh/waterbudgeting/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+v+"_primary.csv")
    details=[df['Human pop'][0],df['cattle pop'][0],df['sheep pop'][0],df['poultry pop'][0]]
    dom_req=getDomestic(details)
    dom_req_kharif=getDomesticKharif(details)
    temp=['Human population','Cattle population','Sheep population','Poultry population']
    sum_domreq=0
    sum_domkharif=0
    for i in range(0,len(details)):
        print("The Total annual water requriement for ",details[i]," "+temp[i]+" is "+str(dom_req[i])+" TCM")
        sum_domreq=sum_domreq+dom_req[i]
        sum_domkharif=sum_domkharif+dom_req_kharif[i]
    
    print()
    print("Total crop water requirement of kharif crops")
    df=pd.read_csv(home_dir+"Kharif_crops.csv")
    crop=[]
    sow=[]
    area=[]
    for i in range(0,len(df)):
        crop.append(df['Kharif crop'][i])
        sow.append(df['Sow date'][i])
        area.append(df['Area'][i])
    
    import crop_water_req as cwr
    [total_cropreq,monthly_list,total_list]=cwr.cropreq(crop,sow,area,'Kharif')
    df['Monthly list']=monthly_list
    df['Total_list']=total_list
    df.to_csv(home_dir+"Kharif_crops.csv",index=False)
    print('Crop water requirment for grape is in 60 hectares of land is 720TCM')
    total_cropreq=total_cropreq+720+142.5#considered fodders also for kharif, later change it in main code
    print()
    print("Total amount of surface water impounded")
    df=pd.read_csv(home_dir+"WCS_details.csv")
    surface_water_kharif=0
    
    tot_infilteration=0#Total seepage done even during rabi
    total_infilteration_nonmon=0
    

    for i in range(0,len(df)):
        if(df['Structure name'][i]=='K T weir'):
            [infilteration,surface_water,infilteration_nonmon]=ind.KT_weir(df['Storage capacity'][i],df['Area'][i])
            infilteration=infilteration*df['Number'][i]
            surface_water=surface_water*df['Number'][i]
            infilteration_nonmon=infilteration_nonmon*df['Number'][i]
            surface_water_kharif=surface_water_kharif+surface_water
            total_infilteration_nonmon=total_infilteration_nonmon+infilteration_nonmon
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," during the monsoon is ",infilteration,"TCM")
            print("The surface water in ",df['Number'][i]," ", df['Structure name'][i]," after the monsoon is ",surface_water,"TCM")
            
            print()
        elif(df['Structure name'][i]=='Konambe dam'):
            [infilteration,surface_water,infilteration_nonmon]=ind.dam(df['Storage capacity'][i],df['Area'][i])
            infilteration=infilteration*df['Number'][i]
            infilteration_nonmon=infilteration_nonmon*df['Number'][i]
            surface_water=surface_water*df['Number'][i]
            
            surface_water_kharif=surface_water_kharif+650#full 1501 tcm wont be available to be used for the village
            print(infilteration_nonmon)
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," during the monsoon is ",infilteration,"TCM")
            print("The surface water in ",df['Number'][i]," ", df['Structure name'][i]," after the monsoon is ",surface_water,"TCM")
            infilteration=infilteration+infilteration_nonmon
            print()
        elif(df['Structure name'][i]=='CCT'):
            [infilteration,soil_mois]=ind.CCT(df['Storage capacity'][i])
            print("The seepage from ", df['Structure name'][i]," during the monsoon is ",infilteration,"TCM")
            print("The soilmois from ", df['Structure name'][i]," during the monsoon is ",soil_mois,"TCM")
            #infilteration=infilteration+soil_mois
            infilteration=soil_mois
        elif(df['Structure name'][i]=='Recharge shaft'):
            infilteration=ind.shaft(df['Storage capacity'][i])
            infilteration=infilteration*df['Number'][i]
            print("The seepage from ", df['Structure name'][i]," during the monsoon is ",infilteration,"TCM")
        else:
            infilteration=ind.WCS(df['Storage capacity'][i])
            infilteration=infilteration*df['Number'][i]
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," to the groundwater is",infilteration,"TCM")
            if(df['Structure name'][i]=='Percolation tank forest' or df['Structure name'][i]=='Cement nala bund forest'):
                   infilteration=0
            print()
        tot_infilteration=tot_infilteration+infilteration
        
    infilteration_village=infilteration_village+tot_infilteration
    
    #Need to subtract protective irrigation if present
    

    print()
    print("Total amount of surface water impounded by lined farm ponds")
    df=pd.read_csv(home_dir+"farmponds_lined.csv")
    surface_water=df['Capacity'][0]*df['Lined farm pond'][0]
    #surface_water=surface_water-((df['Area'][0]*1900/1000)/1000)
    print("The surface water available in ",df['Lined farm pond'][0]," lined farm ponds after the monsoon is ",surface_water,"TCM")
    #print('u-lined',usable_water)
    surface_water_kharif=surface_water_kharif+surface_water

    print()
    print("Total amount of surface water impounded by non lined farm ponds")
    df=pd.read_csv(home_dir+"farmponds.csv")
    [infilteration,surface_water,infilteration_nonmon]=ind.storage_tanks(df['Capacity'][0],df['Area'][0])
    
    print("The surface water available after seepage in ",df['Non Lined farm pond'][0]," Non lined farm ponds after the monsoon is ",(df['Non Lined farm pond'][0]*(surface_water)),"TCM")
    print("The seepage from ",df['Non Lined farm pond'][0]," Non lined farm ponds after the monsoon is ",(df['Non Lined farm pond'][0]*(infilteration)),"TCM")
    #print('u-unlined',usable_water*df['Non Lined farm pond'][0])

    surface_water_kharif=surface_water_kharif+(surface_water*df['Non Lined farm pond'][0])
    
    infilteration_village=infilteration_village+(infilteration*df['Non Lined farm pond'][0])
    total_infilteration_nonmon=total_infilteration_nonmon+(infilteration_nonmon*df['Non Lined farm pond'][0])
    #print("total nonmon", total_infilteration_nonmon)
    #surface_water_kharif=surface_water_kharif-1501+500#this is temporary, just subtracting konambe dam surface water

#Pending work
#Extract near real time evaporation data from the HMS excel sheet.

    surface_water_kharif=surface_water_kharif-(surface_water_kharif*0.30)
    #et=0.3*rainfall_avail
    print()
    print("Evapotranspiration loses from non-agricultrual land")
    et=ind.Evapotranspiration()
    print("Total water lost in barren is ", et[0]/1000,'TCM') 
    print("Total water lost in shrubs is ", (et[1]/1000),'TCM') 
    print("Total water lost in forest is ", et[2]/1000,'TCM')
    #protect_irrigation=0.1*total_cropreq
    print()
    print("Total surface water available after kharif ",surface_water_kharif,'TCM')
    print("Total seepage in the village after kharif ",infilteration_village,'TCM')
    print('Total kharif crop requirement is ',total_cropreq,'TCM')
    #print('The protective irrigation given is ',protect_irrigation,'TCM')
    print('Total domestic requirement for the kharif is ',sum_domkharif,'TCM')
    print('Total loss from non agricultural land is ',(et[0]/1000)+(et[2]/1000)+(et[1]/1000),'TCM')
    print()
    water_kharif=infilteration_village+surface_water_kharif-total_cropreq-sum_domreq-(et[0]/1000)-(et[2]/1000)-(et[1]/1000)#-protect_irrigation
    #water_kharif=infilteration_village+surface_water_kharif-total_cropreq-sum_domreq-et-protect_irrigation
    print('The amount of water present for rabi is',water_kharif,' TCM')

    print()
    a=int(input("Press 1 to continue with rabi planning"))
    if(a==1):
        rabi_req=input_rabi(d,t,v)
    annual_gross_draft=(.1*total_cropreq)+sum_domreq+rabi_req-(surface_water_kharif-total_infilteration_nonmon)-(.1*rabi_req)
    print("Annual gross draft ",annual_gross_draft)
    groundwater=groundwater_avail(worthy_area)
    print('Groundwater available in the village', groundwater)
    stage_of_development=(annual_gross_draft/groundwater)*100
    print('Stage of groundwater developement is ',stage_of_development,'%')
#Ground water availabilty
def groundwater_avail(worthy_area):
    pre_monlevel=13.5
    post_monlevel=6
    specific_yield=0.02
    groundwater=specific_yield*(pre_monlevel-post_monlevel)*worthy_area*10

    return groundwater
    #print(surface_water_kharif,' Surface water')
    #print(sum_domreq,' Domestic requirement')
    
def input_rabi(d,t,v):
    parent_dir="C:/Users/Rishabh/waterbudgeting/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+"Rabi_crops.csv")
    crop_rabi=[]
    sow_rabi=[]
    area_rabi=[]
    for i in range(0,len(df)):
        crop_rabi.append(df['Rabi crop'][i])
        sow_rabi.append(df['Sow date'][i])
        area_rabi.append(df['Area'][i])
    
    import crop_water_req as cwr
    
    [total_cropreq,monthly_list,total_list]=cwr.cropreq(crop_rabi,sow_rabi,area_rabi,'Rabi')
    df['Monthly list']=monthly_list
    df['Total_list']=total_list
    df.to_csv(home_dir+"Rabi_crops.csv",index=False)
    print('Total rabi crop requirement is ',total_cropreq,'TCM')
    return total_cropreq
def getStorageTemp(name):
    n=['Earthen nala bund','K T weir','Cement nala bund','Cement nala bund forest','Percolation tank','Percolation tank forest','Gabion','Recharge shaft','Konambe dam']
    cap=[0.467,1.05,13.045,7.88,25.15,3.88,.345,1,1512]#in TCM,here for recharge shaft the avg tcm has been taken from doc given by deshpande sir+
    i=n.index(name)
    return cap[i]
'''
def getAreaTemp(name):
    n=['Earthen nala bund','K T weir','Cement nala bund','Percolation tank','Percolation tank new']
    area=[155.55,700,3487.5,12575,4800]#in m2
    
    i=n.index(name)
    return area[i]
'''
def fetch_depth(name):
    n=['Earthen nala bund','K T weir','Cement nala bund','Cement nala bund forest','Percolation tank','Percolation tank forest','Gabion','Recharge shaft','CCT','Konambe dam']
    i=n.index(name)
    depth=[2,2,1,1,3,3,1,1,0.6,11.11]
    return depth[i]
def getDomestic(d):
    tot_Domestic=[]
    tot_Domestic.append(d[0]*55*365/1000000)
    tot_Domestic.append(d[1]*35*365/1000000)
    tot_Domestic.append(d[2]*5*365/1000000)
    tot_Domestic.append(d[3]*2*365/1000000)
    return tot_Domestic
def getDomesticKharif(d):
    tot_Domestic=[]
    tot_Domestic.append(d[0]*55*122/1000000)
    tot_Domestic.append(d[1]*35*122/1000000)
    tot_Domestic.append(d[2]*5*122/1000000)
    tot_Domestic.append(d[3]*2*122/1000000)
    return tot_Domestic
def fetch_loc(name):
    lat=73.95
    lon=19.18
    return [lat, lon]
def getArea(n,t,d):
    area=2022.1
    return area


main()
