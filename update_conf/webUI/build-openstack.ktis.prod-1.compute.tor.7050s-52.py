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
  self.insert_contents['page_name']=" Create the Switch Configuration "
  form_content =  open("./build-openstack.ktis.prod-1.compute.tor.7050s-52.form").read()
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
 
  
