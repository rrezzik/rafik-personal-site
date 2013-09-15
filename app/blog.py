from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from forms import LoginForm
from models import User, Post


@app.route('/blog')
def blog_index():
    posts = Post.query.all()
    return render_template('blog_index.html', posts=posts)
