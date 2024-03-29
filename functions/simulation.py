# This script contains all the functions used in the simulations

import numpy as np
import pandas as pd


# The following function is used to prepare the final graph for the exponential fitting

def find_extreme_points(point1, point2, logging_time, df_temp_time):
    """This function returns the two points (begin and end) to be used to fit data.

    Parameters:
        point1 : excel cell containing the measurement number from which the fit starts.
        point2 : excel cell containing the last measurement number for the fit.
        logging_time : excel cell containing the time interval between measurements.
        df_temp_time : dataframe derived from excel from which temperatures and time are extracted.

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


# The next three functions are used inside the functions that actually perform the simulations

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


def exponential_func(t, t0, teq, tau):
    """This function represents the time evolution of a system placed in a thermal bath.

    Parameters:
        t : time (s) after which I want to calculate the temperature of the system.
        t0 : temperature of the system at t = 0
        teq : temperature of the thermal bath
        tau : time constant of the system (see documentation to better understand)

    Returns:
        Value of the system temperature after t seconds."""
    return teq + (t0-teq)*np.exp(-t/tau)


def every_second_exponential_func(t0, teq, tau):
    """This function is the same as exponential_func, but with t set to 1.

    Parameters:
        t0 : temperature of the system at t = 0
        teq : temperature of the thermal bath
        tau : time constant of the system (see documentation to better understand)

    Returns:
        Value of the system temperature after one second."""
    return teq + (t0-teq)*np.exp(-1/tau)


# Next four functions produce a simulation of external temperature according to the clear-sky model

def before_sunrise_temperature_function(Tmin, Tsunset, sunset_time, b, n1, time):
    """This function calculates the external temperature before sunrise.

    Parameters:
        Tmin : minimum temperature of the day.
        Tsunset : temperature at sunset.
        sunset_time : sunset time (string with format "hh:mm:ss").
        b : night-time temperature decay coefficient.
        n1 : corrected night length.
        time : time since midnight (int, in seconds).

    Returns:
        Value of the external temperature before sunrise."""
    return Tmin + (Tsunset-Tmin) * np.exp(- b * (time - get_seconds(sunset_time) + 24*3600) / n1) \
          - (time - get_seconds(sunset_time) + 24*3600) / n1 * np.exp(- b)


def daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, time):
    """This function calculates the external temperature between sunrise and sunset.

    Parameters:
        Tmin : minimum temperature of the day.
        Tmax : maximum temperature of the day.
        sunrise_time : sunrise time (string with format "hh:mm:ss").
        sunset_time : sunset time (string with format "hh:mm:ss").
        a : lag coefficient for Tmin from noon.
        c : time lag fro Tmin from sunrise.
        time : time since midnight (int, in seconds).

    Returns:
        Value of the external temperature between sunrise and sunset."""
    return Tmin + (Tmax - Tmin) * np.sin(np.pi * (time) / \
            (get_seconds(sunset_time) - get_seconds(sunrise_time) + 2 * (a - c) * 3600))


def after_sunset_temperature_function(Tmin, Tsunset, b, n1, time):
    """This function calculates the external temperature after sunset.

    Parameters:
        Tmin : minimum temperature of the day.
        Tsunset : temperature at sunset.
        b : night-time temperature decay coefficient.
        n1 : corrected night length.
        time : time since midnight (int, in seconds).

    Returns:
        Value of the external temperature after sunset."""
    return Tmin + (Tsunset - Tmin) * np.exp(- b * (time) / n1) - (time) / n1 * np.exp(- b)


def one_day_temperature_calculation(Tmin, Tmax, sunrise_time, sunset_time, a, b, c):
    """This function calculates the external temperature in every second of a day (clear-sky model).

    Parameters:
        Tmin : minimum temperature of the day.
        Tmax : maximum temperature of the day.
        sunrise_time : sunrise time (string with format "hh:mm:ss").
        sunset_time : sunset time (string with format "hh:mm:ss").
        a : lag coefficient for Tmin from noon.
        b : night-time temperature decay coefficient.
        c : time lag fro Tmin from sunrise.

    Returns:
        List contanining a value of temperature per every second of the day."""
    all_day_temperatures = []

    # Determine initial parameters from input values
    Tsunset = daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, \
        int(get_seconds(sunset_time) - get_seconds(sunrise_time) - c * 3600))
    n1 = get_seconds(sunrise_time) - \
        get_seconds(sunset_time) + (c + 24) * 3600

    for t in range(int(get_seconds(sunrise_time) + c * 3600)):
        all_day_temperatures.append(before_sunrise_temperature_function(
            Tmin, Tsunset, sunset_time, b, n1, t))
    for t in range(int(get_seconds(sunset_time) - get_seconds(sunrise_time) - c * 3600)):
        all_day_temperatures.append(daytime_temperature_function(
            Tmin, Tmax, sunrise_time, sunset_time, a, c, t))
    for t in range(24 * 3600 - get_seconds(sunset_time)):
        all_day_temperatures.append(
            after_sunset_temperature_function(Tmin, Tsunset, b, n1, t))
    return all_day_temperatures


# Next functions perform the actual simulations, given that all input parameters are provided

def time_to_threshold_temp(initial_t0, teq, tau, threshold_temp):
    """This function calculate the time needed to reach a certain threshold temperature.

    Parameters:
        initial_t0 : initial temperature of the system.
        teq : (constant) temperature of the thermal bath.
        tau : time constant of the system.
        threshold_temp : threshold temperature.

    Returns:
        Value of time after which the temperature of the system reaches the threshold temperature.

    Raise:
        ValueError if the threshold temperature is beyond or equal to teq."""
    if ((initial_t0 < teq) and (threshold_temp > teq)) or \
        ((initial_t0 > teq) and (threshold_temp < teq)):
        raise ValueError(
            "The threshold temperature is beyond equilibrium temperature, \
        therefore it will never be reached. Check again your parameters.")

    if threshold_temp == teq:
        raise ValueError(
            "The threshold temperature that was set is equal to the \
        external temperature, meaning that it will be reached asimptotically.")

    time, temp = 1, initial_t0

    while (temp < threshold_temp) if threshold_temp < teq else (temp > threshold_temp):
        temp = exponential_func(time, initial_t0, teq, tau)
        time += 1

    # Old version of the code 
    """if threshold_temp < teq:
        while (temp < threshold_temp):
            temp = exponential_func(time, initial_t0, teq, tau)
            time += 1
    else:
        while (temp > threshold_temp):
            temp = exponential_func(time, initial_t0, teq, tau)
            time += 1"""
    return time


def temperature_evolution_up_to_threshold(initial_t0, teq, tau, threshold_temp):
    """This function simulates the temperature evolution of the system up to a threshold temperature.

    Parameters:
        initial_t0 : initial temperature of the system.
        teq : (constant) temperature of the thermal bath.
        tau : time constant of the system.
        threshold_temp : threshold temperature.

    Returns:
        List contanining a value of system temperature until threshold is reached.

    Raise:
        ValueError if the threshold temperature is beyond or equal to teq."""
    if ((initial_t0 < teq) and (threshold_temp > teq)) or \
        ((initial_t0 > teq) and (threshold_temp < teq)):
        raise ValueError(
            "The threshold temperature is beyond equilibrium temperature, \
        therefore it will never be reached. Check again your parameters.")

    if threshold_temp == teq:
        raise ValueError(
            "The threshold temperature that was set is equal to the \
        external temperature, meaning that it will be reached asimptotically.")

    system_temperature = []
    system_temperature.append(initial_t0)
    t0, temp = initial_t0, initial_t0
    counter = 0

    while True:
        temp = every_second_exponential_func(t0, teq, tau)
        system_temperature.append(temp)
        t0 = system_temperature[counter + 1]
        counter += 1
        if (temp < threshold_temp and system_temperature[counter - 1] >= threshold_temp) or \
            (temp > threshold_temp and system_temperature[counter - 1] <= threshold_temp):
            break
    
    # Old version of the code 
    """if (temp < threshold_temp and system_temperature[counter - 1] >= threshold_temp) or \
            (temp > threshold_temp and system_temperature[counter - 1] <= threshold_temp):
        break
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
            counter += 1"""
    return system_temperature


def temperature_simulation_with_clear_sky_temperature(starting_time, initial_t0, tau, \
                                                      duration, one_day_external_temperature):
    """This functions simulates the system evolution using external clear-sky day temperatures.

    Parameters:
        starting_time : daytime when the simulation starts (string with format "hh:mm:ss").
        initial_t0 : initial temperature of the system.
        tau : time constant of the system.
        duration : duration of the simulation (string with format "hh:mm:ss").
        one_day_external_temperature : list containing external temperatures
            (generated by temperature_simulation_with_clear_sky_temperature).

    Returns:
        List with the values of the system temperature for every second of the simulation."""
    external_temperature = []
    system_temperature = []
    duration_in_seconds = get_seconds(duration)
    starting_time_in_seconds = get_seconds(starting_time)

    # The number of days needed is calculated in excess so that \
    # the external temperatures are available as long as needed
    number_of_days = duration_in_seconds // (24 * 3600) + 1
    for _ in range(number_of_days):
        external_temperature.extend(one_day_external_temperature)
    system_temperature.append(initial_t0)
    t0 = initial_t0
    for i in range(duration_in_seconds - 1):
        teq = external_temperature[starting_time_in_seconds + i]
        system_temperature.append(every_second_exponential_func(t0, teq, tau))
        t0 = system_temperature[i + 1]
    return system_temperature

# Next functions manage the simulation in case the external temperature is a recording

def get_temperatures_from_file(file_name):
    """This function imports the temperature recording of a digital thermometer and its main features.

    Parameters:
        file_name : name of the file where the recording is saved (excel file).

    Returns:
        Tuple with temperature recording, logging time and measurement duration.

    Raise:
        ValueError if the input file is not an excel file."""
    if not file_name.endswith(".xls"):
        raise ValueError(f"The file '{file_name}' is not a valid Excel file.")

    df_logging_time = pd.read_excel(
        file_name, usecols=[4], skiprows=9, nrows=1)
    logging_time = get_seconds(
        df_logging_time.iloc[0]["Unnamed: 4"])

    df_temp_time = pd.read_excel(
        file_name, usecols=[0, 2], skiprows=25, decimal=',')
    temperatures = np.array(
        df_temp_time.iloc[1:]["Unnamed: 2"])

    duration_in_seconds = len(temperatures) * logging_time
    return (temperatures, logging_time, duration_in_seconds)


def temperature_simulation_with_variable_ext_temperature(initial_t0, tau, external_temperature_tuple):
    """This functions simulates the thermal response of a system to external temperature recording.

    Parameters:
        initial_t0 : initial temperature of the system.
        tau : time constant of the system.
        external_temperature_tuple : tuple containing external temperatures,
            logging time and duration of the temperature recording.

    Returns:
        List with the system temperatures, with the same time interval of the input recording."""
    system_temperature = []
    external_temperature, logging_time, duration_in_seconds = external_temperature_tuple

    system_temperature.append(initial_t0)
    t0 = initial_t0
    for i in range(duration_in_seconds//logging_time - 1):
        teq = external_temperature[i]
        system_temperature.append(exponential_func(logging_time, t0, teq, tau))
        t0 = system_temperature[i + 1]
    return system_temperature