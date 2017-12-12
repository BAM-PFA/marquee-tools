#!/usr/bin/env python3

import pyodbc
import configparser
import os

def query(host,user,pw):
	try:
		c = pyodbc.connect("DRIVER={FileMaker ODBC};DATABASE=Marquee;SERVER="+host+";UID="+user+";PWD="+pw)
		print(c)
		# c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
		# c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
		# c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
		# c.setencoding(encoding='utf-8')
		cursor= c.cursor()
		
		# SQL TO GET REQUIRED VALUES FROM FM
		cursor.execute("""SELECT field01,field02,field03,field04,
			field05,field06,field07,field08
			FROM marquee""")	
		rows = cursor.fetchall()
		for result in rows:
			if result == None:
				result = ''

		currentValues = [x for y in rows for x in y]
		return currentValues
	except:
		print("something failed in the FileMaker query")

def write():
	marqueeDir = os.path.dirname(os.path.abspath(__file__))
	configPath = os.path.join(marqueeDir,'config','config.ini')
	outputDir = os.path.join(marqueeDir,'output-files')
	print(configPath)
	print(outputDir)	
	config = configparser.SafeConfigParser()
	config.read_file(open(configPath,'r'))
	user = config['FileMaker']['user']
	pw = config['FileMaker']['pass']
	host = config['FileMaker']['host']
	# print(os.listdir(outputDir))
	# print(query())
	for textfile in os.listdir(outputDir):
		textfilePath = os.path.join(outputDir,textfile)
		if textfile.endswith(".txt"):
			fileNumber = int(textfile[0])
			fileIndex = fileNumber - 1
			try: 
				with open(textfilePath,'w+') as valuefile:
					valuefile.write(query(host,user,pw)[fileIndex])
			except:
				print("something went wrong")
				pass
				print(valuefile)

if __name__ == '__main__':
	write()