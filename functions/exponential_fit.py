import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# HACK


def get_seconds(time_str):
    """This function transforms a time in format hh:mm:ss into a time measured in seconds.

    Parameters:
        time_str : time in format hh:mm:ss.

    Returns:
        Value of the input time in seconds.

    Raise:
        ValueError if the input string contains anything but digits and colons."""
    for char in time_str:
        if not char.isdigit() and char != ':':
            raise ValueError(
                "Invalid character in time format. Only digits and colons are allowed.")
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


def find_extreme_points(point1, point2, logging_time, df_temp_time):
    """This function returns the two points (begin and end) to be used to fit data.

    Parameters:
        point1 : measurement number from which the fit starts.
        point2 : last measurement number fro the fit.
        logging_time : time between measurements.
        df_temp_time : dataframe from which temperatures and time are extracted.

    Returns:
        2x2 array containing begin and end of the fitting interval."""
    time1, time2 = point1 * \
        logging_time, point2 * \
        logging_time
    temp1 = df_temp_time.iloc[point1]["Unnamed: 2"]
    temp2 = df_temp_time.iloc[point2]["Unnamed: 2"]
    highlight_points = np.array(
        [[time1, temp1], [time2, temp2]])
    return highlight_points


def exponential_func(t, T0, Teq, tau):
    """This function represents the time evolution of a system placed in a thermal bath.

    Parameters:
        t : time (s) after which I want to calculate the temperature of the system.
        t0 : temperature of the system at t = 0
        teq : temperature of the thermal bath
        tau : time constant of the system (see documentation to better understand)

    Returns:
        Value of the system temperature after t seconds."""
    return Teq + (T0-Teq)*np.exp(-t/tau)


# Input part (skipped at the moment, all parameters are already set). TODO Use a config file to perform the fit.


"""
file_name = input("Hello! With this code, you will be able to calculate the time constant of your thermal container and use it to perform simulations. First, write the name of the excel file from which you want to calculate the time constant.")
"""
file_name = "EFI234105840_20230801164648.xls"
if not file_name.endswith(".xls"):
    raise ValueError(f"The file '{file_name}' is not a valid Excel file.")

df_logging_time = pd.read_excel(
    file_name, usecols=[4], skiprows=9, nrows=1)
logging_time = get_seconds(
    df_logging_time.iloc[0]["Unnamed: 4"])

df_temp_time = pd.read_excel(
    file_name, usecols=[0, 2], skiprows=25, decimal=',')

temp = np.array(
    df_temp_time.iloc[1:]["Unnamed: 2"])
time = np.arange(len(
    temp)) * logging_time

# point1=input("Great! Now tell me the number of the measurement you want the fit to start from")
point1 = 6626

# point2=input("Last parameter: the number of the last measurement to be considered for the fit")
point2 = 7660

# Consider raising an exception if the numbers are beyond the data length

highlight_points = find_extreme_points(
    point1, point2, logging_time, df_temp_time)
temp_for_fit = np.array(
    df_temp_time.iloc[point1:point2]["Unnamed: 2"])
time_for_fit = np.arange(len(
    temp_for_fit)) * logging_time


# The following step of the fit is meant to let the user check that the chosen fitting interval is correct by plotting it
"""
plt.plot(time, temp, label="Preliminary check")

for point in highlight_points:
    plt.scatter(point[0], point[1], color="red", label="Boundary of fitting interval")

plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Time constant calculation")
plt.show()
"""

# Acutal fitting

params, covariance = curve_fit(
    exponential_func, time_for_fit, temp_for_fit)

T0, Teq, tau = params

temp_from_fitting = exponential_func(
    time_for_fit, T0, Teq, tau)

# remember to separate the plotting from the analysis. do it before handing the project (should take not a lot)


# Example of exponential fitting and comparison with experimental data
"""
plt.scatter(time_for_fit, temp_for_fit, label='Experimental data', color='blue', marker='o', s=20)
plt.plot(time_for_fit, temp_from_fitting, 'r', label=f'Exponential fit')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.title('Time constant calculation')
plt.legend()
plt.grid()
plt.show()

print(f'The exponential fit calculated tau={tau:.2f}s')
"""
