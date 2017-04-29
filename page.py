from flask import Flask
from flask import render_template
from TZA import *

app = Flask(__name__)

@app.route("/")
def index():
		return render_template("index.html")

@app.route("/data")
def data():
	return the_goods()



if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)