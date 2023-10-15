import simulation as sim
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import configparser

config = configparser.ConfigParser()
config.read("configuration.ini")

file_name = config.get("exponential fit", "file_name")
point1 = int(config.get("exponential fit", "point1"))
point2 = int(config.get("exponential fit", "point2"))
df_temp_time = pd.read_excel(
    file_name, usecols=[0, 2], skiprows=25, decimal=',')

# Get 2 out of 3 parameters calculated by get_temperatures_from_file
file_tuple = sim.get_temperatures_from_file(file_name)
temperatures, logging_time = file_tuple[0], file_tuple[1]
time = np.arange(len(
    temperatures)) * logging_time

# Save the temperatures needed for the fit

highlight_points = sim.find_extreme_points(
    point1, point2, logging_time, df_temp_time)
temperatures_for_fit = np.array(
    df_temp_time.iloc[point1:point2]["Unnamed: 2"])
time_for_fit = np.arange(len(
    temperatures_for_fit)) * logging_time


# The following step of the fit is meant to let the user check that the chosen fitting interval is correct by plotting it

plt.plot(time, temperatures, label="Preliminary check")
for point in highlight_points:
    plt.scatter(point[0], point[1], color="red", label="Boundary of fitting interval")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Time constant calculation")
plt.show()
command = input("This is the fitting interval that was selected from the exponential fit.\n"
"Type y if you want to go on with the fit, otherwise type n to stop the process and change the parameters.\n")


if command == "y":
    # Actual fitting

    params, covariance = curve_fit(
        sim.exponential_func, time_for_fit, temperatures_for_fit)

    T0, Teq, tau = params

    temperatures_from_fitting = sim.exponential_func(
        time_for_fit, T0, Teq, tau)


    # Exponential fit and comparison with experimental data
    
    plt.scatter(time_for_fit, temperatures_for_fit, label='Experimental data', color='blue', marker='o', s=20)
    plt.plot(time_for_fit, temperatures_from_fitting, 'r', label="Exponential fit")
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Time constant calculation')
    plt.legend()
    plt.grid()
    plt.show()
    print(f"The exponential fit calculated tau={tau:.2f}s")
    
    command = input("Type y if you want to set this value of the tau parameter in the configuration file, otherwise type any other character\n")
    if command == "y":
        tau_rounded = round(tau, 2)
        config.set("fundamental parameters", "tau", str(tau_rounded))
        print(f"The tau parameter calculated from {file_name} has ben saved in the configuration file\n")
        with open("configuration.ini", 'w') as config_file:
            config.write(config_file)
    else:
        print("End of the fitting process")

elif command == "n":
    print("The determination of the tau parameter has been stopped\n")
else:
    print("Invalid command")