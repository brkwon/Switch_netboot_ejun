#! /usr/bin/env python

import os

cgi_weburl='30.0.0.3'
cgi_alias='switch_netboot'

sleep_time=1
home_link_line = "<a href=\"http://"+cgi_weburl+"/"+cgi_alias+"/home.py\"> Go to Home Main </a>"

def exec_bash(relate_runpath,run_command):
 wDIR=os.getcwd()
 os.chdir(relate_runpath)
 run_result = os.popen(run_command)
 os.chdir(wDIR)
 return run_result
