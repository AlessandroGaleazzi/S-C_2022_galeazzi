# This script contains the tests of all functions defined in the other scripts

import functions.simulation as sim
import numpy as np
import pandas as pd
import pytest

# RUN THE TESTS FROM THE FOLDER "TESTS", OTHERWISE THE TESTS THAT REQUIRE AN EXCEL FILE FAIL

def is_monotonic(list):
    """This function assesses if a list is monotonic. I wrote it to perform a test in this script.

    Parameters:
        list: list to be tested.

    Returns:
        True if the list is monotonic.
        False if the list is not monotonic."""
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

def test_is_monotonic__empty_list():
    """Test that an empty list raises the corresponding exception."""
    with pytest.raises(ValueError) as excinfo:  
        is_monotonic([])  
    assert str(excinfo.value) == "The list is empty"

def test_is_monotonic__one_element_list():
    """Test that a list with one element raises the corresponding exception."""
    with pytest.raises(ValueError) as excinfo:  
        is_monotonic([5])  
    assert str(excinfo.value) == "The list contains one element and cannot be defined monotonic"

def test_is_monotonic__increasing_list():
    """Test that a list with increasing values returns True."""
    assert is_monotonic([1, 3, 7, 10]) == True

def test_is_monotonic__decreasing_list():
    """Test that a list with decreasing values returns True."""
    assert is_monotonic([10, 7, 3, 1]) == True

def test_is_monotonic__not_monotonic_list():
    """Test that a not monotonic list returns False."""
    assert is_monotonic([1, 10, 79, 8]) == False

def test_is_monotonic__two_equal_values():
    """Test that the function returns true also with a not-strictly decreasing or increasing list."""
    assert is_monotonic([1, 1, 3, 7]) == is_monotonic([8, 6, 6, 3]) == True


def test_find_extreme_points__correct_output_values():
    """Test that a known files returns the values the function was designed to return."""
    df_temp_time_test = pd.read_excel("../input/EFI234105840_Exp_Fit.xls", usecols=[
                                 0, 2], skiprows=25, decimal=',')
    extremepoints = sim.find_extreme_points(
        point1 = 6626, point2 = 7660, logging_time = 10, df_temp_time = df_temp_time_test)
    assert (extremepoints[0][0] == 66260) and (extremepoints[0][1] == -18) and \
        (extremepoints[1][0] == 76600) and (extremepoints[1][1] == 27.3)

def test_find_extreme_points__times_are_log_time_multiples():
    """Test that extreme points time is multiple of the logging time (in this case, 10)."""
    df_temp_time_test = pd.read_excel("../input/EFI234105840_Exp_Fit.xls", usecols=[
                                 0, 2], skiprows=25, decimal=',')
    extremepoints = sim.find_extreme_points(
        point1 = 6626, point2 = 7660, logging_time = 10, df_temp_time = df_temp_time_test)
    assert (extremepoints[0, 0] % 10 == 0) and (
        extremepoints[1, 0] % 10 == 0)


def test_get_seconds__invalid_string():
    """Test that a string containing anything but digits and colons raises the corresponding exception."""
    with pytest.raises(ValueError) as excinfo:  
        sim.get_seconds("00:10:1o")  
    assert str(excinfo.value) == "Invalid character in time format. Only digits and colons are allowed."

def test_get_seconds__midnight():
    """Midnight should always return 0 seconds"""
    assert sim.get_seconds(time_str = "00:00:00") == 0

def test_get_seconds__seconds_part():
    """Test that the part of the string that cointains seconds is transformed correctly."""
    assert sim.get_seconds(time_str = "00:00:53") == 53

def test_get_seconds__minutes_part():
    """Test that the part of the string that cointains minutes is transformed correctly."""
    assert sim.get_seconds(time_str = "00:15:00") == 900

def test_get_seconds__minutes_part():
    """Test that the part of the string that cointains hours is transformed correctly."""
    assert sim.get_seconds(time_str = "24:00:00") == 86400


def test_exponential_func__temp_at_t0():
    """Test that at t=0, the function returns t0."""
    assert sim.exponential_func(t = 0, t0 = -10, teq = 20, tau = 1000) == -10

def test_exponential_func__temp_temp_gets_closer_to_teq():
    """Test that as time goes by, the temperature gets always closer to teq."""
    assert (sim.exponential_func(t = 1000, t0 = -10, teq = 20, tau = 1000) <
            sim.exponential_func(t = 10000, t0 = -10, teq = 20, tau = 1000)) == True
    
def test_exponential_func__temp_stays_between_t0_and_teq():
    """Test that, for t > 0, the temperature stays between t0 and teq."""
    t = 1000
    t0 = -10
    teq = 20
    tau = 1000
    assert (-10 < sim.exponential_func(t, t0, teq, tau) < 20) == True


def test_every_second_exponential_func__works_as_exponential_func():
    """Test that this function works as exponential_func, but with time=1."""
    t0 = -10
    teq = 20
    tau = 1000
    time = 1
    assert sim.exponential_func(time, t0, teq, tau) == \
        sim.every_second_exponential_func(t0, teq, tau)

def test_every_second_exponential_func__temp_stays_between_t0_and_teq():
    """Test that, for t > 0, the temperature stays between t0 and teq."""
    t0 = -10
    teq = 20
    tau = 1000
    assert (-10 < sim.every_second_exponential_func(t0, teq, tau) < 20) == True


def test_before_sunrise_temperature_function__temp_higher_than_Tmin():
    """Test that at any time, the function returns T > Tmin."""
    Tmin = 10
    Tsunset = 22
    sunset_time = "19:26:00"
    b = 3.14
    n1 = 44000
    time = 18000
    assert (sim.before_sunrise_temperature_function(Tmin, Tsunset, sunset_time,
                                                     b, n1, time) > 10) == True

def test_before_sunrise_temperature_function__is_monotonic():
    """Test that the function decreases monotonically."""
    Tmin = 10
    Tsunset = 22
    sunset_time = "19:26:00"
    b = 3.14
    n1 = 44000
    assert (sim.before_sunrise_temperature_function(Tmin, Tsunset, sunset_time,
                                                     b, n1, time = 10000) >
            sim.before_sunrise_temperature_function(Tmin, Tsunset, sunset_time,
                                                     b, n1, time = 20000)) == True


def test_daytime_temperature_function__Tsunset_higher_than_Tmin():
    """Test that Tsunset is always above Tmin (from a bug correction)."""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time = "19:26:00"
    a = 2.71
    c = 0.75 
    time = int(sim.get_seconds("19:26:00") - sim.get_seconds("6:52:00") - 0.75 * 3600)
    assert (sim.daytime_temperature_function(Tmin, Tmax, sunrise_time,
                                              sunset_time, a, c, time) > 10) == True

def test_daytime_temperature_function__temp_lower_than_Tmax():
    """Test that temperature is always lower than Tmax (from a bug correction)."""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time = "19:26:00"
    a = 2.71
    c = 0.75 
    time = 40000
    assert (sim.daytime_temperature_function(Tmin, Tmax, sunrise_time,
                                              sunset_time, a, c, time) < 30) == True


def test_after_sunset_temperature_function__temp_lower_than_tsunset():
    """Test that, at any time, the function returns T < Tsunset"""
    Tmin = 10
    Tsunset = 22
    b = 3.14
    n1 = 44000
    time = 18000
    assert (sim.after_sunset_temperature_function(Tmin, Tsunset, b, n1, time) < Tsunset) == True

def test_after_sunset_temperature_function__decreases_monotonically():
    """Test that the function decreases monotonically"""
    Tmin = 10
    Tsunset = 22
    b = 3.14
    n1 = 44000
    assert (sim.after_sunset_temperature_function(Tmin, Tsunset, b, n1, time = 10000) >
            sim.after_sunset_temperature_function(Tmin, Tsunset, b, n1, time = 20000)) == True


def test_one_day_temperature_calculation__length_is_one_day():
    """Test that the temperatures of the whole day were calculated. (output length == 24*3600)"""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time="19:26:00"
    a = 2.71
    b = 3.14
    c = 0.75
    assert len(sim.one_day_temperature_calculation(
        Tmin, Tmax, sunrise_time, sunset_time, a, b, c)) == 24*3600

def test_one_day_temperature_calculation__temp_between_Tmin_and_Tmax():
    """Test that the temperatures calculated by this function stays always between Tmin and Tmax"""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time = "19:26:00"
    a = 2.71
    b = 3.14
    c = 0.75
    assert all(10 <= x <= 30 for x in sim.one_day_temperature_calculation(Tmin, Tmax, sunrise_time,
               sunset_time, a, b, c))


def test_time_to_threshold_temp__same_teq_and_threshold():
    """Test that the if teq and threshold_temp are the same, the corresponding exception is raised."""
    with pytest.raises(ValueError) as excinfo:  
        sim.time_to_threshold_temp(initial_t0 = -18, teq = 30, tau = 1000, threshold_temp = 30)  
    assert str(excinfo.value) == "The threshold temperature that was set is equal to the \
        external temperature, meaning that it will be reached asimptotically."

def test_time_to_threshold_temp__threshold_beyond_teq():
    """Test that if threshold_temp is beyond teq, the corresponding exception is raised."""
    with pytest.raises(ValueError) as excinfo:
        sim.time_to_threshold_temp(initial_t0 = -18, teq = 20, tau = 1000, threshold_temp = 25)
    assert str(excinfo.value) == "The threshold temperature is beyond equilibrium temperature, \
        therefore it will never be reached. Check again your parameters."

def test_time_to_threshold_temp__time_is_integer():
    """Test that the time returned by the function is an integer."""
    initial_t0 = -18
    teq = 30
    tau = 1000
    threshold_temp = 25
    assert type(sim.time_to_threshold_temp(initial_t0, teq, tau, threshold_temp)) == int

def test_time_to_threshold_temp__time_higher_for_higher_threshold():
    """Test that the higher the threshold temperature, the higher the time needed to reach it."""
    initial_t0 = -20
    teq = 30
    tau = 1000
    assert (sim.time_to_threshold_temp(initial_t0, teq, tau, threshold_temp = 25) <
            sim.time_to_threshold_temp(initial_t0, teq, tau, threshold_temp = 28)) == True

def test_time_to_threshold_temp__invariant_for_temp_change_direction():
    """Test that the function returns the same result both for increasing and decreasing temperatures"""
    tau = 1000

    initial_t0_up = -20
    teq_up = 30
    threshold_temp_up = 25

    initial_t0_down = 30
    teq_down = -20
    threshold_temp_down = -15
    assert sim.time_to_threshold_temp(initial_t0_up, teq_up, tau, threshold_temp_up) == \
        sim.time_to_threshold_temp(initial_t0_down, teq_down, tau, threshold_temp_down)


def test_temperature_evolution_up_to_threshold__same_teq_and_threshold():
    """Test that the if teq and threshold_temp are the same, the corresponding exception is raised."""
    with pytest.raises(ValueError) as excinfo:  
        sim.temperature_evolution_up_to_threshold(initial_t0 = -18, teq = 30, tau = 1000, threshold_temp = 30)  
    assert str(excinfo.value) == "The threshold temperature that was set is equal to the \
        external temperature, meaning that it will be reached asimptotically."

def test_temperature_evolution_up_to_threshold__threshold_beyond_teq():
    """Test that if threshold_temp is beyond teq, the corresponding exception is raised."""
    with pytest.raises(ValueError) as excinfo:
        sim.temperature_evolution_up_to_threshold(initial_t0 = -18, teq = 20, tau = 1000, threshold_temp = 25)
    assert str(excinfo.value) == "The threshold temperature is beyond equilibrium temperature, \
        therefore it will never be reached. Check again your parameters."

def test_temperature_evolution_up_to_threshold__longer_list_for_higher_threshold():
    """Test that the higher the threshold temperature, the longer the list returned."""
    initial_t0 = -20
    teq = 30
    tau = 1000

    lower_threshold = 25
    higher_threshold = 28
    assert (len(sim.temperature_evolution_up_to_threshold(initial_t0, teq, tau, lower_threshold)) <
            len(sim.temperature_evolution_up_to_threshold(initial_t0, teq, tau, higher_threshold))) == True

def test_temperature_evolution_up_to_threshold__same_length_for_both_directions():
    """Test that the output list has the same length for both increasing and decreasing temperatures."""
    tau = 1000

    initial_t0_up = -20
    teq_up = 30
    threshold_temp_up = 25

    initial_t0_down = 30
    teq_down = -20
    threshold_temp_down = -15
    assert len(sim.temperature_evolution_up_to_threshold(initial_t0_up, teq_up, tau, threshold_temp_up)) == \
        len(sim.temperature_evolution_up_to_threshold(initial_t0_down, teq_down, tau, threshold_temp_down))

def test_temperature_evolution_up_to_threshold__is_monotonic():
    """Test that the list returned by the function is monotonic"""
    initial_t0 = -20
    teq = 30
    tau = 1000
    threshold_temp = 25
    assert is_monotonic(sim.temperature_evolution_up_to_threshold(initial_t0, teq, \
                                                                  tau, threshold_temp)) == True


def test_temperature_simulation_with_clear_sky_temperature__length_equal_to_sim_length():
    """Test that the function returns a list whose length is equal to the duration of the simulation."""
    Tmin = 13
    Tmax = 25
    sunrise_time = "6:52:00"
    sunset_time="19:26:00"
    a = 2.71
    b = 3.14
    c = 0.75

    starting_time = "00:00:00"
    initial_t0 = -18
    tau = 10000
    duration = "24:00:00"

    temperatures_in_one_day1 = sim.one_day_temperature_calculation(Tmin, Tmax, sunrise_time, \
                                                                   sunset_time, a, b, c)
    assert len(sim.temperature_simulation_with_clear_sky_temperature(
        starting_time, initial_t0, tau, duration, temperatures_in_one_day1)) == \
            sim.get_seconds("24:00:00") == len(temperatures_in_one_day1)

def test_temperature_simulation_with_clear_sky_temperature__right_output_if_Text_const():
    """Test that the output is the same as temperature_evolution_up_to_threshold, \
        if external temperature is constant."""

    # In next lines, I test the function using a 24*3600 elements array \
    # of temperatures equal to 20, according to its expected last argument
    starting_time = "00:00:00"
    initial_t0 = -20
    tau = 1000
    teq = 20
    duration = "24:00:00"
    threshold_temp = 15
    external_temperature = [20] * (24 * 3600)
    temperature_evolution1 = sim.temperature_simulation_with_clear_sky_temperature(
        starting_time, initial_t0, tau, duration, external_temperature)
    temperature_evolution2 = sim.temperature_evolution_up_to_threshold(
        initial_t0, teq, tau, threshold_temp)
    elements_equal = [temperature_evolution1[i] == temperature_evolution2[i]
                      for i in range(len(temperature_evolution2))]
    assert all(elements_equal)

def test_temperature_simulation_with_clear_sky_temperature__Tmax_never_overcome():
    """Test that, if initial_t0 of the system is lower than Tmax, the system never overcomes Tmax.\
        The same for Tmin, with initial_t0 > Tmin). This comes from a bug correction."""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time="19:26:00"
    a = 2.71
    b = 3.14
    c = 0.75
    starting_time = "00:00:00"
    initial_t0 = -20
    tau = 1000
    duration = "24:00:00"
    initial_t0_higher = 40
    initial_t0_lower = -20
    external_temperatures = sim.one_day_temperature_calculation(
        Tmin, Tmax, sunrise_time, sunset_time, a, b, c)
    
    temperature_evolution3 = sim.temperature_simulation_with_clear_sky_temperature(
        starting_time, initial_t0_lower, tau, duration, external_temperatures)
    temperature_evolution4 = sim.temperature_simulation_with_clear_sky_temperature(
        starting_time, initial_t0_higher, tau, duration, external_temperatures)
    assert max(temperature_evolution3) < 30
    assert min(temperature_evolution4) > 10


def test_get_temperatures_from_file__only_xls_files_accepted():    
    """Test that in case the input is not an excel file, the corresponding exception is raised."""
    with pytest.raises(ValueError) as excinfo:  
        sim.get_temperatures_from_file("not_a_proper_file.txt")  
    assert str(excinfo.value) == "The file 'not_a_proper_file.txt' is not a valid Excel file."

def test_get_temperatures_from_file__correct_output_values():
    """This function should return a tuple containing an ndarray,\
        the logging time and the duration of the simulation."""
    result = sim.get_temperatures_from_file(file_name = "../input/EFI234105840_Exp_Fit.xls")
    assert len(result) == 3 and isinstance(result[0], np.ndarray) and\
        (result[1] == 10) and (result[2] == 76600)

def test_get_temperatures_from_file__duration_is_multiple():
    """Test that the duration in seconds divided by the logging time has no rest."""
    result = sim.get_temperatures_from_file(file_name = "../input/EFI234105840_Exp_Fit.xls")
    assert result[2] % result[1] == 0


def test_temperature_simulation_with_variable_ext_temperature__expected_output():
    """Test that this function works just like temperature_simulation_with_clear_sky_temperature,\
        given that the input is the same."""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time = "19:26:00"
    a = 2.71
    b = 3.14
    c = 0.75
    external_temperature = sim.one_day_temperature_calculation(Tmin, Tmax,\
                                                               sunrise_time, sunset_time, a, b, c)
    initial_t0 = -20
    tau = 1000
    starting_time = "00:00:00"
    duration = "24:00:00"
    assert sim.temperature_simulation_with_variable_ext_temperature(initial_t0, tau,\
            external_temperature_tuple = (external_temperature, 1, 24*3600)) ==\
                sim.temperature_simulation_with_clear_sky_temperature(
        starting_time, initial_t0, tau, duration, external_temperature)

def test_temperature_simulation_with_variable_ext_temperature__input_and_output_have_same_length():
    """Test that the function returns an array of temperatures as long as imput one\
        (one-to-one correspondence between external and system temperatures)."""
    Tmin = 10
    Tmax = 30
    sunrise_time = "6:52:00"
    sunset_time = "19:26:00"
    a = 2.71
    b = 3.14
    c = 0.75
    initial_t0 = -20
    tau = 1000
    external_temperature = sim.one_day_temperature_calculation(Tmin, Tmax,\
                                                               sunrise_time, sunset_time, a, b, c)
    assert len(sim.temperature_simulation_with_variable_ext_temperature(initial_t0,
               tau, (external_temperature, 1, 24*3600))) == len(external_temperature)
