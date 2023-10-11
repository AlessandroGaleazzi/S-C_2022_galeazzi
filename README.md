# Thermal evolution of a system with negligible internal resistance

A lot of transient heat flow problems can be efficiently addressed with good accuracy if we assume that the internal conductive resistance within the studied system is negligible, ensuring that its temperature remains relatively uniform at any given moment. This simplification is legitimate when the external thermal resistance between the system's surface and the surrounding medium is significantly greater than the internal resistance, so that this last contribution can be neglected while studying the heat exchange process. The relationship between these resistances can be quantified through the their ratio, as

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

In general, it is not possible to calculate ***&tau;*** for an arbitrary thermal container with reasonable precision. On the other hand, it is possible to determine it with an exponential fit on experimental data. This kind of experiment does not require any major apparatus (a digital thermometer is enough) and allows a complete determination of the capability of a thermal container, since the only system-related quantity that we need to predict the temperature evolution of a system is its ***&tau;***.