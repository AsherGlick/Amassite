from subprocess import Popen
import subprocess
import os

units = [
    {"TestName" : "Single Var Arg (Generate)"
    ,"Test"     : "../source/amassite.py -c htmlvars/varArgument.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\n"
    }
    ,
    {"TestName" : "Single Var Arg (Compare)"
    ,"Test"     : "cat output.html"
    ,"Stdin"    : ""
    ,"Result"   : open("htmlvars/results/varArgument.html").read()
    }
    ,
    {"TestName" : "Array Argument (Generate)"
    ,"Test"     : "../source/amassite.py -c htmlvars/arrayArgument.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\n"
    }
    ,
    {"TestName" : "Array Argument (Compare)"
    ,"Test"     : "cat output.html"
    ,"Stdin"    : ""
    ,"Result"   : open("htmlvars/results/arrayArgument.html").read()
    }
    ,
    {"TestName" : "Nested Var Argument (Generate)"
    ,"Test"     : "../source/amassite.py -c htmlvars/nestedVarArgument.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\n"
    }
    ,
    {"TestName" : "Nested Var Argument (Compare)"
    ,"Test"     : "cat output.html"
    ,"Stdin"    : ""
    ,"Result"   : open("htmlvars/results/nestedVarArgument.html").read()
    }
    ,
    {"TestName" : "Indeneted Var Argument (Generate)"
    ,"Test"     : "../source/amassite.py -c htmlvars/indentedVarArgument.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\n"
    }
    ,
    {"TestName" : "Indented Var Argument (Compare)"
    ,"Test"     : "cat output.html"
    ,"Stdin"    : ""
    ,"Result"   : open("htmlvars/results/indentedVarArgument.html").read()
    }
    ,
    {"TestName" : "Indeneted Array Argument (Generate)"
    ,"Test"     : "../source/amassite.py -c htmlvars/indentedArrayArgument.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\n"
    }
    ,
    {"TestName" : "Indented Array Argument (Compare)"
    ,"Test"     : "cat output.html"
    ,"Stdin"    : ""
    ,"Result"   : open("htmlvars/results/indentedArrayArgument.html").read()
    }
    # Debugging output Tests
    ,
    {"TestName" : "Main Doc With Undefined Variable"
    ,"Test"     : "../source/amassite.py -c debugOutput/docWithError.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\nERROR: name 'helloworld' is not defined on line 6 of debugOutput/docWithError.html\n"
    }
    ,
    {"TestName" : "Template With Undefined Variable"
    ,"Test"     : "../source/amassite.py -c debugOutput/templateWithErrorWrapper.html output.html"
    ,"Stdin"    : ""
    ,"Result"   : "Cleanup Mode\nERROR: name 'error' is not defined on line 2 of templateWIthError.html\n"
    }
]













def run (command, cin=""):
    commands = command.split(" ")
    process = Popen(commands, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if cin != "":
        output = process.communicate(input=cin)[0]
    else:
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]
    return output



#print "|--|\n",run("./chead HELLO WORLD"),"|--|"


OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])



(width, height) = getTerminalSize()
for unit in units:
    if run(unit["Test"],unit["Stdin"]) == unit["Result"]:
        print unit["TestName"] + " " +("."*(width-11-len(unit["TestName"])) ) + OKGREEN + " [SUCESS]" + ENDC
    else:
        print unit["TestName"] + " " +("."*(width-11-len(unit["TestName"])) ) + FAIL + " [FAILED]" + ENDC
        print run(unit["Test"],unit["Stdin"])
