#!/usr/bin/env python

import re
import sys
import os

#for iomanipulation
import StringIO

#for partial functions
#from functools import partial

standardout = sys.stdout

flag_alias = {
  '-v':'Verbose',
  '-verbose':'Verbose',
  '-c':'Compress',
  '-m':'Minimize',
  '--help':'Help',
  '-p':'Python'
}

flags = {
  'Verbose':0,
  'Compress':0,
  'Minimize':0,
  'Python':0
}
         
flag_descriptions = {
  'Verbose':"Print out information step by step of the process",
  'Compress':"Compresses the file, removes spaces and whatnot",
  'Minimize':"",
  'Python':"Creates a file and outputs it containing python code to generate the page"
}

__PATH=["."]

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
  
  #input_file = open(arguments[1],'r')
  output_file = open(arguments[2],'w')
  
  #input_file_text = input_file.read()
  
  #output_file_text = parsefile (input_file_text, {})
  
  output_file_text = includeCore (arguments[1])
    
  print "Amassite Parsing Complete"
  
  output_file.write(output_file_text)
  
  print "Amassite Writing Complete"

################################## PARSE FILE ##################################
# Parse all the files, nope i am not doing a good job of documenting this just #
# yet
################################################################################
def parsefile ( file_text, variable_map ):
  # add the "include" function to the variables list
  variable_map["include"]=include
  # match patterns
  match_pattern = "{{.*?}}"
  regexmatch = re.compile(match_pattern,re.DOTALL)
  #parsed_file = re.sub(match_pattern,parseelement,file_text)
  
  
  matches = regexmatch.findall (file_text)
  everythingelse = regexmatch.split(file_text)
  
  variable_map["__EVERYTHING_ELSE"] = everythingelse;
  indentationLevel = 0
  indent = "  ";
  output = "import math\nimport sys\nprint __EVERYTHING_ELSE[0]\n"
  iteration = 1;
  for match in matches:
    match = match[2:len(match)-2] # cut off the brackets
    match = re.sub("\n\s*", " ", match) # convert all of the line breaks to spaces
    # if while for
    if (match=="endif") | (match=="endfor") | (match=="endwhile"):
      indentationLevel -= 1
      match = ""
      #continue #endx is not really a function so it will not be included in the code
    if (match[0:4]=="elif") | (match[0:4]=="else"):
      indentationLevel -=1
    #create indentation level
    newline = indent*indentationLevel
    if (match[0:5]=="print"):
      match+=","
    newline += match
    if (match[0:2]=="if") | (match[0:3]=="for") | (match[0:5]=="while") | (match[0:4]=="elif") | (match[0:4]=="else"):
      indentationLevel += 1
      if match[len(match)-1:len(match)] != ":":
        newline+=":"
    newline += "\n"
    # then include the text
    newline += indent*indentationLevel + "sys.stdout.write(__EVERYTHING_ELSE["+ str(iteration) + "])\n"
    iteration += 1
    # add it to the output
    output += newline
  #print "Finished Generating Python"
  print output
  
  
  # Swap the Output buffer
  tempout = sys.stdout
  newout = StringIO.StringIO()
  sys.stdout = newout
  # Execute the code
  exec (output,variable_map);
  # Swap the output buffer back
  sys.stdout = tempout
  newout.close
  #return parsed_file
  #print "finished running python"
  return newout.getvalue()


def include(filePath, *args, **kw):
  print includeCore (filePath, *args, **kw)
  
def includeCore (filePath, *args, **kw):
  outputStream = sys.stdout
  sys.stdout = standardout;
  #print "INCLUDING FILE"
  #print "Old path",__PATH[-1]
  #print "relative Path", filePath
  newpath = os.path.join(__PATH[-1],filePath)
  print "New path", newpath
  newrootpath = os.path.dirname(newpath)
  #print "New Root path",newrootpath
  input_file = open(newpath,'r')
  input_file_text = input_file.read()
  __PATH.append(newrootpath)
  output_file_text = parsefile (input_file_text, kw)
  __PATH.pop()
  print "FINISHED INCLUDING FILE"
  sys.stdout = outputStream
  return output_file_text
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
