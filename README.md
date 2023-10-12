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

# The data logger

In this project, all temperatures recordings were performed using the device "Elitech RC-5+ Reusable USB Temperature Data Logger With Auto PDF Report" ( it is possible to find more details [here](https://www.elitechus.com/collections/multi-use-temperature-data-logger/products/elitech-rc-5-pdf-usb-temperature-data-logger-32000-points-reusable)), since it possesses all the main requirements that any person interested in this kind of measurements would desire (small size, low cost, possibility to store data and export them into excel files thanks to a free software) and was precisely designed "to monitor the temperature of food, medicine, chemicals and other products in storage and transports" (from the User's Manual).
This projects contains some excel datasheets that are meant to show examples of temperature recording and use. In the folder "functions", you can find two excel datasheets:

- The file *EFI234105840_Exp_Fit.xls* contains an example of an experimental measurement of the ***&tau;*** parameter (a cold container was placed in a thermal bath)
- The file *EFI234105840_Ext_Temp_Recording.xls* contains an example of external temperature recording, from which a simulation can be performed

The project relies on this kind of input data to calculate ***&tau;*** parameters and to perform simulation based on external temperatures recordings, together with  a very particular kind of external temperature simulation (next section).

# The clear-sky model

If we want to simulate the temperature evolution of a system exposed to diurnal variation of external temperature, a good starting point is the model described in [this work](https://link.springer.com/article/10.1007/s00484-017-1471-5), in which the variation of external temperature over 24 hours is simulated according to the behaviour that it shows in so-called "clear-sky" days (a day in which the influence of clouds on the solar radiation at ground can be neglected). In this case, temperature will be described by a set of 3 equations (Eqq. 1a-b-c), every one of which will be used in a particular part of the day. When the assumption of the clear-sky day is respected, it is possible to see that this model will calculate a very accurated daily temperature (Fig. 2, [same paper](https://link.springer.com/article/10.1007/s00484-017-1471-5)), so that a simulation based on this kind of external temperature will be not far from an every-day life situation.
In order to calculate the clear-sky temperature of a day, we need to set the following parameters:

- ***T<sub>max***: the maximum temperature of the day
- ***T<sub>min***: the minimum temperature of the day
- Sunrise and sunset times: this times are a function of the day of the year and of the location, and can be found in calendars
- ***a***: lag coefficient for ***T<sub>max*** from noon (set to 2.71)
- ***b***: night-time temperature decay coefficient (set to 3.14)
- ***c***: time lag for ***T<sub>min*** from sunrise (set to 0.75)

# Structure of the project