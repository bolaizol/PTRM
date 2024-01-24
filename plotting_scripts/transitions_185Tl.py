import decimal
import numpy as np
import sys
sys.path.append('/home/bruno/experiments/ISOLDE/Tl-neutron-deficient/Calculations/Particle-Rotor/Scripts')  # Modify the path accordingly to your parameters script
import parameters

# initialise main parameters

#Import paths of directories
results_dir=parameters.results_dir

# initialise main parameters. They are taken from parameters.py, so edit that file and rerun everything for changes
name = parameters.name
Z = parameters.Z
N = parameters.N
A = parameters.A
potential = parameters.potential
e2plus = parameters.e2plus

# intialise range and increments of beta and gamma deformation parameters. They are taken from parameters.py, so edit that file and rerun everything for changes
beta2_min = parameters.beta2_min
beta2_max = parameters.beta2_max
beta2_delta = parameters.beta2_delta
gamma_min = parameters.gamma_min
gamma_max = parameters.gamma_max
gamma_delta = parameters.gamma_delta

# fix floating point error precision errors using decimal and fix undefined error of chi values

beta2__min = decimal.Decimal(f"{beta2_min}")
beta2__delta = decimal.Decimal(f"{beta2_delta}")
beta2__max = decimal.Decimal(f"{beta2_max}")
gamma__min = decimal.Decimal(f"{gamma_min}")
gamma__delta = decimal.Decimal(f"{gamma_delta}")
gamma__max = decimal.Decimal(f"{gamma_max}")

######## Which core did you use for the calculations: 1 for Grodzins, 2 for Hg and 3 for Pb:
core_var=1 #1=Grodzins, 2=Hg and 3=Pb
if core_var==1:
	core='Grodzins'
if core_var==2:
	core='Hg_core'
if core_var==3:
	core='Pb_core'

#Literature values:
BE2_lit=29.9 #W.u.
BE2_lit_error=3.4
BM1_lit=0.69 #mW.u.
BM1_lit_error=0.1
delta_lit = +0.66
delta_lit_error = 0.06

##Errors and limits: 
sigma=3. ##Number of sigmas you want to use in the error bars, by default 1
BE2_lim_sup=(BE2_lit+sigma*BE2_lit_error)/BE2_lit
BE2_lim_bot=(BE2_lit-sigma*BE2_lit_error)/BE2_lit


# a loop to process through each beta and gamma asyrmo output
# within this is a loop to search for the observed excitation energies of each state and calculate chi-sqaured
# this is done twice to include both positive and negative parity output files

#Counter to see if the calculations progress and estimate the time
n_beta=(beta2__max-beta2__min)/beta2__delta
n_gamma =(gamma__max-gamma__min)/gamma__delta
n_max = int((n_beta+1)*(n_gamma+1))
counter=0

#output file where results will be written to
results = open(f"{A}{name}_transitions.txt", "w+")

chsi='1.00' #This is the attenuation factor. For now I don't want to interate over it, just look at it one by one

gamma=gamma__min
while gamma <= gamma__max:
    beta2 = beta2__min
    while beta2 <= beta2__max:
        BM1=0.0 #Variable to hold the magnetic moment
        BE2=0.0 #variable to hold the quadrupole moment
        delta=0.0 #variable to hold the mixing ratio
        if beta2 == 0:
            pass
        else:
            path = f"{results_dir}/{name}{A}/Raw-{core}/(+) g={gamma} b={beta2} c={chsi} probamo_out.txt"
            file1 = open(path,'r')
            lines = file1.readlines() # splits each file into a list of lines
            first=0 #We are only interested in the first 3/2+ --> 1/2+ transition, so we flag it with this variable.
            for n in lines: # loop through each line to find lines of interest
                words = n.split() # splits each line to a list of words
                if len(words) < 5: # skip lines of no interest (speeds up computation)
                    pass
                else:
                    if (words[1] == "3/2") and (words[3] == "0.0") and (words[4] == "1/2"):
                    	first +=1
                    	if first==1: #We make sure it is the first 3/2+ --> 1/2+ transition
                        	BM1=float(words[8])
                        	BE2=float(words[6])
                        	delta=float(words[10])
        
        
        #Limits for the B(E2) and B(M1) values
        limits = True #variable to turn on and off the truncation of values
        if limits:
        	if BE2>(BE2_lit+sigma*BE2_lit_error):
        		BE2=BE2_lit+sigma*BE2_lit_error
        	if BE2<(BE2_lit-sigma*BE2_lit_error):
        		BE2=BE2_lit-sigma*BE2_lit_error
        	if BM1>(BM1_lit+sigma*BM1_lit_error):
        		BM1=BM1_lit+sigma*BM1_lit_error
        	if BM1<(BM1_lit-sigma*BM1_lit_error):
        		BM1=BM1_lit-sigma*BM1_lit_error
        	if delta>(delta_lit+sigma*delta_lit_error):
        		delta=delta_lit+sigma*delta_lit_error
        	if delta<(delta_lit-sigma*delta_lit_error):
        		delta=delta_lit-sigma*delta_lit_error
        
        	
        #Chi^2 of the transition rates and mixing ratio delta
        chi_BE2=(BE2-BE2_lit)**2/BE2_lit**2
        chi_BM1=(BM1-BM1_lit)**2/BM1_lit**2
        chi_tot=chi_BM1+chi_BE2
        if chi_tot>0.25:
        	chi_tot=0.25
        if chi_BE2>5:
        	chi_BE2=5
        if chi_BM1>1.:
        	chi_BM1=1.
        chi_delta = (delta-delta_lit)**2/delta_lit
        if chi_delta>2.:
        	chi_delta=2.
        
        
        #Ratio calculations to literature values
        limits = False #variable to turn on and off the truncation of values
        if limits:
        	if BE2>0.:
        		ratio_BE2=BE2/BE2_lit
        	else:
        		ratio_BE2=BE2_lim_bot
        	if ratio_BE2>BE2_lim_sup :
        		ratio_BE2=BE2_lim_sup
        	if ratio_BE2<BE2_lim_bot :
        		ratio_BE2=BE2_lim_bot
        
        	if BM1>0.:
        		ratio_BM1=BM1_lit/BM1
        		lim_sup=(BM1_lit+sigma*BM1_lit_error)/BM1
        		lim_down=(BM1_lit-sigma*BM1_lit_error)/BM1
        	else:
        		ratio_BM1=0.
        		lim_sup=0.1
        		lim_down=0.1
        	if ratio_BM1>lim_sup :
        		ratio_BM1=lim_sup
        	if ratio_BM1<lim_down :
        		ratio_BM1=lim_down
        
              
	# write into new line in the results file
        results.write(f"""{gamma} {beta2} {BM1} {BE2} {delta} {chi_tot}\n""")
        #results.write(f"""{gamma} {beta2} {ratio_BM1} {ratio_BE2} {delta}\n""")
        #results.write(f"""{gamma} {beta2} {chi_BM1} {chi_BE2} {chi_delta}\n""")
        #counter to see some progress
        print("Progress: ", counter,"/",n_max, end='\r', flush=True)
        counter += 1
        
        beta2 += beta2__delta
    gamma += gamma__delta
    
results.close()
