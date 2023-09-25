import functions.simulation as sim

 
# Definition of class for testing
def test_get_seconds():
        # Midnight should always return 0 seconds
        assert sim.get_seconds("00:00:00") == 0

        # Ordinary case testing
        assert sim.get_seconds("01:00:00") == 3600

def test_exponential_func():
        # At t=0, the function should return t0
        assert sim.exponential_func(0, -10, 20, 1000) == -10

        # As time goes by, temperature should always get closer to teq
        assert (sim.exponential_func(1000, -10, 20, 1000) < sim.exponential_func(10000, -10, 20, 1000)) == True

def test_time_to_threshold_temp():
        # The time returned by the function must be a multiple of the time interval given (here, 10)
        assert sim.time_to_threshold_temp(-18, 30, 1000, 25, 10) % 10 == 0

        #Given the same external conditions, the time needed to reach a higher threshold temperature should be higher 
        assert (sim.time_to_threshold_temp(-20, 30, 1000, 25, 10) < sim.time_to_threshold_temp(-20, 30, 1000, 28, 10)) == True

        #The function should return the same result both for increasing and decreasing temperatures, in the same conditions
        assert sim.time_to_threshold_temp(-20, 30, 1000, 25, 10) == sim.time_to_threshold_temp(30, -20, 1000, -15, 10)

def test_before_sunrise_temperature_function():
        # At any time, the function should return T > Tmin
        assert (sim.before_sunrise_temperature_function( 10, 22, "19:26:00", 3.14, 44000, 18000) > 10 ) == True

        # The function should decrease monotonically 
        assert (sim.before_sunrise_temperature_function( 10, 22, "19:26:00", 3.14, 44000, 10000) > sim.before_sunrise_temperature_function( 10, 22, "19:26:00", 3.14, 44000, 20000)) == True

def test_daytime_temperature_function():
        #This test is the result of a bug correction, where Tsunset was lower than Tmin
        assert (30 > sim.daytime_temperature_function( 10, 30, "6:52:00", "19:26:00", 2.71, 0.75, int( sim.get_seconds("19:26:00")- sim.get_seconds("6:52:00") - 0.75 * 3600 )) > 10) == True

def test_after_sunset_temperature_function():
        # At any time, the function should return T < Tsunset
        assert (sim.after_sunset_temperature_function( 10, 22, 3.14, 44000, 18000) < 22) == True

        # The function should decrease monotonically 
        assert (sim.after_sunset_temperature_function( 10, 22, 3.14, 44000, 10000) > sim.after_sunset_temperature_function( 10, 22, 3.14, 44000, 20000)) == True

def test_one_day_temperature_calculation():
        # The function should return an array with 24*3600 values, meaning that every second of the day has a correspondent temperature
        assert len(sim.one_day_temperature_calculation(10, 30, sunrise_time="6:52:00", sunset_time="19:26:00", a = 2.71, b = 3.14, c = 0.75 )) == 24*3600
