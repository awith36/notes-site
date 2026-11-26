#!/bin/python

from flask import Flask, render_template, request, jsonify, session
import json
# import requests
import secrets






# loading the database
def load():
    with open("database.json", "r") as file:
       database = json.load(file)

# load the database ✨but not a function✨
with open("database.json", "r") as file:
   database = json.load(file)



#app stuff
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


# hosting the login html
@app.route("/")
def index():
    return render_template("index.html")


# main page hosting
@app.route("/notes")
def notes():
    return render_template("notes.html")


# SIGNUP

# hosting the signup page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# creating the new username
@app.route("/newUser", methods=["POST"])
def newUser():

    # get the user input and set the variables to it
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # store the username in the session cookie
    session["username"] = username

    # write data to the python dictionary
    database["users"].append(data)
    database["documents"][username] = "start type here"

    # write python dictionary to the database and reload
    with open("database.json", "w") as file:
        json.dump(database, file, indent=4)
    load()

    # confirm saved to the user
    return jsonify({"status": "saved"})




# incorect password
@app.route("/access-denied")
def access():
    return render_template("denied.html")


# reciving the json from the login screen
@app.route('/login', methods=['POST'])
def handle_form():
    username = request.get_json('username')
    password = request.get_json('password')
    return jsonify({"success": login(username, password)})


# handles the get request for the text
@app.route("/getNotes")
def getNotes():
    return getText()


# get the text from the database
def getText():
    username = session["username"]
    stuff = database["documents"][username]
    return stuff


# login stuff
# dont ask why you can sign in with somone elses
# password it just works

def login(username, password):

    # find the user in the database
    if username in database["users"]:

        if password in database["users"]:
            print("allowed")
            access = "allowed"

            #set the session cookie as the username
            session["username"] = username["username"]
        else:
            print("denied")
            access = "denied"

    else:
        print("denied")
        access = "denied"
    
    return access



# saving text
@app.route("/save", methods=['POST'])
def save():

    # get the text from the user and set it as
    # a variable
    text = request.get_json("text")
    username = session.get("username")

    # write text to the dictionary
    database["documents"][username] = text["text"]

    #write dictionary to disk
    with open("database.json", "w") as file:
        json.dump(database, file, indent=4)
    
    # reload the ditionary from the file
    load()

    return ""


# surely you can figure this one out yourself
app.run(host="0.0.0.0",port=8080)




