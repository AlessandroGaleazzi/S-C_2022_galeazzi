# This script contains all the functions and commands to plot the results of the simulations

import numpy as np
import matplotlib.pyplot as plt
import configparser
import argparse

parser = argparse.ArgumentParser(description="Launch one or more simulations.")
parser.add_argument("ConfigFile", nargs="?", default="configuration.ini", help="Select the configuration file.")
parser.add_argument("plots", nargs='+', choices=["plot1", "plot2", "plot3y", "plot3n", "plot4", "plot5n", "plot5y"], \
                     help="Select the desired plot.")

args = parser.parse_args()
chosen_configfile = args.ConfigFile
chosen_plots = args.plots

config = configparser.ConfigParser()
config.read(chosen_configfile)

threshold = float(config.get("specific parameters", "threshold_temperature"))
logging_time = int(config.get("specific parameters", "logging_time"))
duration_in_seconds = int(config.get("specific parameters", "duration_in_seconds"))

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

def threshold_temp_plot():
    """This function plots the temperature evolution of the system and the selected threshold."""
    temperature_threshold = np.load(source1)
    time = np.arange(len(temperature_threshold))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, temperature_threshold, label="System temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature evolution up to threshold", fontsize = 40)
    plt.axhline(y = threshold, color="r", linestyle="-", label="Threshold temperature")
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination1)
    print(f"The plot has been saved as {destination1} in the plots folder.")

def clear_sky_temperature_plot():
    """This function plots the external temperature calculated from the clear-sky model."""
    clear_sky_temperature = np.load(source2)
    time = np.arange(24*3600)
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, clear_sky_temperature, label="External temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="One-day clear-sky temperature", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination2)
    print(f"The plot has been saved as {destination2} in the plots folder.")

def clear_sky_simulation_plot():
    """This function plots the thermal simulation of a system exposed to clear-sky temperatures."""
    clear_sky_simulation = np.load(source3)
    time = np.arange(len(clear_sky_simulation))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, clear_sky_simulation, label="System temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature with clear-sky model", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination3)
    print(f"The plot has been saved as {destination3} in the plots folder.")

def clear_sky_simulation_temperature_plot():
    """This function plots the thermal simulation of a system exposed to clear-sky temperatures and the external one."""
    clear_sky_simulation = np.load(source3)
    time = np.arange(len(clear_sky_simulation))
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, clear_sky_simulation, label="System temperature")
    temperatures_24h = np.load(source2)
    simulation_duration = len(clear_sky_simulation)
    repetitions = simulation_duration // len(temperatures_24h)
    ext_temperature = np.tile(temperatures_24h, repetitions)
    remaining_seconds = simulation_duration - len(ext_temperature)
    if remaining_seconds > 0:
        ext_temperature = np.concatenate((ext_temperature, temperatures_24h[:remaining_seconds]))
    # The following line would be the only test needed for previous 7 lines
    assert len(ext_temperature) == len(clear_sky_simulation)
    plt.plot(time, ext_temperature, label="External temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature with clear-sky model", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination3)
    print(f"The plot has been saved as {destination3} in the plots folder.")

def external_temperature_plot():
    """This function plots the temperatures recorded using a digital thermometer."""
    external_temperature = np.load(source4, allow_pickle=True)
    time = [i * logging_time for i in range(duration_in_seconds // logging_time)]
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, external_temperature, label="External temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="External temperature recording", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination4)
    print(f"The plot has been saved as {destination4} in the plots folder.")

def external_temperature_simulation_plot():
    """This function plots the thermal simulation of a system exposed to recorded temperatures."""
    external_temperature_simulation = np.load(source5)
    time = [i * logging_time for i in range(duration_in_seconds // logging_time)]
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, external_temperature_simulation, label="System temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature simulation from external temperature recording", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination5)
    print(f"The plot has been saved as {destination5} in the plots folder.")

def external_temperature_simulation_with_ext_plot():
    """This function plots the thermal simulation of a system exposed to recorded temperatures."""
    external_temperature_simulation = np.load(source5)
    time = [i * logging_time for i in range(duration_in_seconds // logging_time)]
    f = plt.figure(figsize=(18, 12))
    plt.plot(time, external_temperature_simulation, label="System temperature")
    external_temperature = np.load(source4, allow_pickle=True)
    plt.plot(time, external_temperature, label="External temperature")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature simulation from external temperature recording", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination5)
    print(f"The plot has been saved as {destination5} in the plots folder.")


for plot in chosen_plots:
    if plot == "plot1":
        threshold_temp_plot()
    elif plot == "plot2":
        clear_sky_temperature_plot()
    elif plot == "plot3n":
        clear_sky_simulation_plot()
    elif plot == "plot3y":
        clear_sky_simulation_temperature_plot()
    elif plot == "plot4":
        external_temperature_plot()
    elif plot == "plot5n":
        external_temperature_simulation_plot()
    elif plot == "plot5y": 
        external_temperature_simulation_with_ext_plot()
        