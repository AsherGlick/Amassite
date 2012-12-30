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
  '-C':'Compress',
  '-m':'Javascript Minimize',
  '--help':'Help',
  '-p':'Python',
  '-c':'Cleanup',
}

flags = {
  'Verbose':0,
  'Compress':0,
  'Minimize':0,
  'Python':0,
  'Cleanup':0
}
         
flag_descriptions = {
  'Verbose':"Print out information step by step of the process",
  'Compress':"Compresses the file, removes spaces and whatnot",
  'Minimize':"",
  'Python':"Creates a file and outputs it containing python code to generate the page",
  'Cleanup':"The lowest form of compression, removes blank lines"
}

__PATH=["."]

##################################### MAIN #####################################
# The main function, does all the work, all the time...                        #
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
  
  output_file = open(arguments[2],'w')
  output_file_text = includeCore (arguments[1])
    
  print "Amassite Parsing Complete"
  
  if flags["Cleanup"]==1:
    print "Cleaning File"
    blankline = re.compile("^[ \t\r\f\v]*\n",re.MULTILINE)
    output_file_text = blankline.sub("",output_file_text)
    print "Cleaning Complete"
  if flags["Compress"]==1:
    print "Compressing HTML"
    regexmatch = re.compile("<!--.*?-->",re.DOTALL)
    output_file_text = regexmatch.sub("",output_file_text)
    output_file_text = re.sub(">[ \t\r\f\n\v]*<","><",output_file_text)
    print "Compressing Complete"
  output_file.write(output_file_text)
  
  print "Amassite Writing Complete"

################################## PARSE FILE ##################################
# Parse all the files, nope i am not doing a good job of documenting this just #
# yet                                                                          #
################################################################################
def parsefile ( file_text, variable_map ):
  # add the "include" function to the variables list
  variable_map["include"]=include
  # match patterns
  match_pattern = "{{.*?}}"
  regexmatch = re.compile(match_pattern,re.DOTALL)
  
  matches = regexmatch.findall (file_text)
  everythingelse = regexmatch.split(file_text)
  
  variable_map["__EVERYTHING_ELSE"] = everythingelse;
  variable_map["stdoutRedirects"] = []
  variable_map["stringIOs"] = []
  variableNames = [] # an array/queue of the variable names for the html arguments
  indentationLevel = 0
  indent = "  ";
  output = "import math, sys, StringIO\nsys.stdout.write(__EVERYTHING_ELSE[0])\n"
  iteration = 1;
  inArgument = False

  # Iterate through all the tokens
  for match in matches:
    # input sanitization
    match = match[2:len(match)-2] # cut off the brackets
    match = re.sub("\n\s*", " ", match) # convert all of the line breaks to spaces

    # un indent without real command
    unIndentWithoutCommand = ['endif','endfor','endwhile']
    if multiPrefixMatch(unIndentWithoutCommand,match):
      indentationLevel -= 1
      match = "" #end___ are not really a functions so they will not be included in the code

    # un indent with real command
    unIndentWithCommand = ['elif','else']
    if multiPrefixMatch(unIndentWithCommand,match):
      indentationLevel -=1

    # create indentation at the level specified by indentationLevel
    newline = indent*indentationLevel

    # match some key commands to modify into different functions
    if (match[0:5]=="print"):
      match="sys.stdout.write("+match[5:]+")"


    if (match[0:11]=="varArgument"):
      variableNames.append(match[12:])
      #print variableName
      newline += "stdoutRedirects.append(sys.stdout)\n"
      newline += "newOutput = StringIO.StringIO()\n"
      newline += "sys.stdout = "+ "newOutput\n"
      newline += "stringIOs.append(newOutput)\n"
      match = ""
      
    if (match[0:11]=="endArgument"):
      variableName = variableNames.pop()
      # grab the embedded value
      newline += "outputString = stringIOs.pop()\n"
      # createTheVariable
      newline += variableName + " = outputString.getvalue()\n" 
      # Swap the output buffer back
      newline += "sys.stdout = stdoutRedirects.pop()\n"
      newline += "outputString.close\n"  
      match = ""
    

    ## array arguments
    if prefexMatch('arrayArguments', match):
      variableName = match[15:]
      variableNames.append(variableName)
      #print variableName
      newline += "stdoutRedirects.append(sys.stdout)\n"
      newline += "newOutput = StringIO.StringIO()\n"
      newline += "sys.stdout = "+ "newOutput\n"
      newline += "stringIOs.append(newOutput)\n"
      
      newline += variableName + " = []\n"

      match = ""

    if prefexMatch('nextArgument',match):

      variableName = variableNames[-1]


      # grab the embedded value
      newline += "outputString = stringIOs.pop()\n"
      # createTheVariable
      newline += variableName + ".append(outputString.getvalue())\n" 
      #newline += variableName + ".append('v')\n" 

      # Swap the output buffer back
      #newline += "sys.stdout = stdoutRedirects.pop()\n"
      newline += "outputString.close\n"
      # put a new outout string inot the buffer for the next element
      newline += "newOutput = StringIO.StringIO()\n"
      newline += "sys.stdout = newOutput\n"
      newline += "stringIOs.append(newOutput)\n"
      match = ""
      

    if prefexMatch('endArray',match):

      variableName = variableNames.pop()
      # grab the embedded value
      newline += "outputString = stringIOs.pop()\n"
      # createTheVariable
      newline += variableName + ".append(outputString.getvalue())\n" 
      # Swap the output buffer back
      newline += "sys.stdout = stdoutRedirects.pop()\n"
      newline += "outputString.close\n"
      
      match = ""

    # add the matched command to the generated code
    newline += match

    # if it is a command wich requires indenting on the next line
    indentCommands = ['if','for','while','elif','else']
    if multiPrefixMatch(indentCommands,match):
      indentationLevel += 1
      if match[len(match)-1:len(match)] != ":":
        newline+=":"

    # create a new line
    newline += "\n"
    # include the html between the toens
    newline += indent*indentationLevel + "sys.stdout.write(__EVERYTHING_ELSE["+ str(iteration) + "])\n"
    iteration += 1

    # add it to the output
    output += newline
  
  # Run the generated code and print its output to a file
  # Swap the Output buffer
  ### print output
  tempout = sys.stdout
  newout = StringIO.StringIO()
  sys.stdout = newout
  # Execute the code
  exec (output,variable_map);
  # Swap the output buffer back
  sys.stdout = tempout
  newout.close
  # Return the resulting text
  return newout.getvalue()

#################################### INCLUDE ###################################
# the include function is the function that gets called from the HTML template #
# it runs the `include core` function and prints out the result, which is      #
# redirected to a different input buffer and then saved to the full file       #
################################################################################
def include(filePath, *args, **kw):
  print includeCore (filePath, *args, **kw),
  
################################# INCLUDE CORE #################################
# The `include core` function calculates relative file paths, opens the file   #
# requested and then parses it and returns the completed HTML of the file      #
################################################################################
def includeCore (filePath, *args, **kw):
  # Save the curent output stream and reset it to default
  outputStream = sys.stdout
  sys.stdout = standardout;
  # calculate the relative path of the file, relative to the file calling it  
  newpath = os.path.join(__PATH[-1],filePath)
  # calculate the path of the new file for all the files that it wil call
  newrootpath = os.path.dirname(newpath)
  __PATH.append(newrootpath)
  # open the file
  input_file = open(newpath,'r')
  input_file_text = input_file.read()
  # parse the file that was opened
  output_file_text = parsefile (input_file_text, kw)
  # pop this files path off the stack now that parsefile is done with it
  __PATH.pop()
  # return the output stream to whatever it was before
  sys.stdout = outputStream
  # return the data collected from the parsed file
  return output_file_text

## a simple way to match the begining characters of a string
def prefexMatch(prefex, string):
  #print string, ":", prefex,":",
  if len(string) >= len(prefex):
    substring = string[0:len(prefex)]
    #print substring,":",
    if prefex == substring:
      #print "true"
      return True
    else:
      #print "false"
      return False
  else:
    #print "false"
    return False

## a function to run a prefex match on an array of preefexes and a string
def multiPrefixMatch(prefexes, string):
  for prefex in prefexes:
    if prefexMatch(prefex,string):
      return True
  return False

################################### RUN MAIN ###################################
if __name__ == '__main__':
  main()