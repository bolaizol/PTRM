########################################################################
#
# Created by B. Olaizola, IEM-CSIC
# Based on codes by L. Hardwidge, from U. York
#
# Date: 12/01/2024
#
########################################################################

########################################################################
#
#This is the main script to automate PTRM calculations. It needs of two other scripts, ptrm_programs.py and parameters.py
#Paramaters.py contains all the parameters that the calculations will use. Thatś the one you have to edit
#ptrm_programs.py calls the actual PRTM programs. It may need light editting, like the path to where the programs are installed, but not much more. I may move those paths to parameters.py at some point.
#You will also need other scripts to automatically extract and plot the results. Those are discussed in a separated document. As of now, those other plotting scripts also take values from the parameters.py script!!!
#
########################################################################

import parameters #we import the file with the parameters we will use
import ptrm_programs #to call this other script part of the analysis chain
import decimal #needed later
import os #to use bash commands
import time #to estimate how long it will take to run

#Import paths of directories
results_dir=parameters.results_dir

# initialise main parameters. They are taken from parameters.py, so edit that file and rerun everything for changes
name = parameters.name
Z = parameters.Z
N = parameters.N
A = parameters.A
potential = parameters.potential
e2plus_estimate = parameters.e2plus_estimate
e2plus = parameters.e2plus

# intialise range and increments of beta and gamma deformation parameters and chsi attenuation. They are taken from parameters.py, so edit that file and rerun everything for changes
beta2_min = parameters.beta2_min
beta2_max = parameters.beta2_max
beta2_delta = parameters.beta2_delta
gamma_min = parameters.gamma_min
gamma_max = parameters.gamma_max
gamma_delta = parameters.gamma_delta
chsi_min = parameters.chsi_min
chsi_max = parameters.chsi_max
chsi_delta = parameters.chsi_delta

# calculate other parameters required for PTRM code
nneupr = parameters.odd(N)[0] # odd nucleon parameter for MO
ifonly = parameters.odd(N)[1] # odd nucleon parameter for WS
sp_state = parameters.sp_state(Z, N) # single particle state of odd nucleon to setup basis upon
gn0 = parameters.pf(Z, N, A, potential)[0] # pairing strength gn0
gn1 = parameters.pf(Z, N, A, potential)[1] # pairing strength gn1
ipair = parameters.pf(Z, N, A, potential)[2] # extra pairing parameter ipair

# fix floating point error precision errors using decimal module
beta2__min = decimal.Decimal(f"{beta2_min}")
beta2__delta = decimal.Decimal(f"{beta2_delta}")
beta2__max = decimal.Decimal(f"{beta2_max}")
gamma__min = decimal.Decimal(f"{gamma_min}")
gamma__delta = decimal.Decimal(f"{gamma_delta}")
gamma__max = decimal.Decimal(f"{gamma_max}")
chsi__min = decimal.Decimal(f"{chsi_min}")
chsi__delta = decimal.Decimal(f"{chsi_delta}")
chsi__max = decimal.Decimal(f"{chsi_max}")

# Create folder and text file ready for results to be added
folder_path = os.path.join(results_dir, f"{name}{A}")
raw_folder_path = os.path.join(folder_path, 'Raw')
if not os.path.exists(folder_path):#We check if this specific results folder exists, and if not we create it
    os.makedirs(folder_path)
if os.path.exists(folder_path):#The results may exist, but not contain a Raw/ folder
	if not os.path.exists(raw_folder_path):
		os.makedirs(raw_folder_path)

    
#Counter to see if the calculations progress and estimate the time
n_beta=(beta2__max-beta2__min)/beta2__delta
n_gamma =(gamma__max-gamma__min)/gamma__delta
n_chsi =(chsi__max-chsi__min)/chsi__delta
n_max = int((n_beta+1)*(n_gamma+1)*(n_chsi+1))
n=0
    
# a loop to run the PTRM programs over several deformations and both parities.
total_tic = time.perf_counter()
chsi=chsi__min
while chsi <= chsi__max:
	gamma=gamma__min
	while gamma <= gamma__max:
    		beta2 = beta2__min
    		while beta2 <= beta2__max:
        		###########This is a counter to estimate how long it take to run the code##########
        		if(beta2__min==0):
        			if ((gamma == gamma__min) and (beta2==beta2__min+beta2__delta) and (beta2!=0)):
        				tic = time.perf_counter()
        		else:
        			if ((gamma == gamma__min) and (beta2==beta2__min) and (beta2!=0)):
        				tic = time.perf_counter()
        		##^^^^^^^^^^^^^^Ênd of time counter^^^^^^^^^##########################
        		if beta2 == 0:
            			pass
        		else:
            			if e2plus_estimate== "gro":#For the Grodzins' approximation
            				e2plus = 1225./(float(beta2)**2*A**(7/3))
            			elif e2plus_estimate== "core":#To take a neighbouring even-even as core
            				pass
            			for parity in ["+", "-"]:
                			if potential == "mo":
                    				ptrm_programs.gampn(name, A, Z, beta2, gamma, nneupr, parity, sp_state, chsi)
                    				ptrm_programs.asyrmo(name, A, Z, beta2, gamma, e2plus, parity, sp_state, gn0, gn1, ipair, chsi)
                    				ptrm_programs.probamo(name, A, Z, beta2, gamma, parity, chsi)
                			elif potential == "ws":
                    				ptrm_programs.swgamma(name, A, Z, beta2, gamma, N, ifonly, parity, chsi)
                    				ptrm_programs.wsdcup(name, A, beta2, gamma, parity, sp_state, chsi)
                    				ptrm_programs.asyrws(name, A, Z, beta2, gamma, e2plus, parity, sp_state, gn0, gn1, ipair, chsi)
                    				ptrm_programs.probaws(name, A, Z, beta2, gamma, parity, chsi)
                			else:
                    				raise ValueError("potential must be mo or ws")
        		###########This is a counter to estimate how long it take to run the code##########
        		if(beta2__min==0):
        			if ((gamma == gamma__min) and (beta2==beta2__min+beta2__delta) and (beta2!=0)):
        				toc = time.perf_counter()
        				print(f"Estimated total time: {(toc - tic)*n_max:0.1f} seconds. Real time is usually ~25% longer than estimated.")
        		else:
        			if ((gamma == gamma__min) and (beta2==beta2__min) and (beta2!=0)):
        				toc = time.perf_counter()
        				print(f"Estimated total time: {(toc - tic)*n_max:0.1f} seconds. Real time is usually ~25% longer than estimated.")
        		##^^^^^^^^^^^^^^Ênd of time counter^^^^^^^^^##########################
        		print("Progress: ", n,"/",n_max, end='\r', flush=True)
        		n=n+1
        		beta2 += beta2__delta
    		gamma += gamma__delta
	chsi += chsi__delta
    
total_toc = time.perf_counter()
print(f"Real total time: {total_toc - total_tic:0.1f} seconds")
    
