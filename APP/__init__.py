

from flask import Flask,Blueprint
from flask_pymongo import PyMongo
import urllib


app=Flask(__name__,template_folder='./templates',static_folder="./static")


from APP.BookManager.views import BookManager
from APP.UserManager.views import UserManager




app.register_blueprint(BookManager)
app.register_blueprint(UserManager)