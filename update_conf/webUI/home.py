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
 template_directory="../conf-lib"

 def __init__(self):

  cgitb.enable()
  self.form = cgi.FieldStorage()
  self.base_html = open("./base.html").read()
  self.insert_contents={}
  self.insert_contents['page_name']=" Switch Network Booting <br> "

  if self.form.getvalue('key','') == 'submitted_cnf':
   mgmt_device_name = self.form.getvalue('choose_mgmt','')
   if mgmt_device_name:
    display_config_table = self.display_config(mgmt_device_name)
    form_content = display_config_table
    remove_cnf_form = self.remove_form_generation("./remove-home.form",mgmt_device_name)
    upload_form=self.form_upload_file("home.py",mgmt_device_name,self.get_filename_indir(mgmt_device_name)[0],self.get_filename_indir(mgmt_device_name)[1])
    form_content = self.link_line+"<br><br>"+remove_cnf_form+upload_form+display_config_table+"<br>"+remove_cnf_form+self.link_line
   else:
    form_content = self.form_zone_add() + self.form_select_config() + self.form_select_template()

  ### self.form.getvalue('key','') == 'remove': part
  elif self.form.getvalue('key','') == 'remove':
   rm_filename = self.form.getvalue('filename','')
   ### hard link
   hard_link="/var/www/"+rm_filename.split("/")[2]
   rm_hard_link="rm -rf "+hard_link
   run_result = manage.exec_bash("./",rm_hard_link)
   time.sleep(manage.sleep_time)
   ### directory rm
   run_command = "rm -rf "+rm_filename
   run_result = manage.exec_bash("./",run_command)
   time.sleep(manage.sleep_time)
   form_content = self.form_zone_add() + self.form_select_config() + self.form_select_template()

  ### self.form.getvalue('key','') == 'upload': part
  elif self.form.getvalue('key','') == 'upload':
   upload_mgmt_devinfo=self.form.getvalue('mgmt_devname','')
   upload_radio1 = self.form.getvalue('choose_radio1','')
   upload_file1 = self.form.getvalue('file1','')
   if self.form['file1'].filename:
    f_open = open(self.config_directory+"/"+upload_mgmt_devinfo+"/"+upload_radio1,'wb')
    f_open.write(upload_file1)
    f_open.close()
    time.sleep(manage.sleep_time)
   ### show configuration menu
   form_content = self.form_zone_add() + self.form_select_config() + self.form_select_template() + self.form['file1'].filename

  ### self.form.getvalue('key','') == 'anything': part
  else:
   ### show configuration menu
   form_content = self.form_zone_add() + self.form_select_config() + self.form_select_template()
   

  ### __init__ end
  self.insert_contents['form_name']=form_content

 def form_select_config(self):
  form_content = ''
  form_content = Home.form_start+"<h4>Select the Configuration Name</h4>"+Home.hidden_input_form % ("submitted_cnf") + Home.select_form_start % ("choose_mgmt")
  for filename in os.listdir(Home.config_directory):
   if os.path.isdir(Home.config_directory+"/"+filename):
    option_message = "<option value=\""+filename.strip()+"\">"+filename.strip()+"</option>"
    form_content = form_content + option_message
  form_content = form_content + Home.select_form_end + "<input type='submit' value='Show the Configuration'/>" + Home.form_end
  return form_content

 def form_select_template(self):
  form_content = "<h4>Select the template to create configuration</h4>"
  for filename in os.listdir(Home.template_directory):
   if os.path.isfile(Home.template_directory+"/"+filename):
    URL_link="<a href=http://"+manage.cgi_weburl+"/"+manage.cgi_alias+"/build-"+filename+".py>"+filename+"</a>"
    form_content = form_content + URL_link + "<br>"
  return form_content

 def form_zone_add(self):
  form_content = "<h4>Go to the Zone Aggregation register</h4>"
  Zone_Link="<a href=\"http://"+manage.cgi_weburl+"/"+manage.cgi_alias+"/register-zone-aggrs.py\">Zone AGG Registration</a>"
  form_content = form_content + Zone_Link
  return form_content

 def form_upload_file(self,current_file_name,mgmt_devinfo,selection_option1,selection_option2):
  input_form_dict={}
  input_form_dict['cgi_weburl']=manage.cgi_weburl
  input_form_dict['cgi_alias']=manage.cgi_alias
  input_form_dict['current_file_name']=current_file_name
  input_form_dict['mgmt_devinfo']=mgmt_devinfo
  input_form_dict['selection_option1']=selection_option1
  input_form_dict['selection_option2']=selection_option2
  upload_form = open("./upload_file.form").read()
  return upload_form % input_form_dict

 def get_filename_indir(self,mgmt_device_name):
  return_list=[]
  cnf_dir_name=self.config_directory+"/"+mgmt_device_name
  for filename in os.listdir(cnf_dir_name):
   return_list.append(filename.strip())
  return return_list

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
