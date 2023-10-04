import numpy as np
import pandas as pd


class TemperatureError(Exception):
    # is this the way I should write my own exceptions? Expand this to all the cases in the functions where an exception should be raised. TO DO!!!
    pass


# The next three functions were written to be used inside the functions that actually perform the simulations

def get_seconds(time_str):
    # This function transforms a time in format hh:mm:ss into seconds
    # exception: if anything but numbers and : is present, raise an exception. same for mm, ss > 60

    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


def exponential_func(t, t0, teq, tau):
    # This function represent the time evolution of a system in a thermal bath, as described in the theoretical part of the documentation. (STILL TO WRITE)
    return teq + (t0-teq)*np.exp(-t/tau)


def every_second_exponential_func(t0, teq, tau):
    # This function represent the time evolution of a system in a thermal bath, calculated every second
    return teq + (t0-teq)*np.exp(-1/tau)


# The next four functions are used to produce a simulation of external temperatures in a day, according to the clear-sky model

def before_sunrise_temperature_function(Tmin, Tsunset, sunset_time, b, n1, time):
    # function for temperature calculation during daytime

    return Tmin + (Tsunset-Tmin) * np.exp(- b * (time - get_seconds(sunset_time) + 24*3600) / n1) - (time - get_seconds(sunset_time) + 24*3600) / n1 * np.exp(- b)


def daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, time):
    # function for temperature calculation between sunrise and sunset

    return Tmin + (Tmax - Tmin) * np.sin(np.pi * (time) / (get_seconds(sunset_time) - get_seconds(sunrise_time) + 2 * (a - c) * 3600))


def after_sunset_temperature_function(Tmin, Tsunset, b, n2, time):
    # function for temperature calculation after sunset

    return Tmin + (Tsunset - Tmin) * np.exp(- b * (time) / n2) - (time) / n2 * np.exp(- b)


def one_day_temperature_calculation(Tmin, Tmax, sunrise_time, sunset_time, a=2.71, b=3.14, c=0.75):
    # Function that calculates how the external temperature varies in one day, given certain parameters.
    all_day_temperatures = []

    # Determine initial parameters from input values
    Tsunset = daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, int(get_seconds(
        sunset_time) - get_seconds(sunrise_time) - c * 3600))
    n1 = get_seconds(sunrise_time) - \
        get_seconds(sunset_time) + (c + 24) * 3600
    # n1 and n2 are the same, since they are meant for simulations in which the parameters change as days go by. Maybe I'll need it later
    n2 = get_seconds(sunrise_time) - \
        get_seconds(sunset_time) + (c + 24) * 3600

    for t in range(int(get_seconds(sunrise_time) + c * 3600)):
        all_day_temperatures.append(before_sunrise_temperature_function(
            Tmin, Tsunset, sunset_time, b, n1, t))
    for t in range(int(get_seconds(sunset_time) - get_seconds(sunrise_time) - c * 3600)):
        all_day_temperatures.append(daytime_temperature_function(
            Tmin, Tmax, sunrise_time, sunset_time, a, c, t))
    for t in range(24 * 3600 - get_seconds(sunset_time)):
        all_day_temperatures.append(
            after_sunset_temperature_function(Tmin, Tsunset, b, n2, t))
    return all_day_temperatures


# Next functions are used to perform the actual simulations, given that all input parameters are externally provided or simulated using previous functions

def time_to_threshold_temp(initial_t0, teq, tau, threshold_temp, interval_time):
    # This function calculate the time needed to reach a certain threshold temperature, given the time between measurements and all the system and environmental parameters

    if ((initial_t0 < teq) and (threshold_temp > teq)) or ((initial_t0 > teq) and (threshold_temp < teq)):
        raise TemperatureError(
            "The threshold temperature is beyond equilibrium temperature, therefore it will never be reached. Check again your parameters.")

    if threshold_temp == teq:
        raise TemperatureError(
            "The threshold temperature that was set is equal to the external temperature, meaning that it will be reached asimptotically. ")

    counter = 1
    time, temp = interval_time, initial_t0

    if threshold_temp < teq:
        while (temp < threshold_temp):
            temp = exponential_func(time, initial_t0, teq, tau)
            counter += 1
            time = counter * interval_time
    else:
        while (temp > threshold_temp):
            temp = exponential_func(time, initial_t0, teq, tau)
            counter += 1
            time = counter * interval_time
    return time  # TODO Improve the format, maybe with a message in output


def temperature_evolution_up_to_threshold(initial_t0, teq, tau, threshold_temp):
    # This function simulates the temperature evolution as the system reaches a certain threshold temperature, given the time between measurements and all the system and environmental parameters

    if ((initial_t0 < teq) and (threshold_temp > teq)) or ((initial_t0 > teq) and (threshold_temp < teq)):
        raise TemperatureError(
            "The threshold temperature is beyond equilibrium temperature, therefore it will never be reached. Check again your parameters.")

    if threshold_temp == teq:
        raise TemperatureError(
            "The threshold temperature that was set is equal to the external temperature, meaning that it will be reached asimptotically. ")

    system_temperature = []
    system_temperature.append(initial_t0)
    t0, temp = initial_t0, initial_t0
    counter = 0

    if threshold_temp < teq:
        while (temp < threshold_temp):
            temp = every_second_exponential_func(t0, teq, tau)
            system_temperature.append(temp)
            t0 = system_temperature[counter + 1]
            counter += 1
    else:
        while (temp > threshold_temp):
            temp = every_second_exponential_func(t0, teq, tau)
            system_temperature.append(temp)
            t0 = system_temperature[counter + 1]
            counter += 1
    return system_temperature


def temperature_simulation_with_clear_sky_temperature(starting_time, initial_T0, tau, duration, one_day_external_temperature):
    # This functions simulates the thermal evolution of a system according to an external temperature simulated according to the clear-sky day model.

    external_temperature = []
    system_temperature = []
    duration_in_seconds = get_seconds(duration)
    starting_time_in_seconds = get_seconds(starting_time)

    # The number of days needed is calculated in excess so that the external temperatures are available throughout the duration of the simulation
    number_of_days = duration_in_seconds // (24 * 3600) + 1
    external_temperature = one_day_external_temperature * number_of_days

    system_temperature.append(initial_T0)
    t0 = initial_T0
    for i in range(duration_in_seconds - 1):
        teq = external_temperature[starting_time_in_seconds + i]
        system_temperature.append(every_second_exponential_func(t0, teq, tau))
        t0 = system_temperature[i + 1]
    return system_temperature


def get_temperatures_from_file(file_name):
    # This function takes the temperatures recorded by a digital thermometer, toghether with its logging_time and the duration of the recording

    df_logging_time = pd.read_excel(
        file_name, usecols=[4], skiprows=9, nrows=1)
    logging_time = get_seconds(
        df_logging_time.iloc[0]["Unnamed: 4"])

    df_temp_time = pd.read_excel(
        file_name, usecols=[0, 2], skiprows=25, decimal=',')
    temperatures = np.array(
        df_temp_time.iloc[1:]["Unnamed: 2"])

    duration_in_seconds = len(temperatures) * logging_time

    external_temperature_tuple = [
        temperatures, logging_time, duration_in_seconds]

    return external_temperature_tuple


def temperature_simulation_with_variable_ext_temperature(initial_T0, tau, external_temperature_tuple):
    # This function works just like temperature_simulation_with_clear_sky_temperature, but takes a tuple containing external temperatures, logging time and duration of the measurement as input
    system_temperature = []
    external_temperature, logging_time, duration_in_seconds = external_temperature_tuple

    system_temperature.append(initial_T0)
    t0 = initial_T0
    # Check that this range is still ok in this function
    for i in range(duration_in_seconds//logging_time - 1):
        teq = external_temperature[i]
        system_temperature.append(exponential_func(logging_time, t0, teq, tau))
        t0 = system_temperature[i + 1]
    return system_temperature


# Example of use of time_to_threshold_temperature
"""
try:
    print(time_to_threshold_temp(-18, 27, 1020, 25, 10))
except TemperatureError as e:
    print(f"Error: {e}")
"""


# Example of external temperature simulation
"""
temperatures_in_one_day = one_day_temperature_calculation(Tmin = 13, Tmax = 25, sunrise_time="6:52:00", sunset_time="19:26:00")
seconds_in_one_day = np.arange(24 * 3600)
plt.plot(seconds_in_one_day, temperatures_in_one_day, label="Preliminary check")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("24 hours temperature variation")
plt.show()
"""

# Example of use and plotting of temperature_simulation_with_variable_ext_temperature
"""
temperatures_in_one_day = one_day_temperature_calculation(Tmin = 13, Tmax = 25, sunrise_time="6:52:00", sunset_time="19:26:00")
system_temperature = temperature_simulation_with_variable_ext_temperature("00:00:00", -18, 10000, "24:00:00", temperatures_in_one_day)
seconds_in_one_day = np.arange(24 * 3600)
plt.plot(seconds_in_one_day, temperatures_in_one_day, system_temperature, label="Preliminary check")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("24 hours temperature variation")
plt.show()
"""
