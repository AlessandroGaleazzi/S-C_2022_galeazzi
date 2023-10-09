import simulation as sim
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read("configuration.ini")

tau = float(config.get("fundamental parameters", "tau"))
initial_t0 = float(config.get('fundamental parameters', 'initial_t0'))
teq = float(config.get("specific parameters", "teq"))
threshold_temperature = float(config.get("specific parameters", "threshold_temperature"))
starting_time = str(config.get("specific parameters", "starting_time"))
duration = str(config.get("specific parameters", "duration"))
file_name = config.get("specific parameters", "file_name")
logging_time = int(config.get("specific parameters", "logging_time"))
duration_in_seconds = int(config.get("specific parameters", "duration_in_seconds"))


Tmin = float(config.get("clear-sky simulation", "Tmin"))
Tmax = float(config.get("clear-sky simulation", "Tmax"))
sunrise_time = config.get("clear-sky simulation", "sunrise_time")
sunset_time = config.get("clear-sky simulation", "sunset_time")
a = float(config.get("clear-sky simulation", "a"))
b = float(config.get("clear-sky simulation", "b"))
c = float(config.get("clear-sky simulation", "c"))


destination1 = config.get("paths", "temperature_threshold")
destination2 = config.get("paths", "clear-sky_temperature")
destination3 = config.get("paths", "clear-sky_simulation")
destination4 = config.get("paths", "external_temperature")
destination5 = config.get("paths", "ext_temperature_simulation")

command = input("Select the simulation that you want to perform, using the following numbers:\n"
                "Time to threshold -> 1\nTemperature evolution up to threshold -> 2\nClear-sky temperature -> 3\n"
                "Simulation with clear-sky temperature -> 4\nImport of an external temperature recording -> 5\n"
                "Simulation with external temperature recording -> 6\n")
if command == "1":
    time = sim.time_to_threshold_temp(initial_t0, teq, tau, threshold_temperature)
    print(f"The selected threshold will be reached in {time} seconds.\n")
elif command == "2":
    threshold_temperature_array = sim.temperature_evolution_up_to_threshold(initial_t0, teq, tau, threshold_temperature)
    np.save(destination1, threshold_temperature_array)
    print(f"The temperature evolution of the system up to the selected threshold has been saved in {destination1}\n")
elif command == "3":
    clear_sky_temperature = sim.one_day_temperature_calculation(Tmin, Tmax, sunrise_time, sunset_time, a, b, c)
    np.save(destination2, clear_sky_temperature)
    print(f"The clear-sky external temperatures have been saved in {destination2}\n")
elif command == "4":
    one_day_external_temperature = np.load(destination2)
    clear_sky_simulation = sim.temperature_simulation_with_clear_sky_temperature(starting_time, initial_t0, tau, duration, one_day_external_temperature)
    np.save(destination3, clear_sky_simulation)
    print(f"The result of the simulation with clear-day temperature from {destination2} has been saved in {destination3}\n")
elif command == "5":
    external_temperature_tuple = sim.get_temperatures_from_file(file_name)
    np.save(destination4, external_temperature_tuple[0])
    config.set("specific parameters", "logging_time", str(external_temperature_tuple[1]))
    config.set("specific parameters", "duration_in_seconds", str(external_temperature_tuple[2]))
    print(f"The temperature recording has been saved in {destination4} and the specific parameters of the configuration file have been updated\n")
    with open("configuration.ini", 'w') as config_file:
            config.write(config_file)
elif command == "6":
    external_temperature_tuple = ((np.load(destination4, allow_pickle=True), logging_time, duration_in_seconds))
    ext_temp_simulation = sim.temperature_simulation_with_variable_ext_temperature(initial_t0, tau, external_temperature_tuple)
    np.save(destination5, ext_temp_simulation)
    print(f"The result of the simulation with external temperatures from {destination4} has been saved in {destination5}\n")
else:
    print("Invalid command")