import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def app_obj():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    db.init_app(app)

    try:
        db.create_all()
    except Exception as exception:
        print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
    finally:
        print("db.create_all() in __init__.py was successfull - no exceptions were raised")

    return app
