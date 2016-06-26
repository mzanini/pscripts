import sys, re, os

def createCoClassRepl(matchobj):
	prodIdRE = re.search('vi_progid\((.+?)\)', matchobj.group(0))
	uuidRE = re.search('uuid\((.+?)\)', matchobj.group(0))
	createCoClassString = 'CREATE_COCLASS(' + prodIdRE.group(1) + ', ' + uuidRE.group(1) + ')'
	print('Replacing: \n' + matchobj.group(0))
	print('With: \n' + createCoClassString)
	return createCoClassString

def addIncludeRepl(matchobj):
	includeString = matchobj.group(0) + '\n#include \"createCoClass.h\"'
	print('Replacing: \n' + matchobj.group(0))
	print('With: \n' + includeString)
	return includeString

def substituteCoclassDeclaration(fileName):
	print('Reading from file: ' + fileName)
	f = open(fileName, 'r')
	fileContent = f.read()
	f.close()

	coClassRE = re.compile('\[[^\]]*?coclass.*?\]', re.DOTALL)
	includeRE = re.compile('(.*?\#pragma once.*)|(.*?\#include.*)')

	newFileContent = coClassRE.sub(createCoClassRepl, fileContent)
	if (newFileContent != fileContent and (includeHeaderFile == "Y" or includeHeaderFile == '' )):	
		newFileContent = includeRE.sub(addIncludeRepl, newFileContent, 1)

	outfile = open(fileName, 'w')
	outfile.write(newFileContent)
	outfile.close()



print('This program will look in all header and source files, traversin directories recursively, to replace coclass declarations with CREATE_COCLASS macro.')
includeHeaderFile = input('Do you want the script to include the header file createCoClass.h for you when it is needed? [Y/n]')
input('Press enter when you are ready to start! The process is automatic and no additional user input will be asked.')

for root, dirs, files in os.walk("."):
	headerFiles = [fi for fi in files if fi.endswith( ('.h', '.cpp') )  ]
	for name in headerFiles:
		substituteCoclassDeclaration(os.path.join(root, name))


