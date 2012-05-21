#!/usr/bin/env python

import re
import sys

flag_alias = {'-v':'Verbose',
              '-verbose':'Verbose'}
flags = {'Verbose':0}
         

##################################### MAIN #####################################
# The main function, does all the work, all the time...
################################################################################
def main():
  #remove the functioncall from the arguments list
  arguments = []
  for argument in sys.argv:
    try:
      flagname = flag_alias[argument]
      flags[flagname] = 1
      print flagname, "Mode"
    except Exception:
      arguments.append(argument)
  
  if len(arguments) != 3:
    print "amassite <inputfile> <outputfile>"
    exit()
  
  input_file = open(arguments[1],'r')
  output_file = open(arguments[2],'w')
  
  input_file_text = input_file.read()
  
  output_file_text = parsefile (input_file_text)
  
  print "Amassite Parsing Complete"
  
  output_file.write(output_file_text)
  
  print "Amassite Writing Complete"
    
def parsefile ( file_text ):
  match_pattern = "{{.*?}}"
  parsed_file = re.sub(match_pattern,parseelement,file_text)
  return parsed_file

################################# PARSE ELEMENT ################################
# This function takes in a matched object tag and then parses the insides to   #
# result in the valid HTML for the compiled file                               #
################################################################################
def parseelement (matchobj):
  text = matchobj.group(0)
  return "!"+text+"!"


if __name__ == '__main__':
  main()
