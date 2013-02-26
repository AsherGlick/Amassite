#!/usr/bin/env python
#################################### LICENSE ###################################
# Copyright (c) 2013, Asher Glick                                              #
# All rights reserved.                                                         #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#                                                                              #
# * Redistributions of source code must retain the above copyright notice,     #
# this                                                                         #
#   list of conditions and the following disclaimer.                           #
# * Redistributions in binary form must reproduce the above copyright notice,  #
#   this list of conditions and the following disclaimer in the documentation  #
#   and/or other materials provided with the distribution.                     #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE    #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                                  #
################################################################################

import re
import sys
import traceback
import os
import shutil
import StringIO

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
# The main funciton grabs the arguments and sets the flags, check input        #
# sanity, then checks to see if the input and output destinations are files    #
# or directories. If they are files then it runs the amassite parser on the    #
# input and puts it into the output. If they are directories ir runs the       #
# parser on each file in the directory and ouputs it to the same relative      #
# path of the new directory as it was in the old directory                     #
################################################################################
def main():
  # grab the arguments and set the flag
  arguments = setFlags(sys.argv)

  # argument sanitatiy check
  if len(arguments) != 3:
    print "amassite <input> <output>"
    exit()
  

  inputPath = arguments[1]
  outputPath = arguments[2]

  # Check to see if arguments are files or directories
  if os.path.isdir(inputPath) != os.path.isdir(outputPath):
    print "Both the input and the output must be a directory or a file path, they cannot be both"
    exit()

  
  if os.path.isdir(inputPath) == False:
    compileFile(inputPath, outputPath)
  else:
    fileList = getFileList(inputPath)
    for fileName in fileList:
      compileFile(os.path.join(inputPath,fileName), os.path.join(outputPath,fileName))

################################ VERBOSE OUTPUT ################################
# This function is used when, during the runtime of the code, a message        #
# should be displayed to the user that would be considered verbose and not     #
# nessasary all the time. These messages are only displayed if the verbose     #
# flag is set                                                                  #
################################################################################
def verboseOutput(*args):
  if flags["Verbose"] == 1:
    print " ".join(args)

################################# GET FILE LIST ################################
# This function recursively gets all the files in a directory and returns an   #
# array containing all of the relative file paths from the specified directory #
################################################################################
def getFileList(inputPath):
  fileList = []
  for path in os.listdir(inputPath):
    if os.path.isdir(os.path.join(inputPath,path)):
      subFiles = [os.path.join(path,f) for f in getFileList(os.path.join(inputPath,path))]
      fileList.extend(subFiles)
    else:
      fileList.append(path)
  return fileList

################################## CREATE FILE #################################
# The create file function will create a new file at the specified directory   #
# and return the opened file as an object. If the directory does not exist     #
# then the directories will be created.                                        #
################################################################################
def createFile (filePath):
  (path,filename) = os.path.split(filePath)
  if not os.path.exists(path):
    os.makedirs(path)
  return open(filePath,'w')

################################# COMPILE FILE #################################
# This function opens the file and checks any medatata contained at the top    #
# of the file. If the metadata indicates that the file is an amassite          #
# template then the file is ignored. If the metadata indicates taht the file   #
# is an amassite doc then the file is parsed and then any cleanup or           #
# compression flags that are active are run on the results of the parsed       #
# file. If there is no metadata then the file is just copied to it's new       #
# destination                                                                  #
################################################################################
def compileFile(inputFile,outputFile):
    # Check to see if this file is a template file
    input_file = open(inputFile)
    firstLine = input_file.readline()
    input_file.close()
    if firstLine == "{{AMASSITE-TEMPLATE}}\n": ## TODO ## This method needs to check to see if that tag exists at all on the first line of the file instead of matching exactly
      # This file is an amassite template file and should not be processed
      verboseOutput ("Skipping Template", inputFile)
      return
    elif firstLine == "{{AMASSITE-DOC}}\n":
      verboseOutput("Beginning", inputFile)

      output_file = createFile(outputFile)

      output_file_text = includeCore(inputFile)  # act as if the specified file was being included in a blank html document (only will accept files)
        
      verboseOutput("  Parsing", inputFile, "completed")

      if flags["Cleanup"]==1:
        verboseOutput("  Cleaning File")
        blankline = re.compile("^[ \t\r\f\v]*\n",re.MULTILINE)
        output_file_text = blankline.sub("",output_file_text)
        verboseOutput("  Cleaning Complete")
      if flags["Compress"]==1:
        print "compressing"
        verboseOutput("  Compressing HTML")
        regexmatch = re.compile("<!--.*?-->",re.DOTALL)
        output_file_text = regexmatch.sub("",output_file_text)
        output_file_text = re.sub(">[ \t\r\f\n\v]*<","><",output_file_text)
        verboseOutput("  Compressing Complete")
      output_file.write(output_file_text)

      verboseOutput("  Writing", outputFile, "Complete")
    else:
      # just copy the file
      verboseOutput("Copying", inputFile)
      createFile (outputFile);
      shutil.copy2(inputFile, outputFile)

################################### SET FLAGS ##################################
# The set flags function takes in all the command line arguments and pulls     #
# out all the flags that are in the argument list and activates them. The      #
# function then returns all the remaining arguments as an array                #
################################################################################
def setFlags(arguments):
  #remove the functioncall from the arguments list
  nonFlagArguments = []
  for argument in arguments:
    try:
      flagname = flag_alias[argument]
      flags[flagname] = 1
      print flagname, "Mode"
    except Exception:
      nonFlagArguments.append(argument)
  return nonFlagArguments

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
  # find all the matches in the document
  matches = regexmatch.findall (file_text)
  # find everything that is not a match
  everythingelse = regexmatch.split(file_text)
  
  variable_map["__EVERYTHING_ELSE"] = everythingelse
  variable_map["stdoutRedirects"] = []
  variable_map["stringIOs"] = []
  variableNames = [] # an array/queue of the variable names for the html arguments
  indentationLevel = 0
  indent = "  "
  
  iteration = 1

  lineMapping = [] # every time there is a new line in the generated code, append the current source line to this
  currentSourceLine = 1

  output = "import math, sys, StringIO\nsys.stdout.write(__EVERYTHING_ELSE[0])\n"
  lineMapping.append(currentSourceLine)
  currentSourceLine += numberOfLines(everythingelse[0])
  lineMapping.append(currentSourceLine)
  print currentSourceLine
  

########################### CHECK THROUGH THE MATCHES ##########################
# These are the matches for the different Amassite tags in the HTML            #
################################################################################
  for match in matches:
    # input sanitization
    bracketlessTag = match[2:len(match)-2]              # cut off the brackets
    sanitizedTag = re.sub("\n\s*", " ", bracketlessTag) # convert all of the line breaks to spaces
    resultingFunction = sanitizedTag                    # the text of the resulting python code from the parsed tag

    metaTags = ["AMASSITE-TEMPLATE", "AMASSITE-DOC"]    # Meta-tags, remove any meta tags as they have allready been parsed and handled
    psuedoUnindentTags = ["endif","endfor","endwhile"]  # Un indentation for the psuedo commands created in ammassite
    unindentTags = ["elif", "else"]                     # Un indentation for the python commands that require un indentation
    indentCommands = ['if','for','while','elif','else'] # if it is a command wich requires indenting on the next line

    if multiPrefixMatch(metaTags,sanitizedTag):
      resultingFunction = ""
    elif multiPrefixMatch(psuedoUnindentTags, sanitizedTag):
      indentationLevel -= 1
      resultingFunction = ""
    elif multiPrefixMatch(unindentTags, sanitizedTag):
      indentationLevel -=1
      resultingFunction = sanitizedTag

    #Create a new line in the python code with the given indentation level
    newline = indent*indentationLevel

    # match some key commands to modify into different functions
    if prefexMatch('print',sanitizedTag):
      resultingFunction = "sys.stdout.write("+sanitizedTag[5:]+")"
      

    elif prefexMatch("varArgument",sanitizedTag):
      variableNames.append(sanitizedTag[12:])
      newline += "stdoutRedirects.append(sys.stdout)\n"
      lineMapping.append(currentSourceLine)
      newline += "newOutput = StringIO.StringIO()\n"
      lineMapping.append(currentSourceLine)
      newline += "sys.stdout = "+ "newOutput\n"
      lineMapping.append(currentSourceLine)
      newline += "stringIOs.append(newOutput)\n"
      lineMapping.append(currentSourceLine)
      resultingFunction = ""
      
    elif prefexMatch("endArgument",sanitizedTag):
      variableName = variableNames.pop()
      # grab the embedded value
      newline += "outputString = stringIOs.pop()\n"
      lineMapping.append(currentSourceLine)
      # createTheVariable
      newline += variableName + " = outputString.getvalue()\n" 
      lineMapping.append(currentSourceLine)
      # Swap the output buffer back
      newline += "sys.stdout = stdoutRedirects.pop()\n"
      lineMapping.append(currentSourceLine)
      newline += "outputString.close\n"  
      lineMapping.append(currentSourceLine)
      resultingFunction = ""
    
    elif prefexMatch('arrayArguments', sanitizedTag):
      variableName = sanitizedTag[15:]
      variableNames.append(variableName)
      #print variableName
      newline += "stdoutRedirects.append(sys.stdout)\n"
      lineMapping.append(currentSourceLine)
      newline += "newOutput = StringIO.StringIO()\n"
      lineMapping.append(currentSourceLine)
      newline += "sys.stdout = "+ "newOutput\n"
      lineMapping.append(currentSourceLine)
      newline += "stringIOs.append(newOutput)\n"
      lineMapping.append(currentSourceLine)
      newline += variableName + " = []\n"
      lineMapping.append(currentSourceLine)
      resultingFunction = ""

    elif prefexMatch('nextArgument',sanitizedTag):
      variableName = variableNames[-1]
      # grab the embedded value
      newline += "outputString = stringIOs.pop()\n"
      lineMapping.append(currentSourceLine)
      # createTheVariable
      newline += variableName + ".append(outputString.getvalue())\n" 
      lineMapping.append(currentSourceLine)
      #newline += variableName + ".append('v')\n" 

      # Swap the output buffer back
      #newline += "sys.stdout = stdoutRedirects.pop()\n"
      newline += "outputString.close\n"
      lineMapping.append(currentSourceLine)
      # put a new outout string inot the buffer for the next element
      newline += "newOutput = StringIO.StringIO()\n"
      lineMapping.append(currentSourceLine)
      newline += "sys.stdout = newOutput\n"
      lineMapping.append(currentSourceLine)
      newline += "stringIOs.append(newOutput)\n"
      lineMapping.append(currentSourceLine)
      resultingFunction = ""
      
    elif prefexMatch('endArray',sanitizedTag):
      variableName = variableNames.pop()
      # grab the embedded value
      newline += "outputString = stringIOs.pop()\n"
      lineMapping.append(currentSourceLine)
      # createTheVariable
      newline += variableName + ".append(outputString.getvalue())\n"
      lineMapping.append(currentSourceLine)
      # Swap the output buffer back
      newline += "sys.stdout = stdoutRedirects.pop()\n"
      lineMapping.append(currentSourceLine)
      newline += "outputString.close\n"
      lineMapping.append(currentSourceLine)
      resultingFunction = ""

    elif multiPrefixMatch(indentCommands,sanitizedTag):
      indentationLevel += 1
      resultingFunction = sanitizedTag
      if sanitizedTag[len(sanitizedTag)-1:len(sanitizedTag)] != ":":
        resultingFunction += ":"

    # create a new line and add the matched command to the generated code
    newline += resultingFunction + "\n"
    lineMapping.append(currentSourceLine)

    currentSourceLine += numberOfLines(match)

    # include the html between the toens
    newline += indent*indentationLevel + "sys.stdout.write(__EVERYTHING_ELSE["+ str(iteration) + "])\n"
    lineMapping.append(currentSourceLine)

    # increment the line debug line number for each newline in the source file
    currentSourceLine += numberOfLines(everythingelse[iteration])
    print currentSourceLine

    iteration += 1

    # add it to the output
    output += newline
  



  # Run the generated code and print its output to a file
  # Swap the Output buffer
  ### print output
  tempout = sys.stdout
  newout = StringIO.StringIO()
  sys.stdout = newout


  # # Execute the code
  # exec (output,variable_map);
  # # Swap the output buffer back
  # sys.stdout = tempout
  # newout.close






  try:
    # Execute the code
    exec (output,variable_map);
    # Swap the output buffer back
    sys.stdout = tempout
    newout.close
  except Exception as e:
    sys.stdout = tempout
    newout.close

    print type(e)
    print e.args

    printErrorInfo(lineMapping)

  ###################### debugging info
  print output
  print "-------"
  print lineMapping
  #####################################


  # Return the resulting text
  return newout.getvalue()

# This function returns the number of newlines a string has
def numberOfLines(string):
  newlineCount = 0
  for char in string:
    if char == "\n":
      newlineCount += 1
  return newlineCount


def printErrorInfo(lineMapping):
  # Line number
  etype, value, tb = sys.exc_info()
  stack = traceback.extract_tb(tb)
  lastElement = stack[-1]
  fileName, lineNumber, function, line = lastElement
  print lineNumber
  print 


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

################################# PREFEX MATCH #################################
# This function checks to see if a given string is the prefex of another       #
# given string. It automaticly creates a substring of the longer string and    #
# compares the substring to the prefex to return the result                    #
################################################################################
def prefexMatch(prefex, string):
  if len(string) >= len(prefex):
    substring = string[0:len(prefex)]
    if prefex == substring:
      return True
    else:
      return False
  else:
    return False

############################## MULTI PREFEX MATCH ##############################
# This function checks to see if any of a list of prefexes are the prefex of   #
# a string. If none of them are then the function returns false                #
################################################################################
def multiPrefixMatch(prefexes, string):
  for prefex in prefexes:
    if prefexMatch(prefex,string):
      return True
  return False

################################### RUN MAIN ###################################
# This is the command that runs the main function after the full python file   #
# has been loaded                                                              #
################################################################################
if __name__ == '__main__':
  main()
