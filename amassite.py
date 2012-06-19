#!/usr/bin/env python

import re
import sys

#for iomanipulation
import StringIO

flag_alias = {
  '-v':'Verbose',
  '-verbose':'Verbose',
  '-c':'Compress',
  '-m':'Minimize',
  '--help':'Help'
}

flags = {
  'Verbose':0,
  'Compress':0,
  'Minimize':0
}
         
flag_descriptions = {
  'Verbose':"Print out information step by step of the process",
  'Compress':"Compresses the file, removes spaces and whatnot"
}

##################################### MAIN #####################################
# The main function, does all the work, all the time...
################################################################################
def main():
  tempout = sys.stdout
  newout = StringIO.StringIO()
  sys.stdout = newout
  exec ('print "hello",')
  sys.stdout = tempout
  newout.close
  print ":",newout.getvalue(),":"
  
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
  
  output_file_text = parsefile (input_file_text, {})
  
  print "Amassite Parsing Complete"
  
  output_file.write(output_file_text)
  
  print "Amassite Writing Complete"

################################## PARSE FILE ##################################
# Parse all the files, nope i am not doing a good job of documenting this just #
# yet
################################################################################
def parsefile ( file_text , variable_map ):
  # match patterns
  
  match_pattern = "{{.*?}}"
  regexmatch = re.compile(match_pattern,re.DOTALL)
  #parsed_file = re.sub(match_pattern,parseelement,file_text)
  
  
  matches = regexmatch.findall (file_text)
  everythingelse = regexmatch.split(file_text)
  
  
 
  print len(matches)
  print len(everythingelse)
  
  # swap output
  exec (code,variable_map);
  # swap output back
  
  return parsed_file

################################# PARSE ELEMENT ################################
# This function takes in a matched object tag and then parses the insides to   #
# result in the valid HTML for the compiled file                               #
################################################################################
'''
def parseelement (matchobj):
  text = matchobj.group(0)
  print text,"|"
  return ""
  # load the text
  
  text = text[2:len(text)-2]
  #   for char in text:
    
  
  # find all of the tokens in the command
  match_variable = "$[^\w]+"
  match_setvar   = "[]"
  match_fileload = "[^\w]+="
  match_all = "("+match_variable+")|("+match_setvar+")|("+match_fileload+")"
  # strip off the brackets
  
  print text
  return "!"+text+"!" 
'''




################################### RUN MAIN ###################################
if __name__ == '__main__':
  main()
