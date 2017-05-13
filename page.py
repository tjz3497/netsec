from flask import Flask
from flask import render_template
import argparse
import plotly.tools as tools
import plotly.offline as offline
import plotly.graph_objs as go

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
	fig = tools.make_subplots(rows=1, cols=2, subplot_titles=("Distance From Average (seconds)", "Map"))

	fig.append_trace(bar1, 1, 1)
	fig.append_trace(bar2, 1, 2)
	fig['layout'].update(height=600, width=600, title='ghfg')
	offline.plot(fig)

#	offline.plot({
#    "data": [go.Bar(x=ip_s, y=dists)],
#    "data": [go.Bar(x=[1,2,3], y=dists)]
#	})

	return(exit())


@app.route("/data")
def data():
	
	

	return the_goods(file = file_name)


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)