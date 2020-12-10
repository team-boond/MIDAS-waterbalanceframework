import pandas as pd
import os
dir = os.getcwd() + '\MIDAS-waterbalanceframework-CARDvillage\MIDAS-waterbalanceframework-CARDvillage'
print(os.getcwd())
df = pd.read_csv(dir + '/Pune/Shirur/Kanhur' + '/Rabi_crops.csv')
df = df.sort_values(by='drip',ascending=False,ignore_index=True)
de = pd.read_csv(dir + '/drip_efficiency.csv')
dripeff = []
for i in range(0,len(df)):
    flag = 0
    for j in range(0,len(de)):
        if df['Rabi crop'][i] == de['crop'][j]:
            dripeff.append(de['eff'][j])
            flag = 1
    if flag == 0:
        dripeff.append(0)
df['dripeff'] = dripeff
water_area = []
for i in range(0,len(df)):
    water_area.append(df['Total_list'][i]/df['Area'][i])
df['water_intensity'] = water_area
#print(df)
sum = df['water_intensity'].sum()
weight = []
for i in range(0,len(df)):
    weight.append(df['water_intensity'][i]/sum)
df['weight'] = weight
cwr = 4745
aval = 4105
old_drip = [0,0,0]
for i in range(0,300):
    print(i) 
    print(cwr)
    for j in range(0,len(df)):
        if  cwr > aval :
            if old_drip[j] + df['weight'][j] < 100 :
                cwr = cwr - df['Total_list'][j] * df['dripeff'][j]/100 * (old_drip[j] + df['weight'][j])/100
                old_drip[j] = old_drip[j] + df['weight'][j]
                #print(df['weight'][j])
                print(df['Rabi crop'][j],'drip',old_drip[j])
        else:
            break
    df['drip'] = old_drip