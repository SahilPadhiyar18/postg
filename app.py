from telnetlib import STATUS
from this import d
from click import password_option
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def home_page():    
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
