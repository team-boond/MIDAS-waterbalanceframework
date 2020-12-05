
#Work pending
#Extract the rainfall from secondary source and do not hard-code it

def rainfall(area,village_name):
    if(village_name=='Konambe'):
        rainfall_amt=780
    else:
        rainfall_amt=520
    rainfall_avail=(rainfall_amt*area)/100
    return rainfall_avail