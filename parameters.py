########################################################################
#
# Created by B. Olaizola, IEM-CSIC
# Based on codes by L. Hardwidge, from U. York
#
# Date: 12/01/2024
#
########################################################################

# Import math library
import math

#Paths pointing to the programs and result folders

working_dir=''
results_dir='/home/bruno/experiments/ISOLDE/Tl-neutron-deficient/Calculations/Results'

# initialise main parameters
name = "Tl" # nucleus name used for filenames
Z = 81 # number of protons
N = 104 # number of neutrons
A = N + Z # mass number
potential = "mo" # modified oscillator = mo, woods-saxon = ws
e2plus_estimate = "gro" # e2 of neighboring even-even = core, Grodzins' estimate = gro
e2plus = 0.6624 # energy of the lowest-lying 2+ state in 186Pb
#e2plus = 0.36678 # energy of the lowest-lying 2+ state in 184Hg
#e2plus = 1225./(float(beta2)**2*A**(7/3)) # energy of the core 2+ using the Grodzin's estimate (not calculated here, it is done in PTRM.py)

# intialise range and increments of beta and gamma deformation parameters
beta2_min = 0 # starting beta2
beta2_max = 0.5 # maximum beta2
beta2_delta = 0.01 # increments of beta2
gamma_min = 0 # starting gamma
gamma_max = 60 # maximum gamma
gamma_delta = 1 # increments of gamma

# intialise range and increments of chsi Coriolis attenuation parameter
chsi_min = 0.10 # starting chsi
chsi_max = 1.0 # maximum chsi
chsi_delta = 0.05 # increments of chsi

def odd(n): # function to define the odd nucleon and tell the ptrm to calulcate for protons or neutrons
    if n % 2 == 0:
        odd_nucleon = "proton"
        ifonly = 2
        nneupr = 1
    else:
        odd_nucleon = "neutron"
        ifonly = 1
        nneupr = -1
    return nneupr, ifonly, odd_nucleon
    
def pf(z, n, a, potential): # function to set values of pairing strength parameters that depend on A and Z.
    odd_nucleon = odd(n)[2]
    if potential == "mo":
        if odd_nucleon == "proton": # modified oscillator, odd proton
            if z < 60:
                gn0 = 22.0
                gn1 = 8.0
                ipair = 5
            else:
                gn0 = 19.2
                gn1 = 7.4
                ipair = 15
        else: # modified oscillator, odd neutron
            if n < 60:
                gn0 = 22.0
                gn1 = 8.0
                ipair = 5
            else:
                gn0 = 19.2
                gn1 = 7.4
                ipair = 15
    elif potential == "ws":
        if odd_nucleon == "proton": # woods-saxon, odd proton
            ipair = z / 4
            if z < 50:
                gn0 = 17.9
                gn1 = 7.4
            elif 50 <= z < 88:
                gn0 = 17.9
                gn1 = 0.176 * a
            else:
                gn0 = 13.3
                gn1 = 0.217 * a
        else: # woods-saxon, odd neutron
            ipair = n / 4
            if z < 50:
                gn0 = 17.9
                gn1 = 7.4
            elif 50 <= z < 88:
                gn0 = 18.95
                gn1 = 0.078 * a
            else:
                gn0 = 19.3
                gn1 = 0.084 * a
    else:
        raise ValueError("potential must be mo or ws")
    return gn0, gn1, ipair
    
def sp_state(z, n): # function to find the Fermi level, to help select the Nilsson states to include in step 2
    if z % 2 == 0:
        s = math.ceil(n/4)
    else:
        s = math.ceil(z/4)
    return s
