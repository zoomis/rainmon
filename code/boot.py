#!/usr/bin/python
#Bootstrap for server and sample data generation
#@author ishafer

import sys
sys.path.append('ui')
from ui.manage import *

#Possible 
'''
iostat.disk.read_requests,
iostat.disk.write_requests,
iostat.disk.msec_write,
iostat.disk.msec_read,
iostat.disk.read_sectors,
iostat.disk.write_sectors,
proc.loadavg.runnable,
proc.meminfo.memfree,
proc.meminfo.memtotal,
proc.meminfo.cached,
proc.meminfo.buffers,
proc.stat.ctxt,
proc.stat.intr,
proc.stat.procs_blocked,
proc.stat.cpu.type.nice,
proc.stat.cpu.type.system,
proc.stat.cpu.type.iowait,
proc.stat.cpu.type.user,
proc.net.packets.direction.out,
proc.net.packets.direction.in,
proc.loadavg.total_threads,
proc.net.bytes.direction.in,
proc.net.bytes.direction.out,
net.sockstat.memory.type.tcp,
net.sockstat.num_sockets.type.tcp
'''

def generate():
    from ui.rain.tasks import run_pipeline
    run_pipeline( \
        "test-from-shell", \
        ['cloud%d' % (i) for i in xrange(1,15)], \
        ['iostat.disk.read_requests','iostat.disk.write_requests','proc.stat.intr'], \
        '2011/11/22-15:00:00', \
        '2011/11/22-15:45:00')

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "generate":
        generate()
    else:
        execute_manager(settings)
    
    print "Done"