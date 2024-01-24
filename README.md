########################################################################
#
# Created by B. Olaizola, IEM-CSIC
# Based on codes by L. Hardwidge, from U. York
#
# Date: 12/01/2024
#
########################################################################


This is a short manual to run the necesary python scripts to automate the PTRM calculations. The calculation programs were prepared by P. Semmes and I. Ragnarsson based on the particle + triaxial rotor model. The source and manuals can be acquired elswhere and will not be treated in this short guide. Suffice to say that they need to be compiled using Intel Frotran compiler. Currently, it only works for the modified oscillator potential. Some editting should allow to use it with the Wood-Saxon one.

- PTRM.py: It is the main script that will call the other subscripts.
- ptrm_programs.py: this subscript calls the different PTRM programs that actually run the calculations. The input for the calculations can be edited here.
- parameters.py: this is the subscript that needs the most editting. It contains the variables for the nucleus to be calculated, ranges of the calulcation parameters, directory paths, etc...


+++ How to run a calculation

1. After familiarizating yourself with how the PTRM code works and how the imput works, you should edit the ptrm_programs.py script:
	1.1 For instance, the script has functions to define the input files for the PTRM programs (gampn, asymo and probamo). Not that much can be editted, actually, and most often the default values will be good for your needs.
	1.2 The whole input file is a single string value in each subfuction
	1.3 Check that the input and output file names are correct for each program (default should work).
	1.4 Leave all the variables in brackets {} alone. Thos values are taken elsewhere (mainly from parameters.py). You can (and should) edit them there
	
2. The main editting will be done in parameters.py. Variables you should edit:
	2.1 working dir (currently not implemented).
	2.2 results_dir : This is the path where all the results from the calculations will be stored. Most of the directory structure is built based on this variable.
	2.3 name : This is just a name for this calculations, it is recommended to use the isotope name you are calculating, as the final name will be mass(A)+name (e.g. 185Tl)
	2.4 Z, N, A : Numer of protons, neutron and mass. A is actually Z+N
	2.5 potential : Potential employed in the caculations. It is a string like "mo" # modified oscillator = mo, woods-saxon = ws (ws not fully implemented)
	2.6 e2plus_estimate and e2plus : Energy of the 2+ of the core employed in the calculations:
		2.6.1 e2plus_estimate is a string. If you want to use the E(2+) of a neighboring even-even = 'core', for Grodzins' estimate = 'gro' 
		2.6.2 Grodzins' estimate  calculates the energy as a function of beta_2 as e2plus = 1225./(float(beta2)**2*A**(7/3)). It is calculated for each deformation in PTRM.py
		2.6.3 If you want to use the same E(2+) for all deformations, e2plus_estimate= 'core' and assign the value in variable e2plus in MeV
	2.7 The script can currently run the calculations covering the phase space of beta_2, gamma and chsi (Coriolis attenuation). All three parameters have the following variables:
		2.7.1 *_min Minimum or starting variable for this parameter
		2.7.2 *_max Maximum or final variable for this parameter
		2.7.3 *_delta Step increament for the parameter. The smaller, the more precise you will cover the whole phase space, but eventually the calculations will take too long to run
	2.8 The rest of the parameters are calculated automatically and it is advised to leave them like that.
	
3. Call PTRM.py. This will run the calculations. Take into account:
	3.1 In the current version, all three python scripts must be in the same directory
	3.2 In the current version, all PTRM programs are added to the PATH variable. Otherwise, the working_dir variable needs to be edited and implemented in ptrm_programs.py (not yet working!!!)
	3.3 The script gives a crude estimate of how long it will take to fully run. It is only precise within +/-50% or so
	3.4 The results for each set of parameters (beta2, gamma, chsi and parity) will be stored in a different folder within results_dir/name

4. A different set of scripts was written to extract and plot the results, they are covered in a different file.
