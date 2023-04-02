import m5
from m5.objects import *
from m5.objects.BranchPredictor import *
from m5.util import addToPath

import cache

import argparse

addToPath('./')


def add_options(parser):
    parser.add_argument('-b', '--binary', type=str, default='',
                        help='Path to the binary to execute.')

    parser.add_argument('--LQEntries', type=int, default=32,
                        help='Number of load queue entries. Default: 32.')
    parser.add_argument('--SQEntries', type=int, default=32,
                        help='Number of store queue entries. Default: 32.')

    parser.add_argument('--l1d_size', type=str, default='32kB',
                        help='L1 data cache size. Default: Default: 32kB.')
    parser.add_argument('--l1i_size', type=str, default='8kB',
                        help='L1 instruction cache size. Default: 8kB.')
    parser.add_argument('--l2_size', type=str, default='256kB',
                        help='L2 cache size. Default: 256kB.')

    parser.add_argument('--bp_type', type=str, default='TournamentBP',
                        help='Branch predictor type. Default: TournamentBP.')

    parser.add_argument('--numROBEntries', type=int, default=128,
                        help='Number of ROB entries. Default: 128.')
    parser.add_argument('--numIQEntries', type=int, default=16,
                        help='Number of IQ entries. Default: 16.')


# if __name__ == '__m5_main__':
parser = argparse.ArgumentParser(
    description='A system with 2-level cache.')
add_options(parser)
options = parser.parse_args()

# Create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('1GB')]

# Create a simple CPU
system.cpu = DerivO3CPU()

# Create an L1 instruction and data cache
system.cache_line_size = 64
system.cpu.icache = cache.L1ICache(options)
system.cpu.dcache = cache.L1DCache(options)

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create a memory bus, a coherent crossbar, in this case
system.l2bus = L2XBar()
# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create an L2 cache and connect it to the l2bus
system.l2cache = cache.L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

# Create a memory bus
system.membus = SystemXBar()
# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)

# create the interrupt controller for the CPU
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Create a DDR3 memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Number of ROBs
system.cpu.numRobs = 1

system.cpu.LQEntries = options.LQEntries
system.cpu.SQEntries = options.SQEntries
system.cpu.numROBEntries = options.numROBEntries
system.cpu.numIQEntries = options.numIQEntries

# Branch predictor
if options.bp_type == 'TournamentBP':
    system.cpu.branchPred = TournamentBP()
elif options.bp_type == 'BiModeBP':
    system.cpu.branchPred = BiModeBP()

system.workload = SEWorkload.init_compatible(options.binary)

# Create a process
process = Process()
# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = [options.binary]
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
# instantiate all of the objects we've created above
m5.instantiate()
print('Beginning simulation!')
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' %
      (m5.curTick(), exit_event.getCause()))
