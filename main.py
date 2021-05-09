from flask import Flask, redirect, url_for, request, render_template
import sys, os, math
from werkzeug.utils import secure_filename
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np


app=Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def homepage():
	return render_template('index.html',path=None)


@app.route('/',methods=['POST'])
def result():
	try:
		if request.method=='POST':
			select=request.form['select']
			select = int(select)
			rowlimit=request.form['rowlimit']
			if rowlimit == "":
				return redirect(url_for('homepage'))
			rowlimit = int(rowlimit)
			print(select)
			print(rowlimit)
			if 'file' not in request.files:
				return redirect(url_for('homepage'))
			file = request.files['file']
			filename = secure_filename(file.filename)
			print(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print(filename.split('.')[0])
			if select == 1:
				path = makeSankey(filename, rowlimit)
				print(path)
				return render_template('index.html',path=path)
			elif select == 2:
				makeParallel(filename, rowlimit)
			elif select == 3:
				makeSimple(filename, rowlimit)
			return redirect(url_for('homepage'))
	except:
		pass

def makeSankey(filename, rowlimit):
	with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
		data = json.load(f)
	df = pd.DataFrame(data)	
	df = df.head(rowlimit)
	df = df[['userId','id',]]
	print(df)
	# data
	label = ["0","1","2","3","4","5","6","7","8","9","10"]
	source = np.array(df['userId'].astype(int))
	print(source)
	target = np.array(df['id'].astype(int))
	value= np.random.randint(1,10,rowlimit)
	# links
	link = dict(source = source, target = target, value = value)
	node = dict(label=label, pad=50, thickness=5)
	data = go.Sankey(link = link, node=node)
	#plot
	fig = go.Figure(data)
	cur_dir = str(os.path.abspath(os.getcwd())) + '/'
	print(cur_dir)
	image_path = str(cur_dir) + "./static/styles/image.png"
	print(image_path)
	try:
		fig.write_image(image_path)
		# plotly.offline.plot(fig, filename="./templates/content.html",auto_open=False)
	except:
		print('not working')	
	return image_path


def makeParallel(filename, rowlimit):
	pass

def makeSimple(filename, select, rowlimit):
	pass

if __name__ == '__main__':
	if not os.path.exists("images"):
		os.mkdir("images")
	if not os.path.exists("files"):
		os.mkdir("files")	
	app.run()
