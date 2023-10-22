# Structure of the project

The project can be downloaded from this repository and can be run from the command line. First of all, it is important to know the content of every file:

- The file [requirements.txt](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/requirements.txt) contains a list of the dependencies needed by the project
- In the folder [tests](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/tests), the user can find the file [test_simulation.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/tests/test_simulation.py), where the functions written in [simulation.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/simulation.py) are tested. It is important to run the tests from this folder with the command ***"pytest test_simulation.py"***, since the tests rely on an the excel file that is stored in the same folder.
- The folders [data](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/data) and [plots](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/plots) contain the results of all the possible simulations (as .npy files) and plots (as .png files), respectively.
- The folder [input](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/input) contains the input datasheets from which temperatures recordings can be used.

### The folder "functions"

The folder [functions](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/functions) is the main part of the program:

- In the file [configuration.ini](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/configuration.ini), all the parameters of the simulation can be set (later on this).
- In the file [simulation.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/simulation.py), all the function used in this project are defined.
- In the file [exponential_fit.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/exponential_fit.py), it is possible to calculate the ***&tau;*** parameter starting from a proper temperature recording and to set it in the [configuration.ini](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/configuration.ini), if wanted.
- In the file [controls,py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/controls.py), all the simulations can be launched and saved.
- In the file [plots.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/plots.py), the results of saved simulations can be plotted.

# How-to guides

### How to exponentially fit

In order to test the performances of a thermal container, the user needs to perform a particular kind of measurements: the best way (or better, the best way the author of this project has found so far) to estimate the  ***&tau;*** parameter is to place the thermal container in a cold environment (like a freezer) and then move it into a room where the temperature is higher and as constant as possible. An example of this kind of measurement is the file *EFI234105840_Exp_Fit.xls*, from which the ***&tau;*** parameter of [this thermal container for insulin transportation](https://www.amazon.it/SHBC-raffreddatori-trasportano-organizzato-Raffreddamento/dp/B07WQGC82P/ref=sr_1_10?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2DGAR2614KNOP&keywords=insulin%2Bcontainer&qid=1697393523&sprefix=insulin%2Bcontainer%2Caps%2C108&sr=8-10&th=1) can be extracted and set in the configuration file. The script that performs this fit can be called with the command ***"python3 exponential_fit.py --configuration file name--"***, which illustrates every step of the fitting process to the user with two different graphs. Before running the fitting command, it is important to write the name of the excel file ***file_name*** in the "exponential fit" section of the configuration file chosen in the command, together with the initial and final point of the fitting interval (***point1*** and ***point2***, respectively).

### How to simulate

All the simulations are performed calling the file [controls.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/controls.py) with the command ***"python3 controls.py --configuration file name-- --simulations to be performed--***, and providing the configuration file name from which to take the parameters together with the simulations wanted. In particular,

1) ***"sim1"*** will calculate the time (in seconds) that the system needs to reach a certain threshold temperature.
2) ***"sim2"*** will return the temperature evolution of the system during every second until the threshold temperature is reached.
3) ***"sim3"*** will calculate the temperature of every second of the day according to the clear-sky model and the selected parameters.
4) ***"sim4"*** will simulate the temperature evolution of the system with the temperature simulated in 3. as external temperature.
5) ***"sim5"*** will import the external temperature recording and its main parameters.
6) ***"sim6"*** will simulate the temperature evolution of the system with the temperature imported in 5. as external temperature.

Before launching the simulation, it is important to check that all the required parameters have been set in the [configuration.ini](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/configuration.ini). In particular,

 1) ***"Time to threshold"*** and ***"Temperature evolution up to threshold"*** (No. 1 and 2) require the parameters ***initial_t0***, ***teq***, ***tau***, ***threshold_temperature***.
 2) ***"Clear-sky temperature"*** (No. 3) requires the parameters ***Tmin***, ***Tmax***, ***sunrise_time***, ***sunset_time***, ***a***, ***b***, ***c***.
 3) ***"Simulation with clear-sky temperature"*** (No. 4) requires the parameters ***starting_time***, ***initial_t0***, ***tau***, ***duration***, and must be performed after a ***"clear-sky temperature"*** simulation (No. 3).
 4) ***"Import of an external temperature recording"*** (No. 5) requires the parameter ***file_name***, and will also update the parameters ***logging_time*** and ***duration_in_seconds***.
 5) ***"Simulation with external temperature recording"*** (No. 6) requires the parameters provided by ***"Import of an external temperature recording"*** (No. 5), together with ***initial_t0*** and ***tau***.
 6) 
The same holds for other configuration files that the user might want to use.

### How to plot

Once the required simulation has been performed, it is possible to plot the results calling the file [plots.py](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/blob/main/functions/plots.py) with the command ***"python3 plots.py --configuration file name-- --simulations to be performed--"***, and providing the configuration file name from which to take the parameters together with the plots wanted. In particular,

1) ***"plot1"*** will plot the temperature evolution up to the threshold temperature simulated with ***"Temperature evolution up to threshold"***.
2) ***"plot2"*** will plot the clear-sky temperature simulated with ***"Clear-sky temperature"***.
3) ***"plot3y"*** and ***"plot3n"*** will plot the temperature evolution of the system with clear-sky external temperature simulated with ***"Simulation with clear-sky temperature"***. y/n enables/disables the external temperature plotting.
4) ***"plot4"*** will plot the external temperature recording imported with ***"Import of an external temperature recording"***.
5) ***"plot5y"*** and ***"plot5n"*** will plot the temperature evolution of the system calculated with the external temperature imported with ***"Import of an external temperature recording"***. y/n enables/disables the external temperature plotting.

All the plotting functions import the numpy arrays saved in the [data](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/data) folder, where the simulation results are saved, and save the graphs in the [plots](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/plots) folder.

# The data logger

In this project, all temperatures recordings were performed using the device "Elitech RC-5+ Reusable USB Temperature Data Logger With Auto PDF Report" ( it is possible to find more details [here](https://www.elitechus.com/collections/multi-use-temperature-data-logger/products/elitech-rc-5-pdf-usb-temperature-data-logger-32000-points-reusable)), since it possesses all the main requirements that any person interested in this kind of measurements would desire (small size, low cost, possibility to store data and export them into excel files thanks to a free software) and was precisely designed "to monitor the temperature of food, medicine, chemicals and other products in storage and transports" (from the User's Manual).
This projects contains some excel datasheets that are meant to show examples of temperature recording and use. In the folder [input](https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi/tree/main/input), you can find two excel datasheets:

- The file *EFI234105840_Exp_Fit.xls* contains an example of an experimental measurement of the ***&tau;*** parameter (a cold container was placed in a thermal bath)
- The file *EFI234105840_Ext_Temp_Recording.xls* contains an example of external temperature recording, from which a simulation can be performed

In these datasheets, we are mainly interested in the ***time*** and ***temperature*** recordings (columns B and C, from raw 27) and in the ***logging time*** of the recording (E:11). 
The project relies on this kind of input data to calculate ***&tau;*** parameters and to perform simulation based on external temperatures recordings, together with  a very particular kind of external temperature simulation (last section).


# Thermal evolution of a system with negligible internal resistance

A lot of transient heat flow problems can be efficiently addressed with good accuracy if we assume that the internal conductive resistance within the studied system is negligible, ensuring that its temperature remains relatively uniform at any given moment. This simplification is legitimate when the external thermal resistance between the system's surface and the surrounding medium is significantly greater than the internal resistance, so that this last contribution can be neglected while studying the heat exchange process. The relationship between these resistances can be quantified through their ratio, as

![equation1](https://latex.codecogs.com/gif.image?\dpi{110}\frac{R_{int}}{R_{ext}}=\frac{L/kA}{1/hA}=\frac{hL}{k})

where

- ***L*** is the scale length of the system
- ***k*** is the thermal conductivity of the system
- ***A*** is the surface area of the system
- ***h*** is the heat transfer coefficent of the medium

This ratio is also called "Biot number" *Bi*, and quantifies the deviation of a system from this picture (The lower *Bi*, the better this approximation will work).

If we consider a system placed in a thermal bath with constant temperature, it is possible to show (see [this link](https://www.unirc.it/documentazione/materiale_didattico/1467_2015_404_23033.pdf) for the derivation, last 3 pages) that the temperature evolution of the system over time is described by 

![equation2](https://latex.codecogs.com/gif.image?\dpi{110}T(t)=T_e_q&plus;(T_0-T_{eq})e^{-t/\tau})

where

- ***T<sub>eq*** is the temperature of the thermal bath the system is placed in
- ***T<sub>0*** is the temperature of the system at t=0
- ***&tau;*** is the time constant of the system

In particular, the parameter ***&tau;*** contains the quantitative information about the capability of the system to slow down its temperature variation in response to a different external temperature, and can be analitically calculated as

![equation3](https://latex.codecogs.com/gif.image?\dpi{110}\mathbf{\tau}=\frac{c\rho&space;V}{hA})

where

- ***c*** is the system specific heat capacity
- ***&rho;*** is the system mass density
- ***V*** is the system volume
- ***h*** is the heat transfer coefficent of the medium
- ***A*** is the system surface area

In general, it is not possible to calculate ***&tau;*** for an arbitrary thermal container with reasonable precision. On the other hand, it is possible to determine it with an exponential fit on experimental data. This kind of experiment does not require any major apparatus (a digital thermometer is enough) and allows a complete determination of the capability of a thermal container, since the only system-related quantity that we need to predict the temperature evolution of a system is its ***&tau;***. Given this parameter, we can simulate its thermal evolution once the external temperature is given (a recording of it is perfectly fine, since it can be seen as a step-by-step constant ***T<sub>eq***) using Eq.2

# The clear-sky model

If we want to simulate the temperature evolution of a system exposed to diurnal variation of external temperature, a good starting point is the model described in [this work](https://link.springer.com/article/10.1007/s00484-017-1471-5), in which the variation of external temperature over 24 hours is simulated according to the behaviour that it shows in so-called "clear-sky" days (a day in which the influence of clouds on the solar radiation at ground can be neglected). In this case, temperature will be described by a set of 3 equations (Eqq. 1a-b-c), every one of which will be used in a particular part of the day. When the assumption of the clear-sky day is respected, it is possible to see that this model will calculate a very accurated daily temperature (Fig. 2, [same paper](https://link.springer.com/article/10.1007/s00484-017-1471-5)), so that a simulation based on this kind of external temperature will be not far from an every-day life situation.
In order to calculate the clear-sky temperature of a day, we need to set the following parameters:

- ***T<sub>max***: the maximum temperature of the day
- ***T<sub>min***: the minimum temperature of the day
- Sunrise and sunset times: this times are a function of the day of the year and of the location, and can be found in calendars
- ***a***: lag coefficient for ***T<sub>max*** from noon (set to 2.71)
- ***b***: night-time temperature decay coefficient (set to 3.14)
- ***c***: time lag for ***T<sub>min*** from sunrise (set to 0.75)
