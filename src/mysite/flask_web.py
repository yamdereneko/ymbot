# -*- coding: utf-8 -*-
import flask
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


flask.Flask.run(app)
