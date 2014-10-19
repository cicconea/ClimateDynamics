# Climate Dynamics
# Problem Set 6
# Adriana Ciccone

import numpy as numpy
import matplotlib.pyplot as plt

# Energy Balance: dE(Earth)/dt = F(sun to earth) - OLR = C * dT/dt

# V = 1.3*10**9 # Volume of water on earth in km^3
# R = 6400.0 # Earth's radius in km
# 1.3*10^18 m^3 volume of water
# 5.14718e14 m2 area of earth
# water depth = 2525m > per square meter there are 2525 m^3 of water

C = 1.056 * 10**10 # Heat capacity = 2525 m^3 * 4.1813 J/mL*K
#C = 1 #test for now 
sigma = 5.67*10**-8 # Stefan Boltzman Constant

Eg = 0.95 # emissivity of Earth's surface
Ea = 0.9 # emissivity of atmosphere
f = 0.23 # aborption by atmosphere of incoming solar radiation

S0 = 1368.0 # incoming solar flux W/m^2
alphaBar = 0.3 # average albedo

Tmax = 296.0 # kelvin
Tmin = 277.0 # kelvin
fIceMax = 0.4 # % of world covered by ice
fIceMin = 0 # % of world covered by ice
aFree = 0.07 # albedo of ice-free regions
aIce = 0.75 # albedo of ice-covered regions

dIdT = (fIceMax - fIceMin)/(Tmin - Tmax)
atmosphereEffect = ((2-f)/(Eg*(2-Ea)))**0.25	

# Calculate solar flux as function of temperature (which affects albedo)
def solarFluxFunction(temp):
	currentAlbedo = albedo(temp)
	SolarFlux = (S0/4)*(1-currentAlbedo) 	# Average sunlight incident on earth calculated 
											# from incoming insolation and albedo
	return SolarFlux						

# Calculate Earth's albedo as function of temperature
def albedo(temp):
	if temp > Tmax: 
		icefrac = fIceMin
	elif temp < Tmin:
		icefrac = fIceMax
	else:
		icefrac = dIdT * (temp - Tmax)
	albedoT = aIce * icefrac + aFree * (1-icefrac) + 0.1
	return albedoT

# Calculate OLR as a function of surface temperature
def emitFlux(temp):
	tEmit = temp / atmosphereEffect
	return (tEmit**4) * sigma

# Calculate difference in temperature as function of incoming and outgoing flux
def TempDiffFunction(Fin, emitFlux):
	dTdt = (Fin - emitFlux)/C
	return dTdt

Tinit = 250.0 # Vary this 

albedoCalc = []		# Albedo result initialization
OLRList = [] 		# OLR flux result initialization
SolarList = []		# Solar flux result initialization
albedoTemp = range(200,400,1) # range of temps for Q1

# For question 1 - run over range of temps to calculate albedo and fluxes for plots
for t in albedoTemp:
	#print t, "; ",albedo(t)
	AofT = albedo(t)
	FinOfT = solarFluxFunction(t)
	FoutOfT = emitFlux(t)
	albedoCalc.append(AofT)
	OLRList.append(FoutOfT)
	SolarList.append(FinOfT)
	
seconds = 3.15569 * 10**7 # number of seconds in a year
# Question 2 simulation

simulationTempList = []
yearList = []
def simulation(Tinit):
	OLR = emitFlux(Tinit)
	SolarIn = solarFluxFunction(Tinit)
	dT = TempDiffFunction(SolarIn, OLR) * seconds
	simTemp = Tinit
	year = 0
	while year <= 1000:
		simTemp += dT
		OLR = emitFlux(simTemp)
		SolarIn = solarFluxFunction(simTemp)
		dT = TempDiffFunction(SolarIn, OLR) * seconds
		year += 1

		simulationTempList.append(simTemp)
		yearList.append(year)
	
	#print simulationTempList
	# Question 2 part a - plot Temp simulation
	plt.plot(yearList, simulationTempList)
	plt.title("Temperature Simulation")
	plt.ylabel("Temp (K)")	
	plt.xlabel("Year from Simulation Start")
	plt.show()


simulation(Tinit)


# Question 1 part a - plot albedo vs T
#plt.plot(albedoTemp, albedoCalc)
#plt.title("Surface Albedo as Function of Temperature")
#plt.ylabel("Albedo")
#plt.xlabel("Temp (K)")
#plt.show()

# Question 1 part b - plot OLR and FSolar as function of Temp
#plt.plot(albedoTemp, OLRList, label="OLR")
#plt.plot(albedoTemp, SolarList, label="Solar Flux")
#plt.legend()
#plt.title("Radiative Flux differences as Function of Temperature")
#plt.ylabel("Flux (W/m^2")
#plt.xlabel("Temp (K)")
#plt.show()



#We start with T0 and initial albedo. Solar influx comes in, and we calculate dTdt based on OLR
#determined by surface temp > emitting temp. In the next period, we calculate T1 by adding dTdt(0)
#to T0, adjusting albedo, and finding new solar influx. Then calculate dTdt(1) based on new OLR
#from T1 Run for a couple thousand periods and plot results. 




