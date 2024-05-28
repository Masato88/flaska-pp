from flaskblog import app
from flask import render_template,request,redirect,url_for
from flaskblog import db
from flask_login import login_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash

@db.login_manager.user_loader
def load_user(user_id):
   return db.User.query.get(int(user_id))


@app.route('/')
def home():
    if request.method == 'GET':
       return render_template(
            'home.html'
            )


@app.route('/top', methods=['GET', 'POST'])
@login_required
def top():
    if request.method == 'GET':
       posts = db.Post.query.all()
       return render_template(
            'top.html',
            posts=posts
            )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.User(username=username, password=generate_password_hash(password, method='sha256'))
        db.database.session.add(user)
        db.database.session.commit()
        
        return redirect(url_for('login'))
    else:
     return render_template(
        'signup.html'
    )
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
        user=db.User.query.filter_by(username=username).first()
        if check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('top'))
        else:
            return redirect(url_for('login'))
    else:
     return render_template(
        'login.html'
    )

@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('home'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title=request.form.get('title')
        body=request.form.get('body')
        
        post=db.Post(title=title, body=body)
        db.database.session.add(post)
        db.database.session.commit()
        
        return redirect(url_for('top'))

    else:
     return render_template(
        'create.html'
    )


@app.route('/<int:id>/update', methods=['GET','POST'])
@login_required
def update(id):
    post = db.Post.query.get(id)
    if request.method == 'GET':
        return render_template(
        'update.html',
        post=post
    )
        
    else:
        post.title=request.form.get('title')
        post.body=request.form.get('body')

        db.database.session.commit()                 
        return redirect(url_for('top'))


@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    post = db.Post.query.get(id)

    db.database.session.delete(post)
    db.database.session.commit()
    return redirect(url_for('top'))

