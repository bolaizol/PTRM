########################################################################
#
# Created by B. Olaizola, IEM-CSIC
# Based on codes by L. Hardwidge, from U. York
#
# Date: 12/01/2024
#
########################################################################

All these scripts are very rough, the code has not been optimized and several unnecesary checks remain.

This is a very rough manual for the very rough scripts written to extract the results of the PTRM calculations (and the python scripts to automatically run them).

The main script is PTRM.py, that runs the calculations mapping the phase space of beta2, gamma and chsi (quadrupole deformation, triaxiality and the Coriolis attenuation). There is a README on how to run those codes elsewhere. The output of those calculations will be stored in a */Results/isotope_name/Raw_core_employed/*_out.txt. Each set of parameters will produce a different output file. Thus, to plot the evolution of the results with deformation, a different set of scripts has been written. They are quite rough, but they get the job done.

+++ chi_squared{Aisotope}.py

The group of scripts called chi_squaredXXX.py (where XXX will be, for example, the name of the isotope) are used to extract a subset of results from the output files and write them in a single txt file. Things to consider:

	- It extracts some variables from the parameters.py script, so make sure that it is edited to your liking. Some example:
		+ Limits on the deformation parameters that have been calculated
		+ Extrictly speaking, a completely different parameters file could be written, in case that the analysis and the calculations are running different isotopes
		
	- Edit variable core_var to specify which core was used in the calculations you want to analyze. core_var=2 i.e. 1=Grodzins, 2=Hg and 3=Pb
	
	- PTRM calculations can calculate more than one level for each spin (i.e. the first three 1/2- states, for instance). This programe keeps track of which 1/2 state you are extracting information from, so the second 1/2 does not overwrite the infor of the first 1/2 state.
	
	- Since there are 3 parameters (beta2, gamma, chsi), it would require a 3D histogram to plot them, which is unrealistic. For this reason, in this script you chose a slize of chsi and plot the variation as a function of beta2 and gamma. Make sure to edit chsi to the one you want. If you don´t know what chsi is, just use chsi=1.0
	
	- The output file will have two columns with all the (gamma, beta2) pairs. The rest of the columns will contain the different variables to be plotted later
	- Some can output variable can be straight forward, such as the energy of the level or the spin of the g.s.. Others, can be more ellaborated, such the chi square of the energy difference between some experiment and calculated levels. Hardcoded limits can be impossed to this variables for easier plotting.
	

+++ {Aisotope}_plot_lvl.py

This script takes the output txt file from chi_squaredXXX.py to plot one of its variables in a heat map with polar coordinates.

	- Edit the "data" variable to point to the chi_squaredXXX.py output txt file
	
	- Edit "values" to the proper column in the data file.
	
	- It also draws a yellow star for the minimum value (other than (0,0)).
	
	- This script is much simpler than {Aisotope}_plot_trans.py. The reader is referred to that one for a more robuts plotting


+++ transitions_{Aisotope}.py

This scripts is basically identical to chi_squaredXXX.py, but it is used to extract the transition rates instead of the energy levels.

	- It extracts some variables from the parameters.py script, so make sure that it is edited to your liking. Some example:
		+ Limits on the deformation parameters that have been calculated
		+ Extrictly speaking, a completely different parameters file could be written, in case that the analysis and the calculations are running different isotopes
		
	- Edit variable core_var to specify which core was used in the calculations you want to analyze. core_var=2 i.e. 1=Grodzins, 2=Hg and 3=Pb
		
	- Edit the experimental (or literature) values you want your calcaultion values to compare to. You can adjust the number os sigmas that will be plotted.
	
	- In the current version, this script will only extract the transition rates of one level.
		+ The variable "first" makes sure we only check the first level of a given spin. If first is set to a higher value first=2,3... second, third of later levels can be checked.
		+ Variable "limits" can be set = True (to set limits on the output variable) or False
		
	- The output file will have two columns with all the (gamma, beta2) pairs. The rest of the columns will contain the different variables to be plotted later
	- Some can output variable can be straight forward, such as B(M1), B(E2) or mising ratio delta. Others, can be more ellaborated, such as the chi square to minimize the B(XL) difference
	

+++ {Aisotope}_plot_trans.py

This script will take the output of transitions_{Aisotope}.py as an input and plot as a heat map in polar coordinated.

	- Edit the "data" variable to point to the transitions_{Aisotope}.py output txt file
		
	- Edit variable core_var to specify which core was used in the calculations you want to analyze. core_var=2 i.e. 1=Grodzins, 2=Hg and 3=Pb
	
	- Edit variable "trans". It should point to the column you wan to plot. By default #trans variable M1=2, E2=3, delta=4, chi²_tot=5 . It is used to write some text later, so if variables were not written in that order in the transitions_{Aisotope}.py script, this will need some editing.
	
	- The script uses contour and polar coordinates to plot your variable set in trans as a function of (gamma, beta2) values.
	
	- It also draws a yellow star for the minimum value (other than (0,0)).
	
	- It is plotted to screen and to a pdf file
		
