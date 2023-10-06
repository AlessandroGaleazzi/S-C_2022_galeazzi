import simulation as sim
import numpy as np
import sys
from sys import argv
import configparser

config = configparser.ConfigParser()
config.read("configuration.ini")

tau = config.get("fundamental parameters", "tau")
initial_t0 = config.get('fundamental parameters', 'initial_t0')

teq = config.get("specific parameters", "teq")
threshold_temperature = config.get("specific parameters", "threshold_temperature")
starting_time = config.get("specific parameters", "starting_time")
duration = config.get("specific parameters", "duration")
file_name = config.get("specific parameters", "file_name")

Tmin = config.get("clear-sky_simulation", "Tmin")
Tmax = config.get("clear-sky_simulation", "Tmax")
sunrise_time = config.get("clear-sky_simulation", "sunrise_time")
sunset_time = config.get("clear-sky_simulation", "sunset_time")
a = config.get("clear-sky_simulation", "a")
b = config.get("clear-sky_simulation", "b")
c = config.get("clear-sky_simulation", "c")

print(Tmin)
"""
command = input("Select the simulation that you want to perform ( func1, func2, func3)")
if command == "func1":
    sim.funzione1()
elif command == "func2":
    sim.funzione2()
elif command == "func3":
    sim.funzione3()
else:
    print("Invalid command")
"""