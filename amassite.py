#!/usr/bin/env python

import re
import sys


##################################### MAIN #####################################
# The main function, does all the work, all the time...
################################################################################
def main():
  print sys.argv
  print len(sys.argv)

def parsefile ( file_text ):
  match_pattern = "{{.*?}}"
  parsed_file = re.sub(match_pattern,parseelement,file_text)

################################# PARSE ELEMENT ################################
# This function takes in a matched object tag and then parses the insides to   #
# result in the valid HTML for the compiled file                               #
################################################################################
def parseelement (matchobj):
  text = matchobj.group(0)
  return "!"+text+"!"


if __name__ == '__main__':
  main()
