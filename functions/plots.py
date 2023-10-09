import numpy as np
import matplotlib.pyplot as plt
import configparser

config = configparser.ConfigParser()
config.read("configuration.ini")

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
    command = input("Do you want to also add the external temperature from which the simulation is performed to the plot? y/n\n")
    if command == "y":
        clear_sky_temperature = np.load(source2)
        plt.plot(time, clear_sky_temperature, label="External temperature")
    elif command == "n":
        pass
    else:
        print("Invalid command")
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
    command = input("Do you want to also add the external temperature from which the simulation is performed to the plot y/n\n")
    if command == "y":
        external_temperature = np.load(source4, allow_pickle=True)
        plt.plot(time, external_temperature, label="External temperature")
    elif command == "n":
        pass
    else:
        print("Invalid command")
    plt.xlabel("Time (s)", fontsize=30)
    plt.xticks(fontsize=20)
    plt.ylabel("Temperature (°C)", fontsize=30)
    plt.yticks(fontsize=20)
    plt.title(label="Temperature simulation from external temperature recording", fontsize = 40)
    plt.legend(fontsize=20)
    plt.axis("tight")
    f.savefig(destination5)
    print(f"The plot has been saved as {destination5} in the plots folder.")


command = input("Select the plot that you want to perform, using the following numbers:\n"
                "Temperature evolution up to threshold -> 1\nClear-sky temperature -> 2\n"
                "Simulation with clear-sky temperature -> 3\nExternal temperature recording -> 4\n"
                "Simulation with external temperature recording -> 5\n")
if command == "1":
    threshold_temp_plot()
elif command == "2":
    clear_sky_temperature_plot()
elif command == "3":
    clear_sky_simulation_plot()
elif command == "4":
    external_temperature_plot()
elif command == "5":
    external_temperature_simulation_plot()
else:
    print("Invalid command")
