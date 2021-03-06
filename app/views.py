from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from forms import LoginForm
from models import User, Post, FlickrAccount, Account, PhotoAlbum
import glob
import json

import traceback

import flickr_api

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
    posts = Post.query.order_by(Post.timestamp.desc())
    photo_urls = []
    try:
        albums = PhotoAlbum.query.order_by(PhotoAlbum.id)
    except Exception as e:
        traceback.print_exc()
        print str(e)

    return render_template('home.html', albums=albums, posts=posts, photo_urls=json.dumps(photo_urls))


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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/running')
def running():
    return render_template('running.html')

@app.route('/photography/album/<id>')
def photo_album(id):
    try:
        album = PhotoAlbum.query.get(id)
    except Exception as e:
        traceback.print_exc()
        print str(e)
    return render_template('album.html', album=album)
