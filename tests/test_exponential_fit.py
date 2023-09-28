import functions.exponential_fit as exp_fit
import pandas as pd

# get_seconds and exponential_func have been already tested in test_simulation.py


def test_find_extreme_points():
    # This function should return two points in the temperature-time graph, namely a 2x2 array

    df_temp_time = pd.read_excel("EFI234105840_20230801164648.xls", usecols=[
                                 0, 2], skiprows=25, decimal=',')
    extremepoints = exp_fit.find_extreme_points(
        6626, 7660, 10, df_temp_time)
    assert extremepoints.shape == (2, 2)

    # The times corresponding to extreme points must be multiples of the logging time (in this case, 10)
    assert (extremepoints[0, 0] % 10 == 0) and (
        extremepoints[1, 0] % 10 == 0)
