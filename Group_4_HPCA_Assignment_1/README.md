# HPCA Assignment 1 - Group 4

## Submission Structure
```
.
├── cache.py
├── config.py
├── HPCA-Assignment-Report.pdf
├── plot.py
├── qsort3
├── qsort3.c
├── README.md
├── simulate.py
├── simulate-top-10.py
└── top-10-results
    ├── rank-01-32-64-64kB-16kB-512kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-02-32-64-64kB-16kB-256kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-03-32-64-32kB-16kB-256kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-04-64-64-64kB-16kB-512kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-05-64-64-32kB-16kB-512kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-06-32-64-32kB-16kB-512kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-07-64-64-64kB-16kB-256kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-08-64-64-32kB-16kB-256kB-TournamentBP-192-64
    │   └── stats.txt
    ├── rank-09-32-64-64kB-16kB-512kB-TournamentBP-128-64
    │   └── stats.txt
    └── rank-10-32-64-64kB-16kB-256kB-TournamentBP-128-64
        └── stats.txt
```

## Description of Files

- `cache.py` : Contains the definitions of the `L1Cache`, `L1ICache`, `L1DCache` and `L2Cache` classes.
- `config.py` : Configuration file containing the parameters and their values (for fixed parameters) for the simulations. It takes the values of the variable parameters as command-line arguments.
- `simulate.py` : Script to simulate all the 256 configuration combinations on the given benchmark.
- `simulate-top-10.py` : Script to simulate the top 10 configurations or any one of the top 10 configurations.
- `qsort3.c` : The benchmark program to be executed.
- `qsort3` : The binary of the benchmark program.
- `plot.py` : Python script to extract the top 10 configurations w.r.t. CPI and plot the various statistics asked for.
- `top-10-results` : Directory containing the `stats.txt` files of the top 10 configurations.
- `HPCA-Assignment-Report.pdf` : The report for the assignment.

## Execution Instructions

First, install and build `gem5`.  

Navigate to the `gem5` directory in your system. All the further commands assume that you are inside the `gem5` directory.  

Then, copy all files in the submission directory to `configs/assignment` inside the `gem5` directory  
```bash
mkdir -p configs/assignment
cp -r Group_4_HPCA_Assignment_1/* configs/assignment/
```  

To execute all the 256 configurations, execute the `simulate.py` file. It takes the path to the `gem5` directory as a command line argument (`-g`). This may take nearly an hour. This creates the statistics outputs in the `configs/assignment/results` directory. The name of each folder inside it is of the format `LQEntries-SQEntries-l1d_size-l1i_size-l2_size-bp_type-numROBEntries-numIQEntries`.
```bash
python configs/assignment/simulate.py -g <path-to-gem5>
```  

To execute the top 10 configurations, execute the `simulate-top-10.py` file. It takes the path to the `gem5` directory as a command line argument (`-g`). To run a specific file among the top 10 (according to the rank), you can do so using the `--rank` command-line argument.  
So, for example, to run the 1st configuration, you can do the following:  
```bash
python configs/assignment/simulate-top-10.py -g <path-to-gem5> --rank=1
```
If you do not specify the `--rank` argument, it will run all the top 10 configurations.
```bash
python configs/assignment/simulate-top-10.py -g <path-to-gem5>
```  
The results for this will be stored in `configs/assignment/top-10-results`.  

To plot the various statistics asked for, execute the `plot.py` file. It takes the path to the `gem5` directory as a command line argument (`-g`), and the path to the directory containing the results as a command line argument (`-r`). This will create the plots in the `configs/assignment/plots` directory.
```bash
python configs/assignment/plot.py -g <path-to-gem5> -r <path-to-results>
```
