from flask import Flask
from flask import render_template
import argparse

from TZA import *

app = Flask(__name__)

@app.route("/")
def index():
		return render_template("index.html")

@app.route("/data")
def data():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", nargs = 1, help = "specify the file to use", action = "store", dest = "file_name")
	args = parser.parse_args()
	if(args.file_name):
		file_name = str(args.file_name).strip("'[]")
	else:
		exit()

	return the_goods(file = file_name)

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)