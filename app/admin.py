from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required, LoginManager
from forms import AddPostForm
from models import Post, Tag
import datetime
import markdown
import json

@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html',
        title = 'Rafik Rezzik - Admin')

@app.route('/admin/posts')
@login_required
def posts():
    posts = Post.query.all();
    return render_template('posts.html', posts=posts)

@app.route('/admin/posts/add', methods = ['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        current_time = datetime.datetime.now()
        post = Post(title=form.title.data,
                body_markdown=form.body_markdown.data,
                body=markdown.markdown(form.body_markdown.data, extensions = ['codehilite']),
                tagline=" ".join(form.body_markdown.data.split()[:25]) + "..",
                timestamp=current_time,
                user_id=current_user.id)
        post.tags.append(Tag(tag='Sports'))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('add_post.html', form=form)

@app.route('/admin/posts/edit/<postid>', methods = ['GET', 'POST'])
@login_required
def edit_post(postid):
    post = Post.query.filter_by(id=postid).first()
    form = AddPostForm(obj=post)
    if form.validate_on_submit():
        current_time = datetime.datetime.now()
        post.title=form.blog_post_title.data
        post.body_markdown=form.blog_post_markdown.data
        post.body=markdown.markdown(form.blog_post_markdown.data, extensions = ['codehilite'])
        post.tagline=" ".join(form.blog_post_markdown.data.split()[:25]) + ".."
        post.timestamp=current_time
        post.user_id=current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('add_post.html', form=form, post=json.dumps(post.serialize()))

@app.route('/admin/posts/delete/<postid>', methods = ['GET', 'POST'])
@login_required
def delete_post(postid):
    post = Post.query.filter_by(id=postid).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))

