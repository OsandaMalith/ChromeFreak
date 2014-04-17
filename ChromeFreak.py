#!/usr/bin/python
'''
This is a open source forensic framework for Google Chrome. This application was fully written by me after researching 
on web browser Chrome. It was really fun exploring, making mistakes, a lot of expirience as a developer. Most of these code,
formatting, queries are my own.
If you plan to copy, redistribute it's okay but give credits to the original author. 

Notes:	Please note this tool may contain errors, and is provided "as it is". There is no guarantee
		that it will work on your target systems(s), as	the code may have to be adapted. 
		This is to avoid script kiddie abuse as well. 

Author: Osanda Malith Jayathissa 
Website: http://osandamalith.wordpress.com
'''
import os
import sys
import sqlite3
import json

# Do not edit unless you know what you are doing :)
class chromeFreak():
	def __init__(self, path):
		self.path =  path


	def HistoryObj(self):
		history = ''
		try:
			PathName = self.path + 'History'
			connexion = sqlite3.connect(PathName)
			c = connexion.cursor()
			c.execute("SELECT urls.url, urls.title, urls.visit_count,urls.typed_count, \
		        datetime((urls.last_visit_time/1000000)-11644473600,'unixepoch', 'localtime'),\
		        datetime((visits.visit_time/1000000)-11644473600,'unixepoch', 'localtime'), \
		        CASE (visits.transition & 255)\
		        WHEN 0 THEN 'User clicked a link'\
		        WHEN 1 THEN 'User typed the URL in the URL bar'\
		        WHEN 2 THEN 'Got through a suggestion in the UI'\
		        WHEN 3 THEN 'Content automatically loaded in a non-toplevel frame - user may not realize'\
		        WHEN 4 THEN 'Subframe explicitly requested by the user'\
		        WHEN 5 THEN 'User typed in the URL bar and selected an entry from the list - such as a search bar'\
		        WHEN 6 THEN 'The start page of the browser'\
		        WHEN 7 THEN 'A form the user has submitted values to'\
		        WHEN 8 THEN 'The user reloaded the page, eg by hitting the reload button or restored a session'\
		        WHEN 9 THEN 'URL what was generated from a replacable keyword other than the default search provider'\
		        WHEN 10 THEN 'Corresponds to a visit generated from a KEYWORD'\
		        END AS Description\
		        FROM urls, visits WHERE urls.id = visits.url")
			
			for row in c:
				try:
				    history += 'URL = %s\n' %str(row[0])
				    history += 'URL Title = %s\n' %str(row[1])
				    history += 'Number of Visits = %s\n' %str(row[2]) 
				    history += 'Last Visit (UTC) = %s\n' %str(row[4]) 
				    history += 'First Visit (UTC) = %s\n' %str(row[5]) 
				    if (str(row[6]) == 'User typed the URL in the URL bar'):
				        history += 'Description = %s\n\n' %(str(row[6]))
				        history += 'Number of Times Typed = %s\n' %(str(row[3]))
				    else:
				        history += 'Description = %s\n\n' %(str(row[6]))
				except UnicodeError:
				    continue
			return history
		
		except sqlite3.OperationalError, e:
			e = str(e)
			if (e == 'database is locked'):
			    print '[!] Make sure Google Chrome is not running in the background'
			    sys.exit(0)
			elif (e == 'no such table: urls'):
			    print '[!] Something wrong with the database name'
			    sys.exit(0)
			elif (e == 'unable to open database file'):
			    print '[!] Something wrong with the database path'
			    sys.exit(0)
			else:
				print e
	
	def DownloadsObj(self):
		downloads = ''
		try:
			PathName = self.path + 'History'
			connexion = sqlite3.connect(PathName)
			c = connexion.cursor()
			c.execute("SELECT url, current_path, target_path,datetime((end_time/1000000)-11644473600,'unixepoch', 'localtime'),\
			 datetime((start_time/1000000)-11644473600,'unixepoch', 'localtime'),\
			 received_bytes, total_bytes FROM downloads,\
			 downloads_url_chains where downloads.id = downloads_url_chains.id")

			for row in c:
				try:
					downloads += 'URL = %s\n' %str(row[0])
					downloads += 'Current Path = %s\n' %str(row[1])
					downloads += 'Target Path = %s\n' %str(row[2]) 
					downloads += 'End Time = %s\n' %str(row[3]) 
					downloads += 'Start Time = %s\n' %str(row[4])
					if (float(row[5]) < 1024):
						downloads += 'Received Bytes = %.2f Bytes\n' %(float(row[5]))
					if (float(row[5]) > 1024 and float(row[5]) < 1048576):
						downloads += 'Received Bytes = %.2f KB\n' %(float(row[5])/1024)
					elif (float(row[5]) > 1048576 and float(row[5]) < 1073741824):
						downloads += 'Received Bytes = %.2f MB\n' %(float(row[5])/1048576)
					else:
						downloads += 'Received Bytes = %.2f GB\n' %(float(row[5])/1073741824)

					if (float(row[6]) < 1024):
						downloads += 'Total Bytes = %.2f Bytes\n\n' %(float(row[6]))
					if (float(row[6]) > 1024 and float(row[6]) < 1048576):
						downloads += 'Total Bytes = %.2f KB\n\n' %(float(row[6])/1024)
					elif (float(row[6]) > 1048576 and float(row[6]) < 1073741824):
						downloads += 'Total Bytes = %.2f MB\n\n' %(float(row[6])/1048576)
					else:
						downloads += 'Total Bytes = %.2f GB\n\n' %(float(row[6])/1073741824)
				except UnicodeError:
					continue
			return downloads
		
		except sqlite3.OperationalError, e:
			e = str(e)
			if (e == 'database is locked'):
			    print '[!] Make sure Google Chrome is not running in the background'
			    sys.exit(0)
			elif (e == 'no such table: downloads'):
			    print '[!] Something wrong with the database name'
			    sys.exit(0)
			elif (e == 'unable to open database file'):
			    print '[!] Something wrong with the database path'
			    sys.exit(0)
			else:
				print e
			sys.exit(0) 
			
	def BookmarksObj(self):
		bookmarks = ''
		try:
			his = self.path + 'History'
			PathName = self.path+'Bookmarks'
			json_data=open(PathName)
			data = json.load(json_data)
			for i in range(0,2500):
				try:
					bookmarks += 'URL: %s\n' %str((data['roots']['bookmark_bar']['children'][i]['url']))
					bookmarks +=  'Name: %s\n' %str((data['roots']['bookmark_bar']['children'][i]['name']))
					bookmarks +=  'Type: %s\n' %str((data['roots']['bookmark_bar']['children'][i]['type']))
					date_time = str(data['roots']['bookmark_bar']['children'][i]['date_added'])
					con = sqlite3.connect(his).cursor().execute("select datetime((" + date_time+ "/1000000)-11644473600,'unixepoch', 'localtime')")
					for row in con:
						bookmarks +=  'Date: %s\n\n' %str(row[0])
				except UnicodeError:
				    continue
				except IndexError:
				    pass
			
			return bookmarks

		except IOError:
			print '[!] Bookmarks file not found'
			sys.exit(0)
		except Exception, e:
			print e
			sys.exit(0)
		
		except sqlite3.OperationalError, e:
			e = str(e)
			if (e == 'database is locked'):
			    print '[!] Make sure Google Chrome is not running in the background'
			    sys.exit(0)
			elif (e == 'no such table: urls'):
			    print '[!] Something wrong with the database name'
			    sys.exit(0)
			elif (e == 'unable to open database file'):
			    print '[!] Something wrong with the database path'
			    sys.exit(0)
			else:
				print e
				sys.exit(0)

	def CookiesObj(self):
		cookie = ''
		try:
		    PathName = self.path + 'Cookies'
		    connexion = sqlite3.connect(PathName)
		    c = connexion.cursor()
		    c.execute("select datetime((creation_utc/1000000)-11644473600,'unixepoch', 'localtime'),\
		        host_key,name,value,path,datetime((expires_utc/1000000)-11644473600,'unixepoch',\
		         'localtime'),secure,httponly,datetime((last_access_utc/1000000)-11644473600,'unixepoch',\
		          'localtime') from cookies;")
		    for row in c:
		        cookie += 'Date Created: %s\n' %(str(row[0]))
		        cookie += 'Host: %s\n' %(str(row[1]))
		        cookie += 'Name: %s\n' %(str(row[2]))
		        cookie += 'Value: %s\n' %(str(row[3]))
		        cookie += 'Path: %s\n' %(str(row[4]))
		        cookie += 'Expiry Date: %s\n' %(str(row[5]))
		        if (str(row[6]) == '0'):
		            cookie += 'Secure Cookie: %s\n' %('No')
		        else:
		            cookie += 'Secure Cookie: %s\n' %('Yes')
		        if (str(row[7]) == '0'):
		            cookie += 'HttpOnly Cookie: %s\n\n' %('No')
		        else:
					cookie += 'HttpOnly Cookie: %s\n' %('Yes')
					cookie += 'Last Access: %s\n\n' %(str(row[8]))
		    return cookie
		    while True:
				msg = str(raw_input('[?] Do you want to save to a file? ')).lower()
				try:
				    if msg[0] == 'y':
				        name = str(raw_input('[*] Enter a filename: '))
				        SaveObj = Savefile(name,cookie)
				        print SaveObj.save()
				    	mainMenu()   
				    if msg[0] == 'n':
				        print cookie
				        mainMenu()
				        break
				    else:
				        print '[!] Enter a valid choice'
				except Exception, e:
				    print e
				    continue
		except sqlite3.OperationalError, e:
			e = str(e)
			if (e == 'database is locked'):
			    print '[!] Make sure Google Chrome is not running in the background'
			    sys.exit(0)
			elif (e == 'no such table: cookies'):
			    print '[!] Something wrong with the database name'
			    sys.exit(0)
			elif (e == 'unable to open database file'):
			    print '[!] Something wrong with the database path'
			    sys.exit(0)
			else:
				print e	 
				sys.exit(0)

	
class Savefile():
    def __init__(self, filename, component):
        self.name = filename
        self.comp = component
        self.comp += '[~] This file was generated by ChromFreak'
        self.comp += '\n[~] Website: http://osandamalith.github.io/ChromeFreak/\n'

    def save(self):
        file = open(self.name+'.txt' , "w")
        file.write(self.comp)
        file.close()
        return '[~] File Saved to ' + os.path.abspath(self.name) + '.txt'

def fullReport(PathName):
	full = ''
	full += banner() + '\n\n'
	full += '---------------\n[*] History\n---------------\n'
	full += chromeFreak(PathName).HistoryObj() + '\n'
	full += '---------------\n[*] Downloads\n---------------\n'
	full += chromeFreak(PathName).DownloadsObj() + '\n'
	full += '---------------\n[*] Bookmarks\n---------------\n'
	full += chromeFreak(PathName).BookmarksObj() + '\n'
	full += '---------------\n[*] Cookies\n---------------\n'
	full += chromeFreak(PathName).CookiesObj()
	
	while True:
		msg = str(raw_input('[?] Do you want to save to a file? ')).lower()
		try:
		    if msg[0] == 'y':
		        name = str(raw_input('[*] Enter a filename: '))
		        SaveObj = Savefile(name,full)
		        print SaveObj.save()
		    	mainMenu()   
		    if msg[0] == 'n':
		        print full
		        mainMenu()
		        break
		    else:
		        print '[!] Enter a valid choice'
		except Exception, e:
		    print e
		    continue


def Start(component):
	while True:
		msg = str(raw_input('[?] Do you want to save to a file? ')).lower()
		try:
		    if msg[0] == 'y':
		        name = str(raw_input('[*] Enter a filename: '))
		        SaveObj = Savefile(name,component)
		        print SaveObj.save()
		    	mainMenu()   
		    if msg[0] == 'n':
		        print component
		        mainMenu()
		        break
		    else:
		        print '[!] Enter a valid choice'
		except Exception, e:
		    print e
		    continue	

def mainMenu():
	while True:
		try:
			choice = str(raw_input('[?] Do you want to go to the main menu?')).lower()
			if choice[0] == 'y':
				main()
				break
			if choice[0] == 'n':
				sys.exit(0)
				break
		except ValueError:
			sys.exit(0)
	
def banner():
	banner = '''
     ,gggg,                                                               
   ,88"""Y8b,,dPYb,                                                       
  d8"     `Y8IP'`Yb                                                       
 d8'   8b  d8I8  8I                                                       
,8I    "Y88P'I8  8'                                                       
I8'          I8 dPgg,    ,gggggg,    ,ggggg,    ,ggg,,ggg,,ggg,    ,ggg,  
d8           I8dP" "8I   dP""""8I   dP"  "Y8ggg,8" "8P" "8P" "8,  i8" "8i 
Y8,          I8P    I8  ,8'    8I  i8'    ,8I  I8   8I   8I   8I  I8, ,8I 
`Yba,,_____,,d8     I8,,dP     Y8,,d8,   ,d8' ,dP   8I   8I   Yb, `YbadP' 
  `"Y888888888P     `Y88P      `Y8P"Y8888P"   8P'   8I   8I   `Y8888P"Y888

		,gggggggggggggg                                       
		dP""""""88""""""                             ,dPYb,    
		Yb,_    88                                   IP'`Yb    
		 `""    88                                   I8  8I    
		     ggg88gggg                               I8  8bgg, 
		        88   8,gggggg,   ,ggg,     ,gggg,gg  I8 dP" "8 
		        88    dP""""8I  i8" "8i   dP"  "Y8I  I8d8bggP" 
		  gg,   88   ,8'    8I  I8, ,8I  i8'    ,8I  I8P' "Yb, 
		   "Yb,,8P  ,dP     Y8, `YbadP' ,d8,   ,d8b,,d8    `Yb,
		     "Y8P'  8P      `Y8888P"Y888P"Y8888P"`Y888P      Y8

[*] Author: Osanda Malith Jayathissa 
[*] Follow @OsandaMalith
[*] Description: A Cross-Platform Forensic Framework for Google Chrome
'''
	return banner
	

def main():
	if os.name == "nt":
		os.system('cls')
	else:
		os.system('clear')
	print banner()
	try:
		if os.name == "nt":
			# This is the Windows Path
			PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
			if (os.path.isdir(PathName) == False):
				print '[!] Chrome Doesn\'t exists' 
				sys.exit(0)
		elif os.name == "posix":
			# This is the Linux Path
			PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
			if (os.path.isdir(PathName) == False):
				print '[!] Chrome Doesn\'t exists' 
				sys.exit(0)
		elif ((os.name == "posix") and (os.path.isdir(PathName) == False)):
			# This is the OS X Path
			PathName = os.getenv('HOME') + "/Library/Application Support/Google/Chrome/Default/"
			if (os.path.isdir(PathName) == False):
				print '[!] Chrome Doesn\'t exists' 
				sys.exit(0)
		
		while True:
			try:
				choice = int(raw_input("[?] What do you like to invistigate? \
					\n1. History\n2. Downloads\n3. Bookmarks\n4. Cookies\n5. Full Report\n6. Exit\n" ))
			except ValueError:
				print '[!] Enter Only a Number'
				continue
		
			if choice == 1:
				history = chromeFreak(PathName).HistoryObj()
				Start(history)
				break
			if choice == 2:
				downloads = chromeFreak(PathName).DownloadsObj()
				Start(downloads)
				break
			if choice == 3:
				bookmarks = chromeFreak(PathName).BookmarksObj()
				Start(bookmarks)
				break
			if choice == 4:
				cookies = chromeFreak(PathName).CookiesObj()
				Start(cookies)
				break
			if choice == 5:
				fullReport(PathName)
			if choice == 6:
				sys.exit(0)
			else:
				print '[!] Invalid Choice'

	except KeyboardInterrupt:
		print '[!] Ctrl + C detected\n[!] Exiting'
		sys.exit(0)
	except EOFError:
		print '[!] Ctrl + D detected\n[!] Exiting'
		sys.exit(0)
	

if __name__ == "__main__": 
    main()  
