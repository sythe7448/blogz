from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogs@localhost:3307/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET'])
def blog():
    post_id = request.args.get('id')

    if post_id:
        post = Blogs.query.get(post_id)
        return render_template('post.html', post=post)
    else:
        blogs = Blogs.query.all()

        return render_template('blog.html', blogs=blogs)


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blogBody']
        new_blog = Blogs(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        post_id = new_blog.id
        return redirect('/blog?id=' + str(post_id))

    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
