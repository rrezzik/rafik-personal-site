from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from forms import LoginForm
from models import User, Post
import glob
from random import randrange

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = Post.query.all()
    return render_template('blog_index.html',
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print "Form submitted and everyting was good?"
        if form.get_user():
            login_user(form.get_user())
            return redirect(url_for('admin'))
    return render_template('login.html',
        title = 'Sign In',
        form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/code')
def code():
    return render_template('code.html')

@app.route('/photography')
def photography():
    '''
    Get all the pictures from the directoty and send the list
    to the template for beautiful masonry gallery
    '''

    picture_files = glob.glob('app/static/photography/photos/*')
    pics = []
    heights = [292, 140]
    widths = [140, 292, 444]
    for pic_file in picture_files:
        pics.append({'filename': pic_file.replace('app/', ''),
            'height': heights[randrange(2)],
            'width': widths[randrange(3)]})
    return render_template('photography.html', pics=pics)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/running')
def running():
    return render_template('running.html')
