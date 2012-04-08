import sqlite3

def foo(var):
	print 'hello'

def getData(name, date, dbloc):

	#connect to the database, change this to re-create the database.
	connection = sqlite3.connect(dbloc)
	cursor = connection.cursor()
	
	query = "SELECT * FROM candidates WHERE name = ?"
	cursor.execute(query, [name])
	
	
	print 'it all worked'