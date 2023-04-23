from flask import Flask, app, redirect, session, request, jsonify, Response, url_for, abort, Blueprint,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path ='/static/')
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

