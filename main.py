#!/usr/bin/env python
import os
from flask import current_app, Flask, redirect, url_for
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from bson.binary import Binary
import gridfs
import base64
from werkzeug import FileStorage, secure_filename
import time

application = Flask(__name__)


# database connection
def db_conn():
    client = MongoClient("mongodb://146.148.84.68/mongodb-1-server-1-data")
    db = client.firstdb
    collection = db.user
    return db


usern = None
# global username

print"connected to database"


@application.route('/', methods=['POST', 'GET'])
def run():
    return render_template("index.html")


@application.route('/newuser', methods=['POST', 'GET'])
def newuser():
    global usern
    db = db_conn()
    username = request.form['username']
    password = request.form['password']

    var = {
        'username': username,
        'password': password
    }
    db.user.insert(var)
    output = """<h1> Sucessfully inserted, go back to login</h1>"""
    return output


@application.route('/login', methods=['POST', 'GET'])
def login():
    global usern
    db = db_conn()
    print "inside login"

    username = request.form['user']
    password = request.form['pass']
    count = db.user.find({'username': username, 'password': password}).count() > 0
    print count
    usern = username
    if count:
        text = "successfully logged in"
        return render_template("loginoutput.html", text=text)
    else:
        text = "please enter your username and password again"

        output1 = """<h1>%s</h1>""" % (text)
        return output1


@application.route('/upload', methods=['POST', 'GET'])
def upload():
    global usern
    db = db_conn()
    image_file = request.files['pic']
    print image_file.filename
    file_name = image_file.filename
    target = image_file.read()
    size = len(target)
    comm = request.form['comments']
    end = time.time()
    print size
    count = 0
    for item in db.fs.files.find({"user": usern}):
        print item
        count += 1
        print count
    if size < 5000000:
        if count < 5:
            # encoded_string=base64.b64encode(target)
            print "inside if"
            fs = gridfs.GridFS(db)
            stored = fs.put(target, filename=file_name, user=usern, comment=comm)
            print stored
        else:
            raise ValueError('count crossed')
    else:
        raise ValueError('size crossed')

    return render_template("insert.html", )


@application.route('/fetchmine', methods=['POST', 'GET'])
def fetchmine():
    db = db_conn()
    fs = gridfs.GridFS(db)
    diclist = []

    for item in db.fs.files.find({"user": usern}):
        com = None
        file_name = item['filename']
        if 'comment' in item.keys():
            com = item['comment']
        picture = fs.find_one({"filename": file_name}).read()
        picdata = "data:image/jpeg;base64," + base64.b64encode(picture)
        dicvar = {}
        # dicvar['user'] = user_name
        dicvar['file_name'] = file_name
        dicvar['com'] = com
        dicvar['image'] = picdata
        # print dicvar
        diclist.append(dicvar)

    return render_template("display.html", lists=diclist)


@application.route('/fetch', methods=['POST', 'GET'])
def fetch():
    global usern
    db = db_conn()
    fs = gridfs.GridFS(db)

    diclist = []

    for item in db.fs.files.find():
        com = None
        user_name = None
        file_name = item['filename']
        if 'user' in item.keys():
            user_name = item['user']
        if 'comment' in item.keys():
            com = item['comment']
        picture = fs.find_one({"filename": file_name}).read()
        picdata = "data:image/jpeg;base64," + base64.b64encode(picture)
        dicvar = {}
        dicvar['user'] = user_name
        dicvar['file_name'] = file_name
        dicvar['com'] = com
        dicvar['image'] = picdata
        # print dicvar
        diclist.append(dicvar)
        # print diclist

    return render_template("displayall.html", lists=diclist)


@application.route('/delete', methods=['POST', 'GET'])
def delete():
    global usern
    db = db_conn()
    name = request.form['images']
    c = db.fs.files
    try:
        print("going inside try")
        c.delete_one({"filename": name})
        return redirect(url_for('fetchmine'))
    except:
        return "could not delete"


if __name__ == "__main__":
    application.run()

