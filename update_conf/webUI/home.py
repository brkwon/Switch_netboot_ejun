#! /usr/bin/env python

import cgi
import cgitb
import os
import time
import manage

class Home:

 form_start="<form method='post' action=\"http://"+manage.cgi_weburl+"/"+manage.cgi_alias+"/home.py\">"
 form_end="</form>"

 select_form_start="<select name=%s>"
 select_form_end="</select>"

 hidden_input_form= "<input type='hidden' name='key' value=%s>"

 link_line = "<a href=\"http://"+manage.cgi_weburl+"/"+manage.cgi_alias+"/home.py\"> Go to Home Main </a>"
 config_directory="../vars"

 def __init__(self):

  cgitb.enable()
  self.form = cgi.FieldStorage()
  self.base_html = open("./base.html").read()
  self.insert_contents={}
  self.insert_contents['page_name']=" Switch Network Booting <br> "

  if self.form.getvalue('key','') == 'submitted':
   mgmt_device_name = self.form.getvalue('choose_mgmt','')
   if mgmt_device_name:
    display_config_table = self.display_config(mgmt_device_name)
    form_content = display_config_table
    remove_cnf_form = self.remove_form_generation("./remove-home.form",mgmt_device_name)
    form_content = self.link_line+"<br><br>"+remove_cnf_form+display_config_table+"<br>"+remove_cnf_form+self.link_line
   else:
    form_content = Home.form_start + Home.hidden_input_form % ("submitted") + Home.select_form_start % ("choose_mgmt")
    for filename in os.listdir(Home.config_directory):
     if os.path.isdir(Home.config_directory+"/"+filename):
      option_message = "<option value=\""+filename.strip()+"\">"+filename.strip()+"</option>"
      form_content = form_content + option_message
    form_content = form_content + Home.select_form_end + "<input type='submit' value='Show the Configuration'/>" + Home.form_end

  ### self.form.getvalue('key','') == 'remove': part
  elif self.form.getvalue('key','') == 'remove':
   rm_filename = self.form.getvalue('filename','')
   run_command = "rm -rf "+rm_filename
   run_result = manage.exec_bash("./",run_command)
   time.sleep(manage.sleep_time)
   form_content = ''
   form_content = Home.form_start + Home.hidden_input_form % ("submitted") + Home.select_form_start % ("choose_mgmt")
   option_message = ''
   for filename in os.listdir(Home.config_directory):
    if os.path.isdir(Home.config_directory+"/"+filename):
     option_message = "<option value=\""+filename.strip()+"\">"+filename.strip()+"</option>"
     form_content = form_content + option_message
   form_content = form_content + Home.select_form_end + "<input type='submit' value='Show the Configuration'/>" + Home.form_end
 
  ### self.form.getvalue('key','') == 'anything': part
  else:
   form_content = Home.form_start + Home.hidden_input_form % ("submitted") + Home.select_form_start % ("choose_mgmt")
   for filename in os.listdir(Home.config_directory):
    if os.path.isdir(Home.config_directory+"/"+filename):
     option_message = "<option value=\""+filename.strip()+"\">"+filename.strip()+"</option>" 
     form_content = form_content + option_message   
   form_content = form_content + Home.select_form_end + "<input type='submit' value='Show the Configuration'/>" + Home.form_end

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

 def remove_form_generation(self,form_file,mgmt_device_name):
  remove_form = open(form_file).read()
  remove_file_name = {}
  remove_file_name['filename'] = Home.config_directory+"/"+mgmt_device_name
  remove_file_name['cgi_weburl'] = manage.cgi_weburl
  remove_file_name['cgi_alias'] = manage.cgi_alias
  remove_cnf_form= remove_form % remove_file_name
  return remove_cnf_form

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
 obj = Home()
 obj.display_html()
