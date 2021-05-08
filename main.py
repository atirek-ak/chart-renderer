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

conn = sql.connect('database.db')
# curr=conn.cursor()
# conn.execute('CREATE TABLE users (Name TEXT, Password REAL)')
# curr.execute("INSERT INTO  users (Name, Password) VALUES (?,?)",("","",))
# conn.commit()
conn.close()

def render_welcome():
	global global_current_user
	con = sql.connect('database.db')
	cur=con.cursor()
	cursor = con.execute("SELECT * FROM " + str(global_current_user))
	cur.execute("SELECT * FROM " + str(global_current_user))
	data = cur.fetchall()
	lis = []
	for item in cursor.description:
		lis.append(item[0])
	con.commit()
	con.close()
	return data,lis


@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/',methods=['POST'])
def result():
	try:
		if request.method=='POST':
			select=request.form['select']
			rowlimit=request.form['rowlimit']
			print(select)
			print(rowlimit)
			if 'file' not in request.files:
				return render_template("index.html")
			file = request.files['file']
			filename = secure_filename(file.filename)
			print(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print(filename.split('.')[0])
			render_data(filename)

			return render_template("index.html")
	except:
		pass
		# con.rollback()

def render_data(filename):
	with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
		data = json.load(f)
	df = pd.DataFrame(data)	
	con = sql.connect('database.db')
	cur=con.cursor()
	df.to_sql(filename.split('.')[0],con)
	con.commit()
	con.close()


if __name__ == '__main__':
	app.run()
