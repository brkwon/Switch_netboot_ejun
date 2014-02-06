#! /usr/bin/env python

import cgi
import cgitb
import os
import manage

class Register_zone_aggrs:

 def __init__(self):

  cgitb.enable()
  self.form = cgi.FieldStorage()
  self.base_html = open("./base.html").read()
  self.insert_contents={}
  self.insert_contents['page_name']="Register Zone AGG Switch "

  if self.form.getvalue('key','') == 'submitted':
   # requested variables for register........
   platform_name = self.form.getvalue('platform_name','')
   zone_name = self.form.getvalue('zone_name','')
   service_name = self.form.getvalue('service_type','')
   add_type = self.form.getvalue('agg_type','')
   agg1_name = self.form.getvalue('agg1_name','')
   agg1_lo = self.form.getvalue('agg1_lo','')
   agg2_name = self.form.getvalue('agg2_name','')
   agg2_lo = self.form.getvalue('agg2_lo','')
   # register file and property..........
   zone_agg_name = platform_name+"."+zone_name+"."+service_name+"."+add_type+"-aggrs"
   zone_agg_path = "../aggr-lib/"+zone_agg_name

   if os.path.exists(zone_agg_path):
    read_zone_file = file(zone_agg_path,'r')
    read_zone_content = read_zone_file.readline() 
    read_messages=''   
    while read_zone_content:
     read_messages = read_messages + read_zone_content.strip() + "<br>"
     read_zone_content = read_zone_file.readline()
    read_zone_file.close()
    remove_form = open("./remove-zone-aggrs.form").read()
    remove_file_name = {}
    remove_file_name['filename'] = zone_agg_name
    remove_zone_form= remove_form % remove_file_name    
    self.insert_contents['form_name']="this zone aggregation switch information is already existed ! <br>"
    self.insert_contents['form_name'] = self.insert_contents['form_name'] + "<h2>"+zone_agg_name+"</h2>"+read_messages+"<br>"+remove_zone_form

   #### if os.path.exists(zone_agg_path): not existed! 
   else:
    if self.variables_empty_status(agg1_name,agg1_lo,agg2_name,agg2_lo):
     run_command = "./register-zone-aggrs.sh "+platform_name+" "+zone_name+" "+service_name+" "+add_type+" "+agg1_name+" "+agg1_lo+" "+agg2_name+" "+agg2_lo
     run_result = manage.exec_bash(run_command)
     self.insert_contents['form_name']="register process is "+run_result.read()+" ! <br><br>"

    #### if self.variables_empty_status(agg1_name,agg1_lo,agg2_name,agg2_lo): empty case
    else:
     self.insert_contents['form_name']="the informations are not enough to register ! <br><br>"
   # link to register zone agg switch page .......
   link_line = "<a href=\"http://30.0.0.3/switch_netboot/register-zone-aggrs.py\"> Go to registe zone aggregation </a>"
   self.insert_contents['form_name'] = self.insert_contents['form_name'] +link_line

  #### if self.form.getvalue('key','') == 'remove':  
  elif self.form.getvalue('key','') == 'remove':
   filename = self.form.getvalue('filename','')
   run_command = "rm -rf ./aggr-lib/"+filename
   run_result = manage.exec_bash(run_command)
   form_content =  open("./register-zone-aggrs.form").read()
   self.insert_contents['form_name']=form_content

  #### if self.form.getvalue('key','') == 'anything': 
  else:
   form_content =  open("./register-zone-aggrs.form").read()
   self.insert_contents['form_name']=form_content


 def variables_empty_status(self, *args):
  status=True
  for arg in args:
   if not arg:
    status=False
    break
  return status
 
 def display_html(self):
  print "Content-Type: text/html\n\n"
  print self.base_html % self.insert_contents


if __name__ == "__main__":
 obj = Register_zone_aggrs()
 obj.display_html()
 
  
