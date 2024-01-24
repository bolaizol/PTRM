########################################################################
#
# Created by B. Olaizola, IEM-CSIC
# Based on codes by L. Hardwidge, from U. York
#
# Date: 12/01/2024
#
########################################################################

import subprocess
import os
import parameters #we import the file with the parameters we will use

# initialise main parameters. They are taken from parameters.py, so edit that file and rerun everything for changes
name = parameters.name
A = parameters.A

#Import paths of directories
results_dir=parameters.results_dir
# Create variable pointing to the folder with the data
folder_path = os.path.join(results_dir, f"{name}{A}")
raw_folder_path = os.path.join(folder_path, 'Raw')

def gampn(name, A, Z, beta2, gamma, nneupr, parity, s, chsi):
    # create new text file, enter the required inputs for the program and then close before any other actions
    input_file = open(f"gam_in.txt", "w+")
    input_file.write(f"""'FOR002.DAT' 'FOR016.DAT' 'FOR017.DAT'
1,0,0
9,{nneupr}
0.120,0.00,0.120,0.00
0.120,0.00,0.120,0.00
0.105,0.00,0.105,0.00
0.090,0.30,0.090,0.25
0.065,0.57,0.070,0.39
0.060,0.65,0.062,0.43
0.054,0.69,0.062,0.34
0.054,0.69,0.062,0.26
0.054,0.69,0.062,0.26
0
0.054,0.69,0.062,0.26
0,1,1,0
5.0,7.0
{parity}15 {s-7} {s-6} {s-5} {s-4} {s-3} {s-2} {s-1} {s} {s+1} {s+2} {s+3} {s+4} {s+5} {s+6} {s+7}
{parity}15 {s-7} {s-6} {s-5} {s-4} {s-3} {s-2} {s-1} {s} {s+1} {s+2} {s+3} {s+4} {s+5} {s+6} {s+7}
{Z},{A}
{beta2},{gamma},0,0,0,8,8,0,0""")
    input_file.close()
    
    # run the GAMPN.exe program with input file
    program = r"gampn"
    target_file = f"gam_in.txt"
    subprocess.run([program, target_file], capture_output=True, text=True)
 
    # rename and move the input and output file for file organisation and to avoid overwriting and deleting
    output_file_name = f"({parity}) g={gamma} b={beta2} c={chsi} gampn_out.txt"
    input_file_name = f"({parity}) g={gamma} b={beta2} c={chsi} gampn_in.txt"
    os.rename("GAMPN.out", os.path.join(raw_folder_path, output_file_name))#The .out file is created in the directory where the script was called, then moved to a new destination.
    os.rename("gam_in.txt", os.path.join(raw_folder_path, input_file_name))#The .in file is created in the directory where the script was called, then moved to a new destination.
    
        
def asyrmo(name, A, Z, beta2, gamma, e2plus, parity, s, gn0, gn1, ipair, chsi):
    # create new text file, enter the required inputs for the program and then close before any other actions
    input_file = open(f"asy_in.txt", "w+")
    input_file.write(f"""'FOR016.DAT' 'FOR017.DAT' 'FOR018.DAT'
1,0
1,0
0,4,4,8,0,0                    VMI,NMIN,NMAX,IARCUT,A00,STIFF
{Z},{A},1,29,29,{e2plus},0.0
{gn0},{gn1},{ipair},{chsi},1.0
{parity}15 {s-7} {s-6} {s-5} {s-4} {s-3} {s-2} {s-1} {s} {s+1} {s+2} {s+3} {s+4} {s+5} {s+6} {s+7}
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 """)
    input_file.close()
    
    # run the ASYRMO.exe program with input file
    program = r"asyrmo"
    target_file = f"asy_in.txt"
    subprocess.run([program, target_file], capture_output=True, text=True)
    
    # rename and move the input and output file for file organisation and to avoid overwriting and deleting
    output_file_name = f"({parity}) g={gamma} b={beta2} c={chsi} asyrmo_out.txt"
    input_file_name = f"({parity}) g={gamma} b={beta2} c={chsi} asyrmo_in.txt"
    os.rename("ASYRMO.out", os.path.join(raw_folder_path, output_file_name))#The .out file is created in the directory where the script was called, then moved to a new destination.
    os.rename("asy_in.txt", os.path.join(raw_folder_path, input_file_name))#The .in file is created in the directory where the script was called, then moved to a new destination.
        
def probamo(name, A, Z, beta2, gamma, parity, chsi):

    # create new text file, enter the required inputs for the program and then close before any other actions
    input_file = open(f"prob_in.txt", "w+")
    input_file.write(f"""'FOR017.DAT' 'FOR018.DAT'
1,0
1
{Z},{A}
0,2300,0,0.65,-1
0.0,0.0,0.0,0.0""")
    input_file.close()
    
    # run the PROBAMO.exe program with input file
    program = r"probamo"
    target_file = f"prob_in.txt"
    subprocess.run([program, target_file], capture_output=True, text=True)
 
    # rename and move the input and output file for file organisation and to avoid overwriting and deleting
    output_file_name = f"({parity}) g={gamma} b={beta2} c={chsi} probamo_out.txt"
    input_file_name = f"({parity}) g={gamma} b={beta2} c={chsi} probamo_in.txt"
    os.rename("PROBAMO.out", os.path.join(raw_folder_path, output_file_name))#The .out file is created in the directory where the script was called, then moved to a new destination.
    os.rename("prob_in.txt", os.path.join(raw_folder_path, input_file_name))#The .in file is created in the directory where the script was called, then moved to a new destination.
           
        
