from app import app
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html',
        title = 'Rafik Rezzik - Admin')

@app.route('/admin/posts')
@login_required
def posts():
    return render_template('posts.html')

@app.route('/admin/posts/delete')
@login_required
def delete_post():
    return render_template('delete_post.html')

