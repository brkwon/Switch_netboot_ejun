#! /usr/bin/env python

import cgi
import cgitb
import os
import manage

class Build_openstack_ktis_prod_1_compute_tor_7050s_52:

 link_line = "<a href=\"http://"+manage.cgi_weburl+"/"+manage.cgi_alias+"/build-openstack.ktis.prod-1.compute.tor.7050s-52.py\"> Go to build the configuration </a>"
 config_directory="../vars"

 def __init__(self):

  cgitb.enable()
  self.form = cgi.FieldStorage()
  self.base_html = open("./base.html").read()
  self.insert_contents={}
  self.insert_contents['page_name']=" Build the Configuration <br> ( openstack.ktis.prod-1.compute.tor.7050s-52 ) "


  if self.form.getvalue('key','') == 'submitted':

   ### get values from request
   switch_name = self.form.getvalue('switch_name','').strip()
   enable_pass = self.form.getvalue('enable_pass','').strip()
   admin_pass = self.form.getvalue('admin_pass','').strip()
   ktcseadmin_pass = self.form.getvalue('ktcseadmin_pass','').strip()
   opadmin_pass = self.form.getvalue('opadmin_pass','').strip()
   service_host_network = self.form.getvalue('service_host_network','').strip()
   storage_host_network = self.form.getvalue('storage_host_network','').strip()
   switch1_service_lo = self.form.getvalue('switch1_service_lo','').strip()
   switch1_storage_lo = self.form.getvalue('switch1_storage_lo','').strip()
   switch2_service_lo = self.form.getvalue('switch2_service_lo','').strip()
   switch2_storage_lo = self.form.getvalue('switch2_storage_lo','').strip()
   service_net_uplink_t1r1 = self.form.getvalue('service_net_uplink_t1r1','').strip()
   service_net_uplink_t2r2 = self.form.getvalue('service_net_uplink_t2r2','').strip()
   storage_net_uplink_t1r1 = self.form.getvalue('storage_net_uplink_t1r1','').strip()
   storage_net_uplink_t2r2 = self.form.getvalue('storage_net_uplink_t2r2','').strip()
   mgmt_device_name = self.form.getvalue('mgmt_device_name','').strip()
   mgmt_network = self.form.getvalue('mgmt_network','').strip()

   ### confirm the values are not empty
   if self.variables_empty_status(switch_name,enable_pass,admin_pass,ktcseadmin_pass,opadmin_pass,service_host_network,storage_host_network,switch1_service_lo,switch1_storage_lo,switch2_service_lo,switch2_storage_lo,service_net_uplink_t1r1,service_net_uplink_t2r2,storage_net_uplink_t1r1,storage_net_uplink_t2r2,mgmt_device_name,mgmt_network):
    
    ### file existance check.............................. 
    if os.path.exists(self.config_directory+"/"+mgmt_device_name):
     ### create table to show the configuration
     display_config_table = self.display_config(mgmt_device_name)
     ### remove form insert
     remove_form = open("./remove-openstack.ktis.prod-1.compute.tor.7050s-52.form").read()
     remove_file_name = {}
     remove_file_name['filename'] = self.config_directory+"/"+mgmt_device_name
     remove_file_name['cgi_weburl'] = manage.cgi_weburl
     remove_file_name['cgi_alias'] = manage.cgi_alias
     remove_cnf_form= remove_form % remove_file_name
     form_content = remove_cnf_form+self.link_line+"<br><br>"+display_config_table+"<br>"+remove_cnf_form+self.link_line
    ### if os.path.exists(config_directory):
    else:
     arguments=switch_name+" "+enable_pass+" "+admin_pass+" "+ktcseadmin_pass+" "+opadmin_pass+" "+service_net_uplink_t1r1+" "+service_net_uplink_t2r2+" "+storage_net_uplink_t1r1+" "+storage_net_uplink_t2r2+" "+switch1_service_lo+" "+switch2_service_lo+" "+switch1_storage_lo+" "+switch2_storage_lo+" "+mgmt_device_name+" "+mgmt_network+" "+service_host_network+" "+storage_host_network
     run_command="./builder\@openstack.ktis.prod-1.compute.tor.7050s-52 "+arguments
     run_result = manage.exec_bash("../builder",run_command)
     form_content="create configuration status : [  "+run_result.read()+"  ] ! <br><br>"
     form_content = form_content+self.link_line

   ### if self.variables_empty_status: not enough input values..................
   else:
    form_content="the informations are not enough to create the configuration ! <br><br>"
    form_content = form_content+self.link_line
  
  ### self.form.getvalue('key','') == 'remove': part
  elif self.form.getvalue('key','') == 'remove':
   filename = self.form.getvalue('filename','')
   run_command = "rm -rf "+filename
   run_result = manage.exec_bash("./",run_command)
   form_content =  open("./build-openstack.ktis.prod-1.compute.tor.7050s-52.form").read()
   cgi_content={}
   cgi_content['cgi_weburl']=manage.cgi_weburl
   cgi_content['cgi_alias']=manage.cgi_alias
   form_content = form_content % cgi_content

  ### self.form.getvalue('key','') == 'anything': part
  else:
   form_content =  open("./build-openstack.ktis.prod-1.compute.tor.7050s-52.form").read()
   cgi_content={}
   cgi_content['cgi_weburl']=manage.cgi_weburl
   cgi_content['cgi_alias']=manage.cgi_alias
   form_content = form_content % cgi_content

  ### __init__ end
  self.insert_contents['form_name']=form_content

 def display_config(self,mgmt_device_name):
  display_config_table="<h2>"+mgmt_device_name+" is already used ! </h2><br><table><tr>"
  cnf_dir_name=self.config_directory+"/"+mgmt_device_name
  for filename in os.listdir(cnf_dir_name):
   display_config_table = display_config_table + "<td><font size=3>"+filename+"</font></td>"
  display_config_table = display_config_table + "</tr><tr>"
  for filename in os.listdir(cnf_dir_name):
   read_cnf_contents=''
   read_cnf_file = file(cnf_dir_name+"/"+filename,'r')
   read_messages=read_cnf_file.readline()
   while read_messages:
    read_cnf_contents=read_cnf_contents+read_messages.strip()+"<br>"
    read_messages=read_cnf_file.readline()
   display_config_table = display_config_table +"<td><font size=2>"+read_cnf_contents+"</font></td>"
  display_config_table = display_config_table +"</tr></table>"
  return display_config_table






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
 obj = Build_openstack_ktis_prod_1_compute_tor_7050s_52()
 obj.display_html()
