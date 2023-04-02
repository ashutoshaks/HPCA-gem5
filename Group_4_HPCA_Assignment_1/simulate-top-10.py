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

param_combinations = [
    (32, 64, '64kB', '16kB', '512kB', 'TournamentBP', 192, 64),
    (32, 64, '64kB', '16kB', '256kB', 'TournamentBP', 192, 64),
    (32, 64, '32kB', '16kB', '256kB', 'TournamentBP', 192, 64),
    (64, 64, '64kB', '16kB', '512kB', 'TournamentBP', 192, 64),
    (64, 64, '32kB', '16kB', '512kB', 'TournamentBP', 192, 64),
    (32, 64, '32kB', '16kB', '512kB', 'TournamentBP', 192, 64),
    (64, 64, '64kB', '16kB', '256kB', 'TournamentBP', 192, 64),
    (64, 64, '32kB', '16kB', '256kB', 'TournamentBP', 192, 64),
    (32, 64, '64kB', '16kB', '512kB', 'TournamentBP', 128, 64),
    (32, 64, '64kB', '16kB', '256kB', 'TournamentBP', 128, 64)
]
param_titles = ['LQEntries', 'SQEntries', 'l1d_size', 'l1i_size',
                'l2_size', 'bp_type', 'numROBEntries', 'numIQEntries']

parser = argparse.ArgumentParser(
    description='Simulating the top 10 configurations.')
parser.add_argument('-g', type=str, default='~/gem5',
                    help='Path to the gem5 directory.')
parser.add_argument('--rank', type=int, default=-1,
                    help='Rank of the configuration to simulate.')
options = parser.parse_args()
gem5_dir = os.path.expanduser(options.g)

# Create a directory to store the results
result_dir = os.path.join(gem5_dir, 'configs/assignment/top-10-results')
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# Run simulations with all possible combinations of parameters
for i, param in enumerate(param_combinations):
    if options.rank != -1 and options.rank != i + 1:
        continue

    # Create a directory to store the results for this combination of parameters
    outdir = f'rank-{(i + 1):02d}-' + ('-'.join(str(x) for x in param))

    print('Running simulation with parameters:', flush=True)
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
