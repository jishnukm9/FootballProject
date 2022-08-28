


# from mongoengine import connect
# from mongoengine import Document, StringField, URLField,ObjectIdField
from flask_mongoengine import MongoEngine
from APP import app


# Setup Flask-MongoEngine 
# db= MongoEngine(app)
connect(db="football", host="localhost", port=27017)
# client = pymongo.MongoClient("mongodb+srv://jishnukm33:<password>@cluster0.axoi6kh.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# db = client.test

