import functions.simulation as sim
# Why it does not recognize the module?


def is_monotonic(list):
    # This function assesses if a list is monotonic. I wrote it to perform a test in this script

    increasing = decreasing = True

    for i in range(1, len(list)):
        if list[i] < list[i - 1]:
            increasing = False
        if list[i] > list[i - 1]:
            decreasing = False

    return increasing or decreasing


def test_get_seconds():
    # Midnight should always return 0 seconds
    assert sim.get_seconds("00:00:00") == 0

    # Ordinary case testing
    assert sim.get_seconds("01:00:00") == 3600


def test_exponential_func():
    # At t=0, the function should return t0
    assert sim.exponential_func(0, -10, 20, 1000) == -10

    # As time goes by, temperature should always get closer to teq
    assert (sim.exponential_func(1000, -10, 20, 1000) <
            sim.exponential_func(10000, -10, 20, 1000)) == True


def test_every_second_exponential_func():
    # Make sure that it is just the same function as exponentials_func, but with t=1
    assert sim.exponential_func(
        1, -10, 20, 1000) == sim.every_second_exponential_func(-10, 20, 1000)
    assert sim.exponential_func(
        1, 10, 30, 100) == sim.every_second_exponential_func(10, 30, 100)


def test_time_to_threshold_temp():
    # The time returned by the function must be a multiple of the time interval given (here, 10)
    assert sim.time_to_threshold_temp(-18, 30, 1000, 25, 10) % 10 == 0

    # Given the same external conditions, the time needed to reach a higher threshold temperature should be higher
    assert (sim.time_to_threshold_temp(-20, 30, 1000, 25, 10) <
            sim.time_to_threshold_temp(-20, 30, 1000, 28, 10)) == True

    # The function should return the same result both for increasing and decreasing temperatures, in the same conditions
    assert sim.time_to_threshold_temp(-20, 30, 1000, 25,
                                      10) == sim.time_to_threshold_temp(30, -20, 1000, -15, 10)


def test_temperature_evolution_up_to_threshold():
    # Given the same external conditions, the list returned by simulation performed to reach a higher threshold temperature should be higher
    assert (len(sim.temperature_evolution_up_to_threshold(-20, 30, 1000, 25)) <
            len(sim.temperature_evolution_up_to_threshold(-20, 30, 1000, 28))) == True

    # The function should return two lists with the same length both for increasing and decreasing temperatures, in the same conditions
    assert len(sim.temperature_evolution_up_to_threshold(-20, 30, 1000, 25
                                                         )) == len(sim.temperature_evolution_up_to_threshold(30, -20, 1000, -15))

    # The list returned by the function should be monotonic
    assert is_monotonic(
        sim.temperature_evolution_up_to_threshold(-20, 30, 1000, 25)) == True


def test_before_sunrise_temperature_function():
    # At any time, the function should return T > Tmin
    assert (sim.before_sunrise_temperature_function(
        10, 22, "19:26:00", 3.14, 44000, 18000) > 10) == True

    # The function should decrease monotonically
    assert (sim.before_sunrise_temperature_function(10, 22, "19:26:00", 3.14, 44000, 10000) >
            sim.before_sunrise_temperature_function(10, 22, "19:26:00", 3.14, 44000, 20000)) == True


def test_daytime_temperature_function():
    # This test is the result of a bug correction, where Tsunset was lower than Tmin
    assert (30 > sim.daytime_temperature_function(10, 30, "6:52:00", "19:26:00", 2.71, 0.75, int(
        sim.get_seconds("19:26:00") - sim.get_seconds("6:52:00") - 0.75 * 3600)) > 10) == True


def test_after_sunset_temperature_function():
    # At any time, the function should return T < Tsunset
    assert (sim.after_sunset_temperature_function(
        10, 22, 3.14, 44000, 18000) < 22) == True

    # The function should decrease monotonically
    assert (sim.after_sunset_temperature_function(10, 22, 3.14, 44000, 10000) >
            sim.after_sunset_temperature_function(10, 22, 3.14, 44000, 20000)) == True


def test_one_day_temperature_calculation():
    # The function should return an array with 24*3600 values, meaning that every second of the day has a correspondent temperature
    assert len(sim.one_day_temperature_calculation(10, 30, sunrise_time="6:52:00",
               sunset_time="19:26:00", a=2.71, b=3.14, c=0.75)) == 24*3600


def test_temperature_simulation_with_variable_ext_temperature():
    # This function should return a list whose length corresponds to the duration of the simulation (which is a parameter)
    temperatures_in_one_day = sim.one_day_temperature_calculation(
        Tmin=13, Tmax=25, sunrise_time="6:52:00", sunset_time="19:26:00")
    assert len(sim.temperature_simulation_with_variable_ext_temperature(
        "00:00:00", -18, 10000, "24:00:00", temperatures_in_one_day)) == sim.get_seconds("24:00:00")

    # This function should work just like time_to_threshold, but to test it i need to produce a graphical version of time_to_threshold... TO DO!!!
