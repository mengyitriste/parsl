# _*_  coding : utf-8   _*_
#
#   Multi-Core Test Script for strategy(ies) benchmark
#
__author__ = 'tkurihana@uchicago.edu'

import os
import sys
import time
from mod_libmonitors import _get_cpu, _get_mem

# parsl module 
import parsl
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
# from parsl.launchers import SimpleLauncher
from parsl.launchers import SingleNodeLauncher
from parsl.config import Config
from parsl.executors import HighThroughputExecutor

# Log 
import logging
logger  = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO) 

@python_app
def _logger(*args):
  import logging
  logger  = logging.getLogger()
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.INFO)
  logger.addHandler(handler)
  _logging = logger.setLevel(logging.INFO) 
  return _logging

# config
config = Config(
    executors=[
        HighThroughputExecutor(
            label="local_threads",
            #label="htex_local",
            # worker_debug=True,
            cores_per_worker=1,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
                # tasks_per_node=1,  # For HighThroughputExecutor, this option sho<
                launcher=SingleNodeLauncher(),
            ),
        )
    ],
    #strategy='htex_aggressive',
    #strategy='htex_totaltime',
    strategy='simple',
)
# Load config 
parsl.load(config)


@python_app
def func(n=1000000, stime=0.00):
  # import necessary library?! otherwise get errors
  import os, sys, time
  import psutil
  import logging
  logger  = logging.getLogger()
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.INFO)
  logger.addHandler(handler)
  logger.setLevel(logging.INFO) 

  logging.info("  ### JOB START ### ")
  x = 0.0
  #n = 1000000
  num = 0
  mems = []
  cpus = []
  times = []
  while num < 1:
    init_time = time.time()
    for i in range(n):
      x += float(i)
      if i % 1000 == 0:
        print("   ", flush=True)
        mems += [psutil.virtual_memory().percent]
        cpus += [psutil.cpu_percent()]
        ctime = time.time() - stime
        times += [ctime]

    num = 1
    end_time  = time.time() - init_time
  logging.info("Elapse Time: %f" % end_time)
  return mems, cpus, times


_n = 10000000
# initial
stime = time.time()
mem_list = []
cpu_list = []
times_list = []
#for i in range(1):
i = 2
#time.sleep(10*(i+1))
cpu_list.append(_get_cpu())
mem_list.append(_get_mem())
times_list.append(time.time()-stime)
#n= _n*(i+1)
n= _n*(i+1)
alist = []
alist +=[ func(n, stime).result()]   # result() should be appended otherwise get error
print(alist)
mem, cpu, times = alist
  
# Upadate 
mem_list.extend(mem)
cpu_list.extend(cpu)
times_list.extend(times)
   