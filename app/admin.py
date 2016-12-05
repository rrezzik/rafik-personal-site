from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory
from flask.ext.login import current_user, login_required, LoginManager
from forms import AddPostForm
from models import Photo, Post, Tag
import datetime
import markdown
import json
from config import ALLOWED_EXTENSIONS
from werkzeug import utils
import os

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
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/admin/photography')
@login_required
def photography():
    photos = Photo.query.all()
    return render_template('photography.html', photos=photos)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/admin/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Get the photo_category
        # Get the photo_album

        # check if the post request has the file part
        print request.files.getlist("file[]")
        # if 'file' not in request.files.getlist("file[]"):
        if len(request.files.getlist("file[]")) == 0:
            print 'no file part'
            flash('No file part')
            return redirect(request.url)
        
        uploaded_files = request.files.getlist("file[]")
        print uploaded_files
        # if user does not select file, browser also
        # submit a empty part without filename
        for file in uploaded_files:
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = utils.secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print "cool redirecting now"

        
        return redirect(url_for('photography'))


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

@app.route('/admin/posts/save', methods = ['POST']) 
@login_required
def save_post():
    form = request.form
    print form

    if 'id' in form:
        print "if"
        # Get the post
        post = Post.query.filter_by(id=form['id']).first()

        current_time = datetime.datetime.now()
        post.title=form['title']
        post.body_markdown=form['body_markdown']
        post.body=markdown.markdown(form['body_markdown'], extensions = ['codehilite'])
        post.tagline=" ".join(markdown.markdown(form['body_markdown']).split()[:25]) + ".."
        post.timestamp=current_time
        post.user_id=current_user.id
        db.session.add(post)
        db.session.commit()
    else:
        print "else"
        post = Post()
        current_time = datetime.datetime.now()
        print "here1"
        post.title=form['title']
        post.body_markdown=form['body_markdown']
        post.body=markdown.markdown(form['body_markdown'], extensions = ['codehilite'])
        post.tagline=" ".join(markdown.markdown(form['body_markdown']).split()[:25]) + ".."
        print "here2"
        post.timestamp=current_time
        post.user_id=current_user.id
        post.published = form['publish'] == 'true'
        print "here3"
        db.session.add(post)
        db.session.commit()

    return jsonify(success = True)
    

@app.route('/admin/posts/delete/<postid>', methods = ['GET', 'POST'])
@login_required
def delete_post(postid):
    post = Post.query.filter_by(id=postid).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))

