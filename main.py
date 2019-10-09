from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogs@localhost:3307/blogz'
db = SQLAlchemy(app)
app.secret_key = "'G@K^=u39vSW)SE("


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    post = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allow_routes = ['login', 'signup', 'post', 'index']
    if request.endpoint not in allow_routes and 'username' not in session:
        return redirect('/login')


@app.route('/blog', methods=['GET'])
def post():
    post_id = request.args.get('id')
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if post_id:
        post_query = Blog.query.get(post_id)
        return render_template('post.html', post=post_query)
    if username:
        user_post_query = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', blog=user_post_query)
    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blog=blogs)


@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username_errors = check_username(username)
        password_errors = check_password(password, username)
        if not username_errors and not password_errors:
            session['username'] = username
            return redirect('/blog?username=' + session['username'])

        return render_template('login.html', username=username, username_errors=username_errors, password=password,
                               password_errors=password_errors)

    return render_template('login.html')

def check_username(username):
    if not User.query.filter_by(username=username).first():
        return 'No username exists'
    return ''

def check_password(password, username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_password = user.password
        if user_password != password:
            return 'Password is incorrect'
    return ''

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_errors = validate_username(username)
        password_errors = validate_password(password, verify)
        verify_errors = validate_verify(verify)
        if not username_errors and not password_errors and not verify_errors:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')

        return render_template('signup.html', username=username, username_errors=username_errors, password=password,
                               password_errors=password_errors, verify=verify, verify_errors=verify_errors)

    return render_template('signup.html')


def validate_username(username):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        existing_user = existing_user.username
    if not username:
        return 'Please enter a username'
    if len(username) < 3 or len(username) > 40:
        return 'Invalid username length'
    if ' ' in username:
        return 'Invalid username please remove spaces'
    if username == existing_user:
        return "Username is already taken"
    return ''


def validate_password(password, verify):
    if not password:
        return 'Please enter a password'
    if len(password) < 3 or len(password) > 40:
        return 'Invalid password length'
    if ' ' in password:
        return 'Invalid password please remove spaces'
    if password != verify:
        return 'Password and verification do not match'
    return ''


def validate_verify(verify):
    if not verify:
        return 'Please enter a verification password'
    return ''


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blogBody']
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, blog_body, owner)
        db.session.add(new_blog)
        db.session.commit()
        post_id = new_blog.id
        return redirect('/blog?id=' + str(post_id))

    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
