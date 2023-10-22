# This script contains the tests of all functions defined in the other scripts

import functions.simulation as sim
import numpy as np
import pandas as pd
import pytest

# REMEMBER TO RUN THE TESTS FROM THE FOLDER "TESTS", OTHERWISE THE TESTS THAT REQUIRE AN EXCEL FILE FAIL

def is_monotonic(list):
    # This function assesses if a list is monotonic. I wrote it to perform a test in this script
    increasing = decreasing = True

    if len(list) == 0:
        raise ValueError("The list is empty")
    if len(list) == 1:
        raise ValueError("The list contains one element and cannot be defined monotonic")

    for i in range(1, len(list)):
        if list[i] < list[i - 1]:
            increasing = False
        if list[i] > list[i - 1]:
            decreasing = False

    return increasing or decreasing

def test_is_monotonic():
    # Test that exceptions are raised correctly
    with pytest.raises(ValueError) as excinfo:  
        is_monotonic([])  
    assert str(excinfo.value) == "The list is empty"
    with pytest.raises(ValueError) as excinfo:  
        is_monotonic([5])  
    assert str(excinfo.value) == "The list contains one element and cannot be defined monotonic"

    # Test two ordinary cases
    assert is_monotonic([1, 3, 7, 10]) == True
    assert is_monotonic([10, 7, 3, 1]) == True
    assert is_monotonic([1, 10, 79, 8]) == False

def test_find_extreme_points():
    # This function should return two points in the temperature-time graph, namely a 2x2 array

    df_temp_time_test = pd.read_excel("EFI234105840_Exp_Fit.xls", usecols=[
                                 0, 2], skiprows=25, decimal=',')
    extremepoints = sim.find_extreme_points(
        point1 = 6626, point2 = 7660, logging_time = 10, df_temp_time = df_temp_time_test)
    assert extremepoints.shape == (2, 2)

    # The times corresponding to extreme points must be multiples of the logging time (in this case, 10)
    assert (extremepoints[0, 0] % 10 == 0) and (
        extremepoints[1, 0] % 10 == 0)

def test_get_seconds():
    # Test that the exception is raised correctly
    with pytest.raises(ValueError) as excinfo:  
        sim.get_seconds("00:10:1o")  
    assert str(excinfo.value) == "Invalid character in time format. Only digits and colons are allowed."

    # Midnight should always return 0 seconds
    assert sim.get_seconds(time_str = "00:00:00") == 0

    # Ordinary case testing
    assert sim.get_seconds(time_str = "01:00:00") == 3600


def test_exponential_func():
    # At t=0, the function should return t0
    assert sim.exponential_func(t = 0, t0 = -10, teq = 20, tau = 1000) == -10

    # As time goes by, temperature should always get closer to teq
    assert (sim.exponential_func(t = 1000, t0 = -10, teq = 20, tau = 1000) <
            sim.exponential_func(t= 10000, t0 = -10, teq = 20, tau = 1000)) == True


def test_every_second_exponential_func():
    # Make sure that it is just the same function as exponentials_func, but with t=1
    assert sim.exponential_func(
        t = 1, t0 = -10, teq = 20, tau = 1000) == sim.every_second_exponential_func(t0 = -10, teq = 20, tau = 1000)
    assert sim.exponential_func(
        t = 1, t0 = 10, teq = 30, tau = 100) == sim.every_second_exponential_func(t0 = 10, teq = 30, tau = 100)


def test_before_sunrise_temperature_function():
    # At any time, the function should return T > Tmin
    assert (sim.before_sunrise_temperature_function(
        Tmin = 10, Tsunset = 22, sunset_time = "19:26:00", b = 3.14, n1 = 44000, time = 18000) > 10) == True

    # The function should decrease monotonically
    assert (sim.before_sunrise_temperature_function(Tmin = 10, Tsunset = 22, sunset_time = "19:26:00", b = 3.14, n1 = 44000, time = 10000) >
            sim.before_sunrise_temperature_function(Tmin = 10, Tsunset = 22, sunset_time = "19:26:00", b = 3.14, n1 = 44000, time = 20000)) == True


def test_daytime_temperature_function():
    # This test is the result of a bug correction, where Tsunset was lower than Tmin
    assert (30 > sim.daytime_temperature_function(Tmin = 10, Tmax = 30, sunrise_time = "6:52:00", sunset_time = "19:26:00", a = 2.71, c = 0.75, time = int(
        sim.get_seconds("19:26:00") - sim.get_seconds("6:52:00") - 0.75 * 3600)) > 10) == True


def test_after_sunset_temperature_function():
    # At any time, the function should return T < Tsunset
    assert (sim.after_sunset_temperature_function(
        Tmin = 10, Tsunset = 22, b = 3.14, n1 = 44000, time = 18000) < 22) == True

    # The function should decrease monotonically
    assert (sim.after_sunset_temperature_function(Tmin = 10, Tsunset = 22, b = 3.14, n1 = 44000, time = 10000) >
            sim.after_sunset_temperature_function(Tmin = 10, Tsunset = 22, b = 3.14, n1 = 44000, time = 20000)) == True


def test_one_day_temperature_calculation():
    # The function should return an array with 24*3600 values, meaning that every second of the day has a correspondent temperature
    assert len(sim.one_day_temperature_calculation(Tmin = 10, Tmax = 30, sunrise_time = "6:52:00",
               sunset_time="19:26:00", a = 2.71, b = 3.14, c = 0.75)) == 24*3600

    # The temperatures calculated by this function should always stay between Tmin and Tmax
    assert all(10 <= x <= 30 for x in sim.one_day_temperature_calculation(Tmin = 10, Tmax = 30, sunrise_time = "6:52:00",
               sunset_time = "19:26:00", a = 2.71, b = 3.14, c = 0.75))


def test_time_to_threshold_temp():
    # Test that the exceptions are raised correctly
    with pytest.raises(ValueError) as excinfo:  
        sim.time_to_threshold_temp(initial_t0 = -18, teq = 30, tau = 1000, threshold_temp = 30)  
    assert str(excinfo.value) == "The threshold temperature that was set is equal to the external temperature, meaning that it will be reached asimptotically."

    with pytest.raises(ValueError) as excinfo:
        sim.time_to_threshold_temp(initial_t0 = -18, teq = 20, tau = 1000, threshold_temp = 25)
    assert str(excinfo.value) == "The threshold temperature is beyond equilibrium temperature, therefore it will never be reached. Check again your parameters."

    # The time returned by the function must be an integer
    assert type(sim.time_to_threshold_temp(initial_t0 = -18, teq = 30, tau = 1000, threshold_temp = 25)) == int

    # Given the same external conditions, the time needed to reach a higher threshold temperature should be higher
    assert (sim.time_to_threshold_temp(initial_t0 = -20, teq = 30, tau = 1000, threshold_temp = 25) <
            sim.time_to_threshold_temp(initial_t0 = -20, teq = 30, tau = 1000, threshold_temp = 28)) == True

    # The function should return the same result both for increasing and decreasing temperatures, in the same conditions
    assert sim.time_to_threshold_temp(initial_t0 = -20, teq = 30, tau = 1000,
                                        threshold_temp = 25) == sim.time_to_threshold_temp(initial_t0 = 30, teq = -20, tau = 1000, threshold_temp = -15)


def test_temperature_evolution_up_to_threshold():
    # Test that the exceptions are raised correctly
    with pytest.raises(ValueError) as excinfo:  
        sim.temperature_evolution_up_to_threshold(initial_t0 = -18, teq = 30, tau = 1000, threshold_temp = 30)  
    assert str(excinfo.value) == "The threshold temperature that was set is equal to the external temperature, meaning that it will be reached asimptotically."

    with pytest.raises(ValueError) as excinfo:
        sim.temperature_evolution_up_to_threshold(initial_t0 = -18, teq = 20, tau = 1000, threshold_temp = 25)
    assert str(excinfo.value) == "The threshold temperature is beyond equilibrium temperature, therefore it will never be reached. Check again your parameters."

    # Given the same external conditions, the list returned by simulation performed to reach a higher threshold temperature should be higher
    assert (len(sim.temperature_evolution_up_to_threshold(initial_t0 = -20, teq = 30, tau = 1000, threshold_temp = 25)) <
            len(sim.temperature_evolution_up_to_threshold(initial_t0 = -20, teq = 30, tau = 1000, threshold_temp = 28))) == True

    # The function should return two lists with the same length both for increasing and decreasing temperatures, in the same conditions
    assert len(sim.temperature_evolution_up_to_threshold(initial_t0 = -20, teq = 30, tau = 1000, threshold_temp = 25
                                                         )) == len(sim.temperature_evolution_up_to_threshold(initial_t0 = 30, teq = -20, tau = 1000, threshold_temp = -15))

    # The list returned by the function should be monotonic
    assert is_monotonic(
        sim.temperature_evolution_up_to_threshold(initial_t0 = -20, teq = 30, tau = 1000, threshold_temp = 25)) == True


def test_temperature_simulation_with_clear_sky_temperature():
    # This function should return a list whose length corresponds to the duration of the simulation (which is a parameter)
    temperatures_in_one_day1 = sim.one_day_temperature_calculation(
        Tmin = 13, Tmax = 25, sunrise_time = "6:52:00", sunset_time="19:26:00", a = 2.71, b = 3.14, c = 0.75)
    assert len(sim.temperature_simulation_with_clear_sky_temperature(
        starting_time = "00:00:00", initial_t0 = -18, tau = 10000, duration = "24:00:00", one_day_external_temperature = temperatures_in_one_day1)) == sim.get_seconds("24:00:00") == len(temperatures_in_one_day1)

    # This function should calculate the same temperature evolution as temperature_evolution_up_to_threshold, in case I provide a temperature which is steady throughout the day

    # This way, I can test the function using a 24*3600 elements array of temperatures equal to 20, according to its expected last argument
    external_temperature = [20] * (24 * 3600)
    temperature_evolution1 = sim.temperature_simulation_with_clear_sky_temperature(
        starting_time = "00:00:00", initial_t0 = -20, tau = 1000, duration = "24:00:00", one_day_external_temperature = external_temperature)
    temperature_evolution2 = sim.temperature_evolution_up_to_threshold(
        initial_t0 = -20, teq =  20, tau = 1000, threshold_temp = 15)
    elements_equal = [temperature_evolution1[i] == temperature_evolution2[i]
                      for i in range(len(temperature_evolution2))]
    assert all(elements_equal)

    # If initial_t0 of the system is lower than Tmax, the system should never overcome Tmax (same for Tmin, with initial_t0 > Tmin). This comes from a bug correction.
    external_temperatures = sim.one_day_temperature_calculation(
        Tmin = 10, Tmax = 30, sunrise_time = "6:52:00", sunset_time="19:26:00", a = 2.71, b = 3.14, c = 0.75)
    temperature_evolution3 = sim.temperature_simulation_with_clear_sky_temperature(
        starting_time = "00:00:00", initial_t0 = -20, tau = 1000, duration = "24:00:00", one_day_external_temperature = external_temperatures)
    temperature_evolution4 = sim.temperature_simulation_with_clear_sky_temperature(
        starting_time = "00:00:00", initial_t0 = 40, tau = 1000, duration = "24:00:00", one_day_external_temperature = external_temperatures)
    assert max(temperature_evolution3) < 30
    assert min(temperature_evolution4) > 10


def test_get_temperatures_from_file():    
    # Test that the exception is raised correctly
    with pytest.raises(ValueError) as excinfo:  
        sim.get_temperatures_from_file("not_a_proper_file.txt")  
    assert str(excinfo.value) == "The file 'not_a_proper_file.txt' is not a valid Excel file."

    # This function should return a tuple contanining a numpy array, an int and another int, in this order
    result = sim.get_temperatures_from_file(file_name = "EFI234105840_Exp_Fit.xls")
    assert len(result) == 3 and isinstance(result[0], np.ndarray) and isinstance(
        result[1], int) and isinstance(result[2], int)

    # The duration in seconds divided by the logging time should have no rest
    assert result[2] % result[1] == 0


def test_temperature_simulation_with_variable_ext_temperature():
    # This function should work just like temperature_simulation_with_clear_sky_temperature, given that the input is the same
    external_temperature = sim.one_day_temperature_calculation(Tmin = 10, Tmax = 30, sunrise_time = "6:52:00",
                                                               sunset_time = "19:26:00", a = 2.71, b = 3.14, c = 0.75)
    assert sim.temperature_simulation_with_variable_ext_temperature(initial_t0 = -20, tau = 1000, external_temperature_tuple = (external_temperature, 1, 24*3600)) == sim.temperature_simulation_with_clear_sky_temperature(
        starting_time = "00:00:00",initial_t0 = -20, tau = 1000, duration = "24:00:00", one_day_external_temperature = external_temperature)

    # This function has to return an array of temperatures with the same length of the imput one (one-to-one correspondence between external and system temperatures)
    assert len(sim.temperature_simulation_with_variable_ext_temperature(initial_t0 = -20,
               tau = 1000, external_temperature_tuple = (external_temperature, 1, 24*3600))) == len(external_temperature)
