'''
import pandas as pd

df = pd.read_csv('days_crop.csv')
c1,c2,c3 = [],[],[]
for i in range(0,len(df)):
    if df['total days'][i] <= 100:
        c1.append(df['crop'][i])
    elif df['total days'][i] > 100 and df['total days'][i] <= 150:
        c2.append(df['crop'][i])
    elif df['total days'][i] > 150:
        c3.append(df['crop'][i])
c3.append('Grapes')

df = pd.read_csv('CWR_from_input.csv')
de = pd.read_csv('drip_efficiency.csv')

# pick the indices of crop which are in c3 and water budget of village 

# where the indices correspond to CWR_from_input.csv
crop = []
eff = []
cwr = []
area = []
c3_vill = []
for i in c3:
    for j in range(0,len(df['crop'])):
        if i == df['crop'][j]:
            c3_vill.append(j)
            crop.append(df['crop'][j])
            cwr.append(df['CWR'][j])
            area.append(df['area'][j])

# similarly pick the indices           
            
val_eff = []            
for i in c3_vill:
    for j in range(0,len(de['crop'])):
        if de['crop'][j] == df['crop'][i]:
            val_eff.append(j)
            eff.append(de['eff'][j])

# create a dataframe containing required values
            
ndf = pd.DataFrame({'crop':crop,'cwr':cwr,'eff':eff,'area':area})
print(ndf)

water_aval = 4460
crop = input("Enter crop name on which drip is to be applied :")
drip_area = int(input("Enter % area to be cultivated in drip :"))



def drip(crop,drip_area):
    cwr_tot = df['CWR'].sum()
    for i in range(0,len(ndf)):
        if ndf['crop'][i]==crop:
            break
    new_cwr = cwr_tot - (ndf['cwr'][i]*ndf['eff'][i]*(drip_area/100))
    print("New Crop Water Requirement after applying ",drip_area,"% of drip on",crop,"is",new_cwr,"TCM")
    print("Water Available :",water_aval,"TCM")
    f = check(new_cwr)
    if f == -1:
        choice_drip = input("Your CWR is high!!! Do you want to increase area under drip Y/N :")
        if choice_drip == "Y":
            drip_area = int(input("Enter % area to be cultivated in drip :"))
            drip(crop,drip_area)
        elif choice_drip == "N":
            choice_area = input("Your CWR is high!!! Do you want to decrease area of crop Y/N :")
            if choice_area == "Y":
                min_area(crop,)

dictonary mein crops rakho. Calculate values based on
single function
make single dictionary


def check(new_cwr):
    if new_cwr>water_aval:
        return -1
    else:
        return 1    
drip(crop,drip_area)'''

import pandas as pd

'''df = pd.read_csv('days_crop.csv')
c1,c2,c3 = [],[],[]
for i in range(0,len(df)):
    if df['total days'][i] <= 100:
        c1.append(df['crop'][i])
    elif df['total days'][i] > 100 and df['total days'][i] <= 150:
        c2.append(df['crop'][i])
    elif df['total days'][i] > 150:
        c3.append(df['crop'][i])
c3.append('Grapes')'''

df = pd.read_csv('CWR_from_input.csv')
de = pd.read_csv('drip_efficiency.csv')

'''# pick the indices of crop which are in c3 and water budget of village 

# where the indices correspond to CWR_from_input.csv
crop = []
eff = []
cwr = []
area = []
c3_vill = []
for i in c3:
    for j in range(0,len(df['crop'])):
        if i == df['crop'][j]:
            c3_vill.append(j)
            crop.append(df['crop'][j])
            cwr.append(df['CWR'][j])
            area.append(df['area'][j])

# similarly pick the indices           
            
val_eff = []            
for i in c3_vill:
    for j in range(0,len(de['crop'])):
        if de['crop'][j] == df['crop'][i]:
            val_eff.append(j)
            eff.append(de['eff'][j])

# create a dataframe containing required values
#       
ndf = pd.DataFrame({'crop':crop,'cwr':cwr,'eff':eff,'area':area})'''

cwr_tot = df['CWR'].sum()
water_aval = 4460
drip_crops = {}
area_crops = {}


def input_user():
    print("Your crops are:")
    print(df)
    choice = int(input("Enter 1 if you want to calculate drip \n OR \n Enter 2 if you want to reduce area \n OR \n Enter 3 if you want to replace crops"))
    if choice == 1:
        crop = input("Enter Crop name :")
        area = int(input("Enter % to be under drip area:"))
        drip_crops[crop] = area
        #print(drip_crops)
    elif choice == 2:
        crop = input("Enter Crop name :")
        area = int(input("Enter % area to be dropped:"))
        area_crops[crop] = area
        #print(area_crops)
    elif choice == 3:
        replace()
    up_cwr(drip_crops,area_crops)

def get_cwr(crop):
    for i in range(0,len(df)):
        if df['crop'][i] == crop:
            return df['CWR'][i]

def get_eff(crop):
    for i in range(0,len(de)):
        if de['crop'][i] == crop:
            return de['eff'][i]

def up_cwr(drip_crops,area_crops):
    new_cwr = cwr_tot
    for i in drip_crops:
        cwr = get_cwr(i)
        eff = get_eff(i)
        new_cwr = new_cwr - ((drip_crops[i]/100)*cwr*eff)
    for i in area_crops:
        cwr = get_cwr(i)
        eff = get_eff(i)
        if i in drip_crops:
            new_cwr = new_cwr-((area_crops[i]/100)*cwr)
        else:
            new_cwr = new_cwr - ((area_crops[i]/100)*cwr)
    print("Updated crop Water",new_cwr)
    print("Water Availability",water_aval)
    if new_cwr>water_aval:
        choice = int(input("Enter 1 to enter more parameters else enter anything"))
        if choice == 1:
            input_user()

import crop_water_req as cwr_replace
pd.options.mode.chained_assignment = None
def replace():
    crop_replace=[]
    sowdate = []
    area = []
    crop = input("Enter previous crop")
    crop_replace.append(input("Enter new crop"))
    sowdate.append(input("Enter sow date DD-MM-YYYY format"))
    area.append(int(input("Enter crop area")))
    [cwr_replace_crop,monthly,total] = cwr_replace.cropreq(crop_replace,sowdate,area)
    for i in range(0,len(df)):
        if df['crop'][i]==crop:
            df['crop'][i] = crop_replace[0]
            df['CWR'][i] = cwr_replace_crop
            df['area'][i] = area[0]
    df.to_csv('CWR_from_input.csv',index = False)
    input_user()


input_user()
