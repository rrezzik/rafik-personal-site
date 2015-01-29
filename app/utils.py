from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required
from forms import AddPostForm
from models import Post, User
import datetime
import markdown2
from werkzeug.security import generate_password_hash


def create_user(in_username, in_password, in_fullname, in_email):
    user = User(username = in_username,
            password = generate_password_hash(in_password),
            fullname = in_fullname,
            email = in_email);

    db.session.add(user)
    db.session.commit()
