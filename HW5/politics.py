import sqlite3
import time

def foo(var):
	print 'hello'

def getData(name, date, race, dbloc):

	#connect to the database, change this to re-create the database.
	connection = sqlite3.connect(dbloc)
	cursor = connection.cursor()
	
	a=time.strptime(date, '%Y-%m-%d')
	nDate = time.strftime('%b %d, %Y',a).replace(' 0', ' ')
	
	query = "SELECT * FROM predictions WHERE candidate LIKE ? AND race = ? AND date = ?"
	cursor.execute(query, ["%"+name+"%", race, nDate])
	predictionResults = cursor.fetchall()
	
	i=-1
	for i,point in enumerate(predictionResults):
		print 'The closing value for',point[3],'on',date,'was',point[1]
	if i == -1:
		print 'There were no results foound for the given date'
		
	
	connection.close()