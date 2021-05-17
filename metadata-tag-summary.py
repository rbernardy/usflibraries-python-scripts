import os, re, pathlib, sys
from datetime import datetime

platform=sys.platform
print("platform=[" + platform + "].")
userdir = pathlib.Path.home()
print ("userdir=[" + str(userdir) + "].")

basedir=os.path.join(userdir,"temp")

if (not os.path.exists(basedir)):
	os.mkdir(basedir)

mdir=os.path.join(basedir,"mods")
print("source dir for modsxml files=[" + mdir + "].")

if (not os.path.exists(mdir)):
	print("modsxml files are expected in [" + mdir + "].")
	exit()

odir = os.path.join(basedir,"tags")

if (not os.path.exists(odir)):
	os.mkdir(odir)

print("tag text files will be written to [" + odir + "].")

files=os.scandir(mdir)

mynow = datetime.now()
path_log=os.path.join(basedir,"mylog-" + mynow.strftime("%Y%m%d-%H%M%S-%f") + ".txt")
print("New log file will be written to [" + path_log + "].")
file_log=open(path_log,"a+")

for file in files:
	
	if (file.name.endswith(".txt")):
		print ("Skipping [" + file.name + "].")
		continue

	print (file.name)
	path=os.path.join(mdir,file.name)
	with open(path,mode="r",encoding="utf-8") as file:
		data=file.read()

	print ("data length is " + str(len(data)))

	p=re.compile('(?<=<)([^\/]*?)((?= \/>)|(?=>))')
	m = p.findall(data)

	tags=[]
	idx=0

	if m:
		msg="Matches found in " + file.name + "."
		file_log.write("\r\n" + msg + "\r\n")
		
		tags=[]
		
		for tag in m:
			idx=idx+1
			
			idx2=0
			for tup in tag:

					if (len(str(tup))>0):
						idx2=idx2+1

						# Exclude some 'tags'

						if (not tup.startswith("usfldc:record") and not tup.startswith("?xml") and not tup.startswith("!--") and not tup == "mods:mods"):
							tags.append(tup)
	
	else:
		tags=[]
		msg = "NO matches in " + file.name + "\r\n"
		print (msg)
		file_log.write(msg)
		input()

	if (len(tags)>0):
		msg="There ARE tags for [" + file.name + "].\r\n"
		print(msg)
		file_log.write(msg)

		tags_final=list(dict.fromkeys(tags))
		tags_final.sort()

		msg=str(len(tags_final)) + " items added.\r\n"
		print(msg)
		file_log.write(msg)

		path_output=file.name.replace(".xml",".tags.txt").replace(os.path.sep + "mods" + os.path.sep,os.path.sep + "tags" + os.path.sep)
		msg=path_output
		print(msg)
		file_log.write(msg)
	
		if (os.path.exists(path_output)):
			os.remove(path_output)

		file_output=open(path_output,"a+")

		for mytag in tags_final:
			print (mytag)
			file_output.write(mytag + "\r\n")

		file_output.close()
	else:
		msg="NO tags for [" + file.name + "]."
		print(msg)
		file_log.write(msg)
		input()

	print ("\r\n" + file.name + "\r\n")
	print ("_________________________________________________________________________________________________________________")

file_log.close()