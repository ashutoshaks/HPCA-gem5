import os
import sys
import itertools
import subprocess
import logging
import argparse

# Parameters
LQEntries = [32, 64]
SQEntries = [32, 64]
l1d_size = ['32kB', '64kB']
l1i_size = ['8kB', '16kB']
l2_size = ['256kB', '512kB']
bp_type = ['TournamentBP', 'BiModeBP']
numROBEntries = [128, 192]
numIQEntries = [16, 64]

# Create a list of all possible combinations of parameters
params = [LQEntries, SQEntries, l1d_size, l1i_size,
          l2_size, bp_type, numROBEntries, numIQEntries]
param_combinations = list(itertools.product(*params))
param_titles = ['LQEntries', 'SQEntries', 'l1d_size', 'l1i_size',
                'l2_size', 'bp_type', 'numROBEntries', 'numIQEntries']

parser = argparse.ArgumentParser(
    description='Simulating all 256 configurations.')
parser.add_argument('-g', type=str, default='~/gem5',
                    help='Path to the gem5 directory.')
options = parser.parse_args()
gem5_dir = os.path.expanduser(options.g)

# Create a directory to store the results
result_dir = os.path.join(gem5_dir, 'configs/assignment/results')
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# The log file helps to identify which simulations have been completed
log_file = os.path.join(gem5_dir, 'configs/assignment/simulate.log')
if not os.path.exists(log_file):
    open(log_file, 'w').close()

# Store the completed simulations in a set
completed_params = set()
with open(log_file, 'r') as f:
    for line in f:
        completed_params.add(line.strip())


logging.basicConfig(filename=log_file, format='%(message)s',
                    level=logging.INFO, filemode='a')
logger = logging.getLogger()

# Run simulations with all possible combinations of parameters
counter = 1
for param in param_combinations:
    # Create a directory to store the results for this combination of parameters
    outdir = '-'.join(str(x) for x in param)
    if outdir in completed_params:
        continue

    print(f'Running simulation {counter} with parameters:', flush=True)
    print(', '.join(f'{x}: {y}' for x, y in zip(
        param_titles, param)), flush=True)
    print()

    # Run the simulation
    cmd = f'''{gem5_dir}/build/X86/gem5.opt \
            --outdir={result_dir}/{outdir} \
            {gem5_dir}/configs/assignment/config.py \
            -b {gem5_dir}/configs/assignment/qsort3 \
            --LQEntries={param[0]} \
            --SQEntries={param[1]} \
            --l1d_size={param[2]} \
            --l1i_size={param[3]} \
            --l2_size={param[4]} \
            --bp_type={param[5]} \
            --numROBEntries={param[6]} \
            --numIQEntries={param[7]}'''
    ret = subprocess.run(cmd, shell=True, check=True)
    print(
        f'Simulation completed with return code {ret.returncode}', flush=True)

    # Log the completed simulation
    if ret.returncode == 0:
        logger.info(outdir)
        counter += 1
