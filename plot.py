# LQEntries: 32, 64
# • SQEntries: 32, 64
# • l1d size: 32kB, 64kB
# • l1i size: 8kB, 16kB
# • l2 size: 256kB, 512kB
# • bp type: TournamentBP, BiModeBP
# • ROBEntries: 128, 192
# • numIQEntries: 16, 64




# – Cycles Per Instruction (CPI). system.cpu.cpi
# – Mispredicted branches detected during execution.
# – Number of branches that were predicted not taken incorrectly.
# – Number of branches that were predicted taken incorrectly.
# – Instructions Per Cycle (IPC).
# – Number of BTB hit percentage.

# – Number of overall miss cycles - 3, miss rate - 3, average overall miss latency - 3.

# – The number of ROB accesses (read and write both) - 2
# – Number of times the LSQ has become full, causing a stall.
# – Number of loads that had data forwarded from stores.
# – Number of times access to memory failed due to the cache being blocked.


#  Total fields to read  = 20

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import re
import os
import argparse
import seaborn as sns

SAMPLE_DIRECTORY_NAME = '32-32-32kB-8kB-256kB-TournamentBP-128-16'

FILE_NAME = 'stats.txt'
PLOT_DIR = 'Plots'
parser = argparse.ArgumentParser()

parser.add_argument("-d", help="Folder containing stats for different configurations", required=True)
dir_path = vars(parser.parse_args())['d']
PARAMS_TO_RECORD = {
    'system.cpu.cpi' : 'CPI',
    'system.cpu.commit.branchMispredicts' : 'BranchMisPred',
    'system.cpu.iew.predictedNotTakenIncorrect' : 'PredNotTakenIncorrect',
    'system.cpu.iew.predictedTakenIncorrect' : 'PredTakenIncorrect',
    'system.cpu.ipc' : 'IPC',
    'system.cpu.branchPred.BTBHitRatio': 'BTBHitFraction', # need to print in % format

    'system.cpu.dcache.overallMisses::total': 'miss_cycle_dcache',
    'system.cpu.icache.overallMisses::total': 'miss_cycle_icache',
    'system.cpu.l2cache.overallMisses::total': 'miss_cycle_l2cache',

    'system.cpu.icache.overallMissRate::total': 'miss_rate_icache',
    'system.cpu.l2cache.overallMissRate::total': 'miss_rate_l2cache',
    'system.cpu.dcache.overallMissRate::total': 'miss_rate_dcache',

    'system.cpu.dcache.overallAvgMissLatency::total': 'OverallAvgMissLatD',
    'system.cpu.icache.overallAvgMissLatency::total': 'OverallAvgMissLatI',
    'system.cpu.l2cache.overallAvgMissLatency::total': 'OverallAvgMissLatL2',    

    'system.cpu.rob.reads' : 'ReadRob',
    'system.cpu.rob.writes' : 'WriteRob',

    'system.cpu.iew.lsqFullEvents' : 'StallDueToLSQFull',
    'system.cpu.lsq0.forwLoads' : 'StoreLoadFwd',
    'system.cpu.lsq0.blockedByCache' : 'MemFailedBlockedByCache',
}

OUTPUT_FIELDS = [PARAMS_TO_RECORD[k] for k in PARAMS_TO_RECORD]
assert(len(OUTPUT_FIELDS) == 20)

def extractDataForConfig(config_directory:str) -> dict:
    # dir_name = '-'.join(config)
    lines = None
    # print(dir_path,config_directory, FILE_NAME)
    file_addr = dir_path + '/' + config_directory + '/' + FILE_NAME
    with open(file_addr, 'r') as f:
        lines = [line for line in f]
    
    data = dict()
    for line in lines:
        fields = re.sub('\s+',' ',line)
        fields = fields.split(" ")
        if fields[0] in PARAMS_TO_RECORD.keys():
            data[PARAMS_TO_RECORD[fields[0]]] = float(fields[1])
    # import ipdb
    # ipdb.set_trace()
    for f in OUTPUT_FIELDS:
        if f not in data:
            print(f'{f} is not present in the file for config {config_directory}')
    assert(len(data) == len(OUTPUT_FIELDS))
    
    return data





if __name__ == '__main__':

    # Run command
    # python plot.py -d m5out
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)
    # print(extractDataForConfig('32-32-32kB-8kB-256kB-TournamentBP-128-16'.split('-')))

    all_data = {}

    
    # for config in all_configs:
    #     dir_name = '-'.join(config)
    #     all_data[dir_name] = extractDataForConfig(config)


    for subdir in os.listdir(dir_path):
        print(subdir)
        if os.path.isdir(dir_path + "/" + subdir):
            all_data[subdir] = extractDataForConfig(subdir)
    print(all_data)
    CPIs = [(all_data[cnfg]['CPI'], cnfg) for cnfg in all_data.keys()]
    CPIs.sort(key=lambda x:x[0], reverse=True)
    CPITop10 = CPIs[:10]
    Top10Configs = [cnfg[1] for cnfg in CPITop10]
    toPrint = [cnfg[1] +" - "+str(cnfg[0]) for cnfg in CPITop10]
    print('The top 10 configurations and their corresponding CPI values are')
    print('\n'.join(toPrint))
        #     # get config object from file name
        #     arg_list = subdir.split("_")
        #     config_dict = dict(zip(options, arg_list))
        #     config = Config(config_dict= config_dict)
        #     config_list.append(config)

        #     # extract info from file
        #     filename = dirpath +"/" + subdir + "/stats.txt"
        #     with open(filename, 'r') as fp:
        #         config_stats, _ = stats_extractor(fp)
        #         for key in config_stats:
        #             stats_lists[key].append(config_stats[key])
    # sort and choose top 10
    num_of_data_points = min(10, len(Top10Configs))
    x_data = list(range(1, num_of_data_points + 1))
    for key in OUTPUT_FIELDS:
        sns.set_style("darkgrid", {"grid.color": ".4", "grid.linestyle": ":"})
        plt.figure(figsize= (10, 8))

        ax = plt.gca()
        ax.yaxis.offsetText.set_visible(False)
        offset = ax.yaxis.get_major_formatter().get_offset()

        y_formatter = mticker.ScalarFormatter(useOffset=False)
        # ax.yaxis.set_major_formatter(y_formatter)
        # print(Top10Configs)
        y_data = [all_data[cnfg][key] for cnfg in Top10Configs]
        plt.plot(x_data, y_data , marker= 'o')
        plt.xlabel("configs")
        plt.ylabel(key)
        plt.xticks(x_data)
        plt.title(key + f" for top {num_of_data_points} configs by CPI")
        plt.savefig(f'{PLOT_DIR}/' + key + ".png")

    # plots in respective folders