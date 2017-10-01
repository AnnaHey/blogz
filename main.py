from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogs@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_body = db.Column(db.String(2400))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, blog_body, owner):
        self.blog_title = blog_title
        self.blog_body = blog_body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blogs']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')



@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:
            flash("Username does not exist", "error")
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect ('/')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error =''
        password_error = ''
        verify_error = ''

        
        if len(username) < 3 or len(username) > 20:
            username_error = "Not a valid username" 
            username = ''

        if password != verify:
            password_error = "Not a match" 
            password = ''
        else:
            password = password
    
        if verify != password:
            verify_error = "Not a match, please re-enter password and verification"
            password = ''
            verify = ''
        else:
            password = password
            verify = verify

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')

        else:
            # will return message that user already exists
            pass

    return render_template('signup.html')




# blogs = []

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="Blogz", users=users)

@app.route('/blog')
def blog_list():
    if request.args.get("id"):
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)

        return render_template('singleblog.html', blog=blog)

    elif request.args.get("user"):
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', blogs=blogs)

    else:
        blogs = Blog.query.all()
        return render_template('blogs.html', title="Blogz", blogs=blogs)

@app.route("/newblog", methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body'] 
        blogs.append(blog_title)
        blogs.append(blog_body)


    return render_template('blogs.html', title="Blogs!", blogs=blogs)

if __name__ == '__main__':
    app.run()

