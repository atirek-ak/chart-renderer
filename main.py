from flask import Flask, redirect, url_for, request, render_template, session, flash
import sqlite3 as sql
from random import randint
import sys, os, math
from werkzeug.utils import secure_filename
import pandas as pd
import json

app=Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# conn = sql.connect('database.db')
# curr=conn.cursor()
# conn.execute('CREATE TABLE users (Name TEXT, Password REAL)')
# curr.execute("INSERT INTO  users (Name, Password) VALUES (?,?)",("","",))
# conn.commit()
# conn.close()

@app.route('/')
def homepage():
	return render_template('index.html')


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
			# renderData(filename)
			if select == 1:
				
				makeSankey(filename, rowlimit)
			elif select == 2:
				makeParallel(filename, rowlimit)
			elif select == 3:
				makeSimple(filename, rowlimit)
			return redirect(url_for('homepage'))
	except:
		pass

def renderData(filename):
	with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
		data = json.load(f)
	df = pd.DataFrame(data)	
	con = sql.connect('database.db')
	cur=con.cursor()
	df.to_sql(filename.split('.')[0],con)
	con.commit()
	con.close()

def makeSankey(filename, rowlimit):
	with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
		data = json.load(f)
	df = pd.DataFrame(data)	
	df = df.head(rowlimit)
	print(df)

def makeParallel(filename, rowlimit):
	pass

def makeSimple(filename, select, rowlimit):
	pass

if __name__ == '__main__':
	app.run()
