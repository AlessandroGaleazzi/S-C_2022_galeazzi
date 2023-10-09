import numpy as np
import matplotlib.pyplot as plt
import configparser

config = configparser.ConfigParser()
config.read("configuration.ini")

logging_time = config.get("specific parameters", "logging_time")
duration_in_seconds = config.get("specific parameters", "duration_in_seconds")

source1 = config.get("paths", "temperature_threshold")
source2 = config.get("paths", "clear-sky_temperature")
source3 = config.get("paths", "clear-sky_simulation")
source4 = config.get("paths", "external_temperature")
source5 = config.get("paths", "ext_temperature_simulation")

destination1 = config.get("paths", "threshold_plot")
destination2 = config.get("paths", "clear_sky_temperature_plot")
destination3 = config.get("paths", "clear_sky_simulation_plot")
destination4 = config.get("paths", "external_temperature_plot")
destination5 = config.get("paths", "ext_temperature_simulation_plot")


# TODO manage the case where the file npy is not found with an exception

# TODO write the docstrings

def threshold_temp_plot():
    temperature_threshold = np.load(source1)
    time = np.arange(len(temperature_threshold))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, temperature_threshold)
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature evolution up to threshold", fontsize = 40)
    plt.axis('tight')
    f.savefig(destination1)
    print(f"The plot has been saved as {destination1} in the plots folder.")

def clear_sky_temperature_plot():
    clear_sky_temp = np.load(source2)
    time = np.arange(24*3600)
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, clear_sky_temp)
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="One-day clear-sky temperature", fontsize = 40)
    plt.axis('tight')
    f.savefig(destination2)
    print(f"The plot has been saved as {destination2} in the plots folder.")

def clear_sky_simulation_plot():
    clear_sky_sim = np.load(source3)
    time = np.arange(len(clear_sky_sim))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, clear_sky_sim)
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature with clear-sky model", fontsize = 40)
    plt.axis('tight')
    f.savefig(destination3)
    print(f"The plot has been saved as {destination3} in the plots folder.")

def external_temperature_plot():
    external_temperature = np.load(source4, allow_pickle=True) 
    time = np.arange(len(external_temperature))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, external_temperature)
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="External temperature recording", fontsize = 40)
    plt.axis('tight')
    f.savefig(destination4)
    print(f"The plot has been saved as {destination4} in the plots folder.")

def external_temperature_simulation_plot():
    external_temperature_simulation = np.load(source5)
    time = np.arange(len(external_temperature_simulation))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, external_temperature_simulation)
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature simulation from external temperature recording", fontsize = 40)
    plt.axis('tight')
    f.savefig(destination5)
    print(f"The plot has been saved as {destination5} in the plots folder.")


# Example of use of the plotting functions
"""
threshold_temp_plot()
clear_sky_temperature_plot()
clear_sky_simulation_plot()
external_temperature_plot()
external_temperature_simulation_plot()
"""

# Implement the control of the plotting step as follows:
"""
command = input("Select the kind of lot that you want to perform (time_threshold, temp_threshold, clear-sky_temp, ext_temp_import, ext_temp_simulation)\n")
if command == "time_threshold":

elif:

else:
    print("Invalid command")
"""