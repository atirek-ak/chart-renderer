from flask import Flask, redirect, url_for, request, render_template, session, flash
import sqlite3 as sql
from random import randint
import sys, os, math
from werkzeug.utils import secure_filename
import pandas as pd
import json

app=Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# conn = sql.connect('database.db')
# curr=conn.cursor()
# conn.execute('CREATE TABLE users (Name TEXT, Password REAL)')
# curr.execute("INSERT INTO  users (Name, Password) VALUES (?,?)",("","",))
# conn.commit()
# conn.close()

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
			name=request.form['ID']
			password=request.form['Password']
			con=sql.connect("database.db")
			cur = con.cursor()
			val=None
			cur.execute("SELECT * FROM users WHERE name = ?", (name,))
			val=cur.fetchone()
			if val[0] == None or val[1] != password:
				return render_template("index.html")
			else:	
				global global_current_user
				session['username']=name
				global_current_user=name
				global global_file_upload
				data = None
				if global_file_upload:
					data,headers = render_welcome()
					return render_template("welcome.html",data=data,headers=headers[1:])
				else:
					return render_template("welcome.html")
			con.close()	
	except:
		con.rollback()

if __name__ == '__main__':
	app.run()
