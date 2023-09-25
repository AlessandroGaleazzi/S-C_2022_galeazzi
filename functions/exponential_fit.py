import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def get_seconds(time_str):
    # split in hh, mm, ss
    #exception: if anything but numbers and : is present, raise an exception. same for mm, ss > 60
    #tests: ordinary case + 00:00:00
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

def find_extreme_points(point1, point2, logging_time, df_temp_time):
    #Think about the possible tests and doc

    time1, time2 = point1 * logging_time, point2 * logging_time
    temp1 = df_temp_time.iloc[point1]["Unnamed: 2"]
    temp2 = df_temp_time.iloc[point2]["Unnamed: 2"]
    highlight_points = np.array([[time1, temp1], [time2, temp2]])
    return highlight_points
    
def exponential_func_free_params(t, T0, Teq, tau):
    return Teq +(T0-Teq)*np.exp(-t/tau)

    

"""print("Hello! With this code, you will be able to calculate the time constant of your thermal container and use it to perform simulations. First, write the name of the excel file from which you want to calculate the time constant.")
file_name=input() """
file_name="EFI234105840_20230801164648.xls"

#i have to manage the case in which the file is not found. exception

df_logging_time = pd.read_excel(file_name, usecols=[4],skiprows=9, nrows=1)
logging_time = get_seconds(df_logging_time.iloc[0]["Unnamed: 4"])

df_temp_time = pd.read_excel(file_name, usecols=[0,2], skiprows=25, decimal=',')

temp = np.array(df_temp_time.iloc[1:]["Unnamed: 2"])
time = np.arange(len(temp)) * logging_time

"""print("Great! Now tell me the number of the measurement you want the fit to start from")
#point1=input()"""
point1 = 6626
"""print("Last parameter: the number of the last measurement to be considered for the fit")
#pint2=input()"""
point2 = 7660

#Consider raising an exception if the numbers are beyond the data length

temp_for_fit = np.array(df_temp_time.iloc[point1:point2]["Unnamed: 2"])
time_for_fit = np.arange(len(temp_for_fit)) * logging_time

#temp_vs_time = np.array([time, temp])
#Serve a qualcosa? non lo uso mai nel progetto

highlight_points=find_extreme_points(point1, point2, logging_time, df_temp_time)

"""
plt.plot(time, temp, label="Preliminary check")

for point in highlight_points:
    plt.scatter(point[0], point[1], color="red", label="Boundary of fitting interval")

plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Time constant calculation")
plt.show()
"""
#check for the correctness of the fitting interval

params, covariance = curve_fit(exponential_func_free_params, time_for_fit, temp_for_fit)

T0, Teq, tau = params

temp_from_fitting = exponential_func_free_params(time_for_fit, T0, Teq, tau)

#remember to separate the plotting from the analysis. do it before handing the project (should take not a lot)

plt.scatter(time_for_fit, temp_for_fit, label='Experimental data', color='blue', marker='o', s=20)
plt.plot(time_for_fit, temp_from_fitting, 'r', label=f'Exponential fit')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.title('Time constant calculation')
plt.legend()
plt.grid()
plt.show()

print(f'The exponential fit calculated tau={tau:.2f}s')