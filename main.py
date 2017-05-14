from flask import Flask,redirect
import json
import argparse
import plotly.tools as tools
import plotly.offline as offline
import plotly.graph_objs as go
import pandas as pd

from TZA import *

app = Flask(__name__)

@app.route("/")
def index():
	

	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", nargs = 1, help = "specify the file to use", action = "store", dest = "file_name")
	args = parser.parse_args()
	if(args.file_name):
		file_name = str(args.file_name).strip("'[]")
	else:
		print("Error: You must enter a filename (-f [file])")
		exit()

	datas = the_goods(file = file_name)


	ip_s = []
	dists = []
	for each in datas[3]:
		ip_s.append(each['ip'])
		dists.append(each['distance from average'])

	dists2 = []
	for each in datas[0]:
		dists2.append(each['distance from average'])
	#print(dists2)

	per_country_avg = {}
	num_country = {}
	for code, dist in zip(datas[1], dists2):
		if(code in per_country_avg):
			num_country[code] += 1
			per_country_avg[code] = int((per_country_avg[code] + dist) / num_country[code])
		else:
			per_country_avg[code] = dist
			num_country[code] = 1

	data = [ dict(
	        type = 'choropleth',
	        locations = datas[1],
	        z = dists2,
	        text = datas[1],
	        colorscale = [[0,"rgb(172,10,5)"],[0.35,"rgb(190,60,40)"],[0.5,"rgb(245,100,70)"],\
	            [0.6,"rgb(245,120,90)"],[0.7,"rgb(247,137,106)"],[1,"rgb(220, 220, 220)"]],
	        autocolorscale = False,
	        reversescale = True,
	        #colorscale = ['Virdis'],
	        marker = dict(
	            line = dict (
	                color = 'rgb(180,180,180)',
	                width = 0.5
	            ) ),
	        colorbar = dict(
	            #autotick = False,
	            autotick = True,
	            #tickprefix = '',
	            title = 'Distance From Average (Seconds)'),
	      ) ]

	layout = dict(
	    title = 'Average Variance per Country',
	    geo = dict(
	        showframe = False,
	        showcoastlines = True,
	        projection = dict(
	            type = 'Mercator'
	        )
	    )
	)

	map1 = dict( data=data, layout=layout )
	offline.plot( map1, validate=False, filename = "map_plot.html")

	bar1 = go.Bar(
		x=ip_s,
		y=dists,
		marker=dict(
				color='rgb(225,202,158)'		)
	)

	barlay = go.Layout(
		title = 'Suspicious Connection Variance from Average Variance'
	)

	offline.plot(
		{
    	"data": [go.Bar(x=ip_s, y=dists)],
    	"layout": barlay
		},
		filename='suspicious_bar.html'
	)

	info = "Average Connection Time: " + str(datas[2])
	print(info)

	return(redirect("http://www.github.com/tjz3497/netsec"))

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)