Amassite
========

Amassite is a static web page compiler allowing users to use the simplicity of python to program the features they desire in their web pages

Goals                   | Status
------------------------|-------
Generic Python Parsing  | Complete
HTML Minification       | Basic HTML compression exists
Debugging Info          | User compiled code is debugged correctly (incorrect function calls are not)
Javascript Minification | Acheived through Closure Compiler
CSS Minification        | Achieved through Closure Stylesheets
Security parsing        | Not Begun
Live Detect Compiling   | Not Begun
Casheing on Recompile   | Not Begun
Publishing (FTP / SSH)  | Not Begin (works with mounting drive as folder)
Publishing (git branch) | External Scripts avalible using git-new-workdir


Program Usage
-------------
amassite <input> <output>
input and output can both be individual files or both be directories
If they are directories then all files in the input will be processed and place in the same file structure in the output directory


Flag         | Function
-------------|-------
-v, -verbose | Displays verbose output of 
-C           | Compress (compressed HTML)
-m           | Javascript Minimize (not enabled)
--help       | Help
-c           | Cleanup (simple compression, removes blank lines)


A static webpage compiler, based on the django markup syntax  
An easy way to avoid php when created non-dynamic websites that you want to change occasinally  


Planned Flags
-C cleanup -> removes excess spaces from the html document  

-j javascript minification  -> runs all javascript files (.js) through the google closure engine  
-c css minification  -> runs all css files (.css) through a yet undetermined css minifier  
-h html minification  -> runs all html files through a html minification  

-F do all the compressions


File Construction
-----------------
Types of files
Amassite Doc - HTML documents that become compiled files
Amassite Template - HTML documents that are used in other files and should not become compiled files
Amassite Script - Javascript files that should be minified
Amassite Style - CSS files that should be minified

All other files will be copied over to the output directory in the same file structure
If a folder only contained Amassite Template files the folder will not exist in the output directory
