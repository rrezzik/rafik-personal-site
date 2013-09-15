from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required
from forms import AddPostForm
from models import Post
import datetime
import markdown2

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html',
        title = 'Rafik Rezzik - Admin')

@app.route('/admin/posts')
@login_required
def posts():
    return render_template('posts.html')

@app.route('/admin/posts/add', methods = ['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        current_time = datetime.datetime.now()
        post = Post(title=form.title.data,
                body_markdown=form.content.data,
                body=markdown2.markdown(form.content.data),
                timestamp=current_time,
                user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        redirect(url_for('posts'))
    return render_template('add_post.html', form=form)

@app.route('/admin/posts/delete')
@login_required
def delete_post():
    return render_template('delete_post.html')

