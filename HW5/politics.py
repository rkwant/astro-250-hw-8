import sqlite3
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

def getData(name, date, race, dbloc):
	'''
	method to find the prediction data for a particular date and print the result
	name: name of the candidate
	date: date of interest
	race: political race
	dbloc: location of the database
	'''
	
	#connect to the database
	connection = sqlite3.connect(dbloc)
	cursor = connection.cursor()
	
	#convert the date to the proper format
	a=time.strptime(date, '%Y-%m-%d')
	nDate = time.strftime('%b %d, %Y',a).replace(' 0', ' ')
	
	#get the data
	query = "SELECT * FROM predictions WHERE candidate LIKE ? AND race = ? AND date = ?"
	cursor.execute(query, ["%"+name+"%", race, nDate])
	predictionResults = cursor.fetchall()
	
	#pint it
	i=-1
	for i,point in enumerate(predictionResults):
		print 'The closing value for',point[3],'on',date,'was',point[1]
	if i == -1:
		print 'There were no results foound for the given date'
		
	
	connection.close()
		
def plotData(name, date, race, dbloc):
	'''
	method to plot a candidate's prediction data and highlighte a particlar date
	name: name of the candidate
	date: date of interest
	race: political race
	dbloc: location of the database
	'''
	
	#connect to the db
	connection = sqlite3.connect(dbloc)
	cursor = connection.cursor()
	
	#convert the input date to the db date format
	a=time.strptime(date, '%Y-%m-%d')
	searchDate = dt.datetime(a.tm_year, a.tm_mon, a.tm_mday)
		
	#get the results
	query = "SELECT * FROM predictions WHERE candidate LIKE ? AND race = ?"
	cursor.execute(query, ["%"+name+"%", race])
	predictionResults = cursor.fetchall()
	
	#arrays and tuple to store the results
	dates = []
	prices = []
	targetPoint = (0,0)
	
	#store each point, converting dates to the appropriate format
	for point in predictionResults:
		t = time.strptime(point[0], '%b %d, %Y')
		d = dt.datetime(t.tm_year, t.tm_mon, t.tm_mday)
		dates.append(d)
		prices.append(point[1])
		
		#make a note of the point of interest
		if d==searchDate: targetPoint = (d, point[1])
		
	dates = np.array(dates)
	prices = np.array(prices)
	
	#plot the data
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(dates, prices)
	fig.autofmt_xdate()
	
	#annotate the target point, if it exists
	if targetPoint != (0,0):
		ax.plot(targetPoint[0], targetPoint[1], 'ro')
		ax.annotate(date,
            xy=(targetPoint[0], targetPoint[1]), xycoords='data',
            xytext=(-60, -50), textcoords='offset points',
            arrowprops=dict(arrowstyle="simple",
			patchA=None,
			patchB=None,
			facecolor='white',
			connectionstyle="angle3"),
            )
	ax.set_title('Prediction data for '+point[3])
	ax.set_xlabel('Date')
	ax.set_ylabel('Closing Price')
	plt.show()