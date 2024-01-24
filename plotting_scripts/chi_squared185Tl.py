import decimal
import numpy as np
import sys
sys.path.append('/home/bruno/experiments/ISOLDE/Tl-neutron-deficient/Calculations/Particle-Rotor/Scripts')  # Modify the path accordingly to your parameters.py script
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
chsi_min = parameters.chsi_min
chsi_max = parameters.chsi_max
chsi_delta = parameters.chsi_delta

# fix floating point error precision errors using decimal and fix undefined error of chi values

beta2__min = decimal.Decimal(f"{beta2_min}")
beta2__delta = decimal.Decimal(f"{beta2_delta}")
beta2__max = decimal.Decimal(f"{beta2_max}")
gamma__min = decimal.Decimal(f"{gamma_min}")
gamma__delta = decimal.Decimal(f"{gamma_delta}")
gamma__max = decimal.Decimal(f"{gamma_max}")

######## Which core did you use for the calculations: 1 for Grodzins, 2 for Hg and 3 for Pb:
core_var=2 #1=Grodzins, 2=Hg and 3=Pb
if core_var==1:
	core='Grodzins'
if core_var==2:
	core='Hg_core'
if core_var==3:
	core='Pb_core'

###empty variable for chi² and literature values
n_levels=7 ##number of levels to be compared, including the g.s.
chiT=0.0
chi = np.zeros((n_levels,3))
chi = np.full((n_levels, 3), -1.0) #fills them with -1.0, so we can skip them if we do not assign any values
ene_exp = np.zeros((n_levels,3))
ene_exp = np.full((n_levels, 3), -1.0) #fills them with -1.0, so we can skip them if we do not assign any values
spin=["" for x in range(n_levels)]
ene=0.0 #variable to store energies


# set values for the expected (experimental) values of excitation energies
#First column the lowest energy for a given spin, second for the next energy and 3rd for the highest one (the code only computes 3)
#Leave -1.0 (or any negative number) for levels you don´t want/have the energy
ene_exp[0,:] = [0.0, -1.0, -1.0] # g.s. is the 1/2+
ene_exp[1] = [286.0, -1.0, -1.0] # expected 1st excited state is 3/2+ ited state is 3/2+ 
ene_exp[2] = [-1.05, -1.0, -1.0] # expected 2nd excited state is 5/2+
ene_exp[3] = [-1.0, -1.0, -1.0] # expected 3rd excited state is 7/2+
ene_exp[4] = [-1.0, -1.0, -1.0] # expected 4th excited state is 9/2+
ene_exp[5] = [-1.0, -1.0, -1.0] # expected 5th excited state is 11/2- first negative parity
ene_exp[6] = [-1.0, -1.0, -1.0] # expected 6th excited state is 15/2-

#Vector containing the spins of the levels listed above:
spin[0] = '1/2+'
spin[1] = '3/2+'
spin[2] = '5/2+'
spin[3] = '7/2+'
spin[4] = '9/2+'
spin[5] = '11/2-'# first negative parity
spin[6] = '15/2-'
# a loop to process through each beta and gamma asyrmo output
# within this is a loop to search for the observed excitation energies of each state and calculate chi-sqaured
# this is done twice to include both positive and negative parity output files

#Counter to see if the calculations progress and estimate the time
n_beta=(beta2__max-beta2__min)/beta2__delta
n_gamma =(gamma__max-gamma__min)/gamma__delta
n_max = int((n_beta+1)*(n_gamma+1))
counter=0

gs_spin =0#variable to hold the g.s. spin

#output file where results will be written to
results = open(f"ChiSquared.txt", "w+")

chsi='0.70' #This is the attenuation factor. For now I don't want to interate over it, just look at it one by one

gamma=gamma__min
while gamma <= gamma__max:
    beta2 = beta2__min
    while beta2 <= beta2__max:
        if beta2 == 0:
            pass
        else:
            flag = np.zeros(n_levels)#This flag makes sure that we are only looking at the first state of each spin (the calculations obtain 3 for each spin)
            # Convert the array values to integers
            flag = flag.astype(int)
            path = f"{results_dir}/{name}{A}/Raw-{core}/(+) g={gamma} b={beta2} c={chsi} asyrmo_out.txt"
            file1 = open(path,'r')
            lines = file1.readlines() # splits each file into a list of lines
            levels = np.empty((0,), dtype=[('spin', 'U10'), ('energy', float)])#array to store all the levels across both parities to find the true g.s.
            level_count=0
            for n in lines: # loop through each line to find lines of interest
                words = n.split() # splits each line to a list of words
                if len(words)>3 and (words[0] == "I=") and (words[2] == "(1)"):
                    try:
                        energy=float(words[3])
                    except ValueError:
                        print(f"Unable to convert levels to a float at index 3")
                    new_level=np.array([(words[1],float(energy))], dtype=[('spin', 'U10'), ('energy', float)])
                    if not levels.size:  # Check if 'levels' is empty
                    	levels = new_level
                    else:
                    	levels = np.vstack((levels, new_level))
                if len(words) < 16: # skip lines of no interest (speeds up computation)
                    pass
                else:
                    for i in range(0,n_levels):
                    	if (words[2] == spin[i]) and (ene_exp[i,flag[i]]>=0):
                    		if ene_exp[i,flag[i]]==0.0:
                        		chi[i,flag[i]] = ((float(words[1])+ene_exp[0,0]) - ene_exp[i,flag[i]]) ** 2 / 1. #If we are dealing with the g.s., this is trouble
                        		flag[i]+=1
                    		elif ene_exp[i,flag[i]]!=0.0:
                        		chi[i,flag[i]] = ((float(words[1])+ene_exp[0,0]) - ene_exp[i,flag[i]]) ** 2 / ene_exp[i,flag[i]]
                        		flag[i]+=1
                    	if (words[2] == '3/2+') and (flag[1]==0): ##Cheap hack to look for the energy of the first 3/2+ state
                    		ene=words[1]
                    		if float(ene)>350.:
                    			ene = 350.
                    		if float(ene)<200.:
                    			ene = 200.
                   
            
            path = f"{results_dir}/{name}{A}/Raw/(-) g={gamma} b={beta2} c={chsi} asyrmo_out.txt"   
            file2 = open(path,'r')
            lines = file2.readlines()
            for n in lines:
            	words = n.split()
            	if len(words)>3 and (words[0] == "I=") and (words[2] == "(1)"):
            		try:
            			energy=float(words[3])
            		except ValueError:
            			print(f"Unable to convert levels to a float at index 3")
            		new_level=np.array([(words[1],float(energy))], dtype=[('spin', 'U10'), ('energy', float)])
            		if not levels.size:  # Check if 'levels' is empty
            			levels = new_level
            		else:
            			levels = np.vstack((levels, new_level))
            		#levels = np.vstack((levels,(words[1],float(energy))))
            	if len(words) < 16:
            		pass
            	else:
                        if (words[2] == spin[5]) and (flag[5]==0):
                            #chi[5] = ((float(words[1])+ene_exp[5]) - ene_exp[5]) ** 2 / ene_exp[5]
                            flag[5]+=1
                        elif (words[2] == spin[6]) and (flag[6]==0):
                            #chi[6] = ((float(words[1])+ene_exp[5]) - ene_exp[6]) ** 2 / ene_exp[6]
                            flag[6]+=1
            
            
            levels['energy'] = levels['energy'].astype(float)
    
                
            # Find the index of the minimum energy value
            min_energy_index = np.argmin(levels['energy'])
            # Retrieve the corresponding spin and energy values
            gs_spin_str = str(levels[min_energy_index]['spin'])  # Ensure gs_spin_str is a string
            # Remove the last three characters from gs_spin_str
            gs_spin_str = gs_spin_str[2:-5]
            # Convert the remaining string to a float
            gs_spin = float(gs_spin_str)
            gs_energy = levels[min_energy_index]['energy']
            
            
            #chiT = chi[0,0] + chi[1,0] + chi[2,0] + chi[3,0] + chi[4,0]
            chiT = chi[0,0] + chi[1,0]
            
            dof=0.#variable for the degrees of freedom
            for n in range(n_levels):
            	for m in range(flag[n]):
            		if chi[n,m]>=0.0:
            			chiT=chiT+chi[n,m]
            			dof+=1.
            
            if chiT>1000. :
            	chiT=1000.
            #else:
            	#chiT=chiT/dof
                
	# write into new line in the results file
        #results.write(f"""{gamma} {beta2} {"%.3f" % chiT} {"%.3f" % chi[1]} {"%.3f" % chi[2]} {"%.3f" % chi[3]} {"%.3f" % chi[4]} {"%.3f" % chi[5]} {"%.3f" % chi[6]} {"%.3f" % chi7} {"%.3f" % chi8}""")
        results.write(f"""{gamma} {beta2} {ene} {"%.3f" % chiT} {gs_spin} \n""")
        #counter to see some progress
        print("Progress: ", counter,"/",n_max, end='\r', flush=True)
        counter += 1
        
        beta2 += beta2__delta
    gamma += gamma__delta
    
results.close()
