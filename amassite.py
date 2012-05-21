import re

def main():
  matchPattern = "{{.*?}}"
  m = re.sub(matchPattern,parse_element,'{{helloworld var=tom}}{{a}}')
  print m

################################# PARSE ELEMENT ################################
# This function takes in a matched object tag and then parses the insides to   #
# result in the valid HTML for the compiled file                               #
################################################################################
def parse_element (matchobj):
  text = matchobj.group(0)
  print text
  return "!"+text+"!"
  
if __name__ == '__main__':
  main()
