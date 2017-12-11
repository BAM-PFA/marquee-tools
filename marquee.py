#!/usr/bin/env python3

import pyodbc
import configparser
import os

marqueeDir = os.dirname(os.path.abspath(__file__))
configPath = os.path.join(marqueeDir,'config','config.ini')
config = configparser.SafeConfigParser()
config.read(configPath)

outputDir = os.path.join(marqueeDir,'output-files')

def query():
	try:
		c = pyodbc.connect("DRIVER={FileMaker ODBC};DSN=marquee;SERVER=bampfa-pfm13.ist.1918.berkeley.edu;UID="+user+";PWD="+cred)
		c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
		c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
		c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
		c.setencoding(encoding='utf-8')
		cursor= c.cursor()
		
		# SQL TO GET REQUIRED METADATA VALUES FROM FM
		cursor.execute("""SELECT m_245a_CompleteTitle, AlternativeTitle, 
			AccessionNumberPrefix, AccessionNumberDepositorNumber, 
			AccessionNumberItemNumber, ProjectGroupTitle,
			m_257a_Country, m_260c_ReleaseYear,
			ct_DirectorsNames, Credits,
			GeneralNotes, m_945z_GeneralConditionNotes
			FROM CollectionItem WHERE AccessionNumberItemNumber = ?""",idNumber)	
		rows = cursor.fetchall()