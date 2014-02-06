#! /usr/bin/env python

import os

def exec_bash(run_command):
 wDIR=os.getcwd()
 os.chdir("../")
 run_result = os.popen(run_command)
 os.chdir(wDIR)
 return run_result
