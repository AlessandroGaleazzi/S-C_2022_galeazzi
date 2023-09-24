import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


class TemperatureError(Exception):
    #is this the way I should write my own exceptions?
    pass


def get_seconds(time_str):
    # split in hh, mm, ss
    #exception: if anything but numbers and : is present, raise an exception. same for mm, ss > 60
    #tests: ordinary case + 00:00:00
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


def exponential_func(t, t0, teq, tau):
    return teq +(t0-teq)*np.exp(-t/tau)

def time_to_threshold_temp(t0, teq, tau, threshold_temp, interval_time):

    #This function calculate the time needed to reach a certain threshold temperature, given the time between temperatures and all the system and environmental parameters
    
    if ((t0 < teq) and (threshold_temp > teq)) or ((t0 > teq) and (threshold_temp < teq)):
        raise TemperatureError("The threshold temperature is beyond equilibrium temperature, therefore it will never be reached . Check again your parameters.")
    
    if threshold_temp == teq:
        raise TemperatureError("The threshold temperature that was set is equal to the external temperature, meaning that it will be reached asimptotically. ")
        #A special function for this situation (like a certain deviation from external temperature)? Maybe it would be actually useless, just think about it

    counter = 1
    time, temp = interval_time, t0
    
    if threshold_temp < teq:
        while (temp < threshold_temp):
            temp = exponential_func(time, t0, teq, tau)
            counter += 1
            time = counter * interval_time   
    else:
        while (temp > threshold_temp):
            temp = exponential_func(time, t0, teq, tau)
            counter += 1
            time = counter * interval_time
    return time




"""
def calculate_day_night_length(sunrise_time, sunset_time):
            
    # calculate time difference between dawn and sunset times
    day_length = get_seconds(sunset_time) - get_seconds(sunrise_time)
    night_length = 24 * 3600 - day_length

    return day_length, night_length   #in seconds
"""
#I wrote this function because I needed it. Now I don't, but just in case I keep it here



def before_sunrise_temperature_function(Tmin, Tsunset, sunset_time, b, n1, time):
    #function for temperature calculation during daytime

    return Tmin + (Tsunset-Tmin) * np.exp( - b * ( time - get_seconds(sunset_time) + 24*3600 ) / n1 ) - ( time - get_seconds(sunset_time) + 24*3600 ) / n1 * np.exp( - b )

def daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, time):
    #function for temperature calculation between sunrise and sunset

    return Tmin + ( Tmax - Tmin) * np.sin( np.pi * ( time  ) / ( get_seconds(sunset_time) - get_seconds(sunrise_time) + 2 * ( a - c ) * 3600))

def after_sunset_temperature_function(Tmin, Tsunset, sunset_time, b, n2, time):
    #function for temperature calculation after sunset
    
    return Tmin + (Tsunset - Tmin) * np.exp(- b * ( time  ) / n2 ) - ( time ) / n2 * np.exp( - b )




def one_day_temperature_calculation(Tmin, Tmax, sunrise_time="6:52:00", sunset_time="19:26:00", a = 2.71, b = 3.14, c = 0.75 ):
    #calculate temp using daytime temperature. do i really need this funcition? maybe it's better to use the main func to handle the time  
    all_day_temperatures = []
    
    #determine initial parameters
    Tsunset = daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, int( get_seconds(sunset_time)- get_seconds(sunrise_time) - c * 3600 ))  #CHECK THE TIME, REMEMBER THAT IS SHIFTED BY ""
    n1 = get_seconds(sunrise_time) - get_seconds(sunset_time) + ( c + 24 ) * 3600
    n2 = get_seconds(sunrise_time) - get_seconds(sunset_time) + ( c + 24 ) * 3600      #they are the same, and are meant for simulations in which the parameters change as days go by 
    
    for t in range(int(get_seconds(sunrise_time) + c * 3600)):
        all_day_temperatures.append(before_sunrise_temperature_function(Tmin, Tsunset, sunset_time, b, n1, t))
    for t in range(int(get_seconds(sunset_time) - get_seconds(sunrise_time) - c * 3600)):
        all_day_temperatures.append(daytime_temperature_function(Tmin, Tmax, sunrise_time, sunset_time, a, c, t))
    for t in range(24 * 3600 - get_seconds(sunset_time)):
        all_day_temperatures.append(after_sunset_temperature_function(Tmin, Tsunset, sunset_time, b, n2, t))
    return all_day_temperatures


"""
def nighttime_temperature_calculation():
    #calculate temp using nighttime temperature


    return temperature
"""


"""
def daily_temperature_simulation(Tmax, Tmin, time_interval, initial_time = "10:00:00", simulation_duration = "72:00:00", dawn_time="6:52:00", sunset_time="19:26:00", a=1.86, b=2.20 ):
    #this function produces a sinusoidal function representing the variation of temperature withing 24h, generating temperature data according to the given time interval
    #Time values: Bologna, 15/09/23

    #REMEMBER TO TURN a AND b INTO SECONDS!!!!!!!
    day_lenght, night_length = calculate_day_night_length(dawn_time, sunset_time)


    return 0
"""




"""

try:
    print(time_to_threshold_temp(-18, 27, 1020, 25, 10))
except TemperatureError as e:
    print(f"Error: {e}")
"""

#print(calculate_day_night_length("6:52:00", "19:26:00"))
temperatures_in_one_day = one_day_temperature_calculation(Tmin = 13, Tmax = 25, sunrise_time="6:52:00", sunset_time="19:26:00")
seconds_in_one_day = np.arange(24 * 3600)
plt.plot(seconds_in_one_day, temperatures_in_one_day, label="Preliminary check")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("24 hours temperature variation")
plt.show()