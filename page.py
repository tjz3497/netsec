from flask import Flask
from flask import render_template
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

	df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

	ip_s = []
	dists = []
	for each in datas[0]:
		ip_s.append(each['ip'])
		dists.append(each['distance from average'])

	print(datas[1])
	print(dists)

	data = [ dict(
	        type = 'choropleth',
	        locations = datas[1],
	        z = dists,
	        text = datas[1],
	        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
	            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
	        autocolorscale = False,
	        reversescale = True,
	        #colorscale = ['Virdis'],
	        marker = dict(
	            line = dict (
	                color = 'rgb(180,180,180)',
	                width = 0.5
	            ) ),
	        colorbar = dict(
	            autotick = False,
	            tickprefix = '$',
	            title = 'Distance From Average (Seconds)'),
	      ) ]

	layout = dict(
	    title = '2014 Global GDP',
	    geo = dict(
	        showframe = False,
	        showcoastlines = False,
	        projection = dict(
	            type = 'Mercator'
	        )
	    )
	)

	fig = dict( data=data, layout=layout )
	offline.plot( fig, validate=False)
	"""
	ip_s = []
	dists = []
	for each in datas:
		ip_s.append(each['ip'])
		dists.append(each['distance from average'])

	bar1 = go.Bar(
		x=ip_s,
		y=dists
	)
	bar2 = go.Bar(
		x=[1,2,3],
		y=dists
	)


	fig = tools.make_subplots(rows=2, cols=1, subplot_titles=("Distance From Average (seconds)", "Map"))

	fig.append_trace(bar1, 1, 1)
	fig.append_trace(bar2, 2, 1)
	fig['layout'].update(height=800, width=800, title='Data')
	offline.plot(fig)

#	offline.plot({
#    "data": [go.Bar(x=ip_s, y=dists)],
#    "data": [go.Bar(x=[1,2,3], y=dists)]
#	})
	"""
	return(exit())


@app.route("/data")
def data():
	
	

	return the_goods(file = file_name)


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)