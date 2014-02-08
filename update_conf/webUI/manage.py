#! /usr/bin/env python

import os

cgi_weburl='30.0.0.3'
cgi_alias='switch_netboot'

def exec_bash(relate_runpath,run_command):
 wDIR=os.getcwd()
 os.chdir(relate_runpath)
 run_result = os.popen(run_command)
 os.chdir(wDIR)
 return run_result
