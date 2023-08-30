import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_seconds(time_str):
    # split in hh, mm, ss
    #exception: if anything but numbers and : is present, raise an exception. same for mm, ss > 60
    #tests: ordinary case + 00:00:00
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

def find_extreme_points(point1, point2, logging_time, df_temp_time):
    time1, time2 = point1 * logging_time, point2 * logging_time
    temp1 = df_temp_time.iloc[point1]["Unnamed: 2"]
    temp2 = df_temp_time.iloc[point2]["Unnamed: 2"]
    highlight_points = np.array([[time1, temp1], [time2, temp2]])
    return highlight_points
    
    

"""print("Hello! With this code, you will be able to calculate the time constant of your thermal container and use it to perform simulations. First, write the name of the excel file from which you want to calculate the time constant.")
file_name=input() #i have to manage the case in which the file is not found. do it! maybe using a while(true)?"""
file_name="EFI234105840_20230801164648.xls"

df_logging_time = pd.read_excel(file_name, usecols=[4],skiprows=9, nrows=1)
logging_time = get_seconds(df_logging_time.iloc[0]["Unnamed: 4"])

df_temp_time = pd.read_excel(file_name, usecols=[0,2], skiprows=25, decimal=',')

temp = np.array(df_temp_time.iloc[1:]["Unnamed: 2"])
time = np.arange(len(temp)) * logging_time

"""print("Great! Now tell me the number of the measurement you want the fit to start from")
#t_initial=input()"""
point1 = 6626
"""print("Last parameter: the number of the last measurement to be considered for the fit")
#t_final=input()"""
point2 = 7660

#Consider raising an exception if the numbers are beyond the data length

temp_for_fit = np.array(df_temp_time.iloc[point1:point2]["Unnamed: 2"])
time_for_fit = np.arange(len(temp)) * logging_time
temp_vs_time = np.array([time, temp])
highlight_points=find_extreme_points(point1, point2, logging_time, df_temp_time)
#print(highlight_points)

#print(temp_vs_time)

plt.plot(time, temp, label="Preliminary check")

for point in highlight_points:
    plt.scatter(point[0], point[1], color="red", label="Boundary of fitting interval")

plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Time constant calculation")
plt.show()
