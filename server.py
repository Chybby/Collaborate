#!/usr/bin/env python2.7

from flask import Flask, render_template
from flask.ext import login
import sqlite3
import json

from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '2SPOOPY'

def get_cursor():
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    return cur

# login stuff
login_manager = login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(zid):
    #return db.session.query(User).get(zid)
    res = cur.execute('''
    SELECT zid, first_name, surname FROM users
    ''')

    if res:
        row = res.fetchone()
        obj = {
            'zid': row[0],
            'first_name': row[1],
            'surname': row[2]
        }
        return obj

@app.route('/json/course_codes')
def course_codes():
    cur = get_cursor()

    res = cur.execute('''
    SELECT
        code
    FROM
        courses
    ''')

    rows = res.fetchall()
    codes = [row[0] for row in rows]

    return json.dumps(codes)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/course/<code>')
def course(code):
    cur = get_cursor()

    res = cur.execute('''
    SELECT
        name, description
    FROM
        courses
    WHERE
        code = ?
    ''', (code,))
    
    name, desc = res.fetchone()

    res = cur.execute('''
    SELECT
        id
    FROM
        offerings
    WHERE
        code = ? AND
        year = ? AND
        session = ?
    ''', (code, 2014, 'S1'))

    offering_id = res.fetchone()[0]

    res = cur.execute('''
    SELECT
        id, given_names, surname
    FROM
        lecturings
    INNER JOIN
        lecturers
    ON
        lecturings.lecturer_id = lecturers.id
    WHERE
        offering_id = ?
    ''', (offering_id,))

    lecturers = res.fetchall()
    lecturer_names = ['%s %s' % (l[1], l[2]) for l in lecturers]

    return render_template('course.html',
            code=code,
            name=name,
            desc=desc,
            lecturers=lecturer_names)

@app.route('/rate')
def rate():
    return render_template('rate.html')

if __name__ == '__main__':
    app.run(debug=True)
