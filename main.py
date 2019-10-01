from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogs@localhost:8889/blogs'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



@app.route('/')
def hello_world():
    return 'Hello World!'

class Blog():
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    datetime = db.Column(db.Datetime)

    def __init__(self, title, body, datetime):
        self.title = title
        self.body = body
        self.datetime = datetime


if __name__ == '__main__':
    app.run()



