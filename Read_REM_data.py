
# coding: utf-8

# In[3]:


import csv
import pandas as pd
import os
import datetime as dt
import numpy as np
import fnmatch

para_file = input("Input your parameter txt file: ")

def get_REM(path,sol_num,solar_time,time_type):
    for file in os.listdir(path):
        if time_type == 'Mean':
            if fnmatch.fnmatch(file, '*'+str(sol_num)+'0000000_______P*'):
                solar_hour = int(solar_time.split('.')[0])
                solar_minute = int((float(solar_time)-solar_hour)*60)
                df = pd.read_csv(path+file,header=None, usecols=[1,7])
                df = df[df[7] != '    UNK']
                df['Solar time (string)'] = df[1].apply(lambda x: x.split('M')[1].split('.')[0])
                df['Solar time'] = pd.to_datetime(df['Solar time (string)'], format='%H:%M:%S').dt.time
                return np.mean([float(x) for x in list(df[(df['Solar time'] > dt.time(solar_hour, solar_minute-10) )& (df['Solar time'] < dt.time(solar_hour, solar_minute+10))][7])])
        elif time_type == 'True':
            if fnmatch.fnmatch(file, '*'+str(sol_num)+'0000000_______P*'):
                solar_hour = int(solar_time.split('.')[0])
                solar_minute = int((float(solar_time)-solar_hour)*60)
                df = pd.read_csv(path+file,header=None, usecols=[2,7])
                df = df[df[7] != '    UNK']
                df['Solar time (string)'] = df[2].apply(lambda x: x.split(' ')[1])
                df['Solar time'] = pd.to_datetime(df['Solar time (string)'], format='%H:%M:%S').dt.time
                return np.mean([float(x) for x in list(df[(df['Solar time'] > dt.time(solar_hour, solar_minute-10) )& (df['Solar time'] < dt.time(solar_hour, solar_minute+10))][7])])
        else:
            return "Wrong Time Type: It should be either True or Mean"
        
def get_REMs(path,sol_nums,solar_time,time_type):
    res = list()
    for sol_num in sol_nums:
        res.append(get_REM(path,sol_num,solar_time,time_type))
    return res



para = list()
with open(para_file,'r') as f:
    for line in f:
        para.append(str(line.split('"')[1]))
path = para[0]
sol_nums = [int(x) for x in para[1].split(',')]
time_type = para[2]
solar_time = para[3]
output_path = para[4]
name = para[5]

savefilename = output_path+name

res = get_REMs(path,sol_nums,solar_time,time_type)

with open(savefilename, 'w+') as f:
    f.write("Brightness temperatures (in Kelvin) from REM (20 minutes time window)\n")
    f.write("Time type: %s\n" % (time_type+' solar time'))
    f.write("Time: %s\n"%solar_time)
    f.write("Sol\tTemperature\n")
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(sol_nums,res))
print('Done!')

