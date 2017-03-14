from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory
from flask.ext.login import current_user, login_required, LoginManager
from forms import AddPostForm
from models import Photo, Post, Tag, FlickrAccount
import datetime
import markdown
import json
from config import ALLOWED_EXTENSIONS
from werkzeug import utils
import flickr_api
import os

@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html',
        title = 'Rafik Rezzik - Admin')

# @app.route('/admin/flickr/verify_flickr')
# @login_required
# def verify_flickr():

#     token = request.args.get('oauth_token')
#     verifier = request.args.get('oauth_verifier')

#     if verifier is not None:
#         auth = flickr_api.auth.AUTH_HANDLER
#         auth.set_verifier(verifier)
#         flickr_api.set_auth_handler(auth)
#         auth.save("flickr_token.token")
#         redirect(url_for('/'))

#     else:
#         FLICKR_PUBLIC = 'b763af2cc441fa6c6c57da66149cf357'
#         FLICKR_SECRET = 'cbd839c4166948fb'
#         flickr_api.set_keys(api_key = FLICKR_PUBLIC, api_secret = FLICKR_SECRET)
#         a = flickr_api.auth.AuthHandler(callback = "http://www.lvh.me/verify_flickr")
#         flickr_api.set_auth_handler(a)

#         perms = "read" # set the required permissions
#         url = a.get_authorization_url(perms)
#         return redirect(url)

@app.route('/admin/flickr/accounts')
@login_required
def flickr_accounts():
    accounts = FlickrAccount.query.all()
    return render_template('flickr/flickr_accounts.html', accounts=accounts)

@app.route('/admin/flickr/verify', methods=["POST", "GET"])
@login_required
def verify_flickr_account():
    if request.method == 'POST':
        print request.form
        the_stuff = flickr_api.auth.AuthHandler.to_dict()
        print the_stuff

        account = FlickrAccount()
        account.authenticated = True
        account.key = the_stuff['api_key']
        account.secret = the_stuff['api_secret']
        account.oauth_token = the_stuff['access_token_key']
        account.oauth_secret = the_stuff['access_token_secret']
        redirect(url_for('flickr_accounts'))
    if request.method == 'GET':
        print request.form
        the_stuff = auth_handler.todict()
        print the_stuff

        account = FlickrAccount()
        account.authenticated = True
        account.key = the_stuff['api_key']
        account.secret = the_stuff['api_secret']
        account.oauth_token = the_stuff['access_token_key']
        account.oauth_secret = the_stuff['access_token_secret']
        redirect(url_for('flickr_accounts'))

@app.route('/admin/flickr/accounts/add', methods=["POST", "GET"])
@login_required
def add_flickr_account():
    if request.method == 'POST':

        print request.form
        flickr_api.set_keys(api_key=request.form.get('api_key'), api_secret=str(request.form.get('api_secret')))
        auth_handler = flickr_api.auth.AuthHandler(request_token_key=session['request_token_key'], request_token_secret=session['request_token_secret'])


        auth_handler.set_verifier(request.form.get('oauth_verifier'))

        the_stuff = auth_handler.todict(include_api_keys=True)
        print the_stuff
        account = FlickrAccount()
        account.authenticated = True
        account.key = the_stuff['api_key']
        account.secret = the_stuff['api_secret']
        account.oauth_token = the_stuff['access_token_key']
        account.oauth_secret = the_stuff['access_token_secret']

        db.session.add(account)
        db.session.commit()
        redirect(url_for('flickr_accounts'))
    else:
        return render_template('flickr/add_flickr_account.html')

@app.route('/admin/flickr/accounts/get_verifier_url', methods=["GET"])
@login_required
def get_verifier_url():
    if request.method == 'GET':
        print "WWWWOOOO!"
        key = request.args.get('api_key')
        secret = request.args.get('api_secret')
        flickr_api.set_keys(api_key=str(key), api_secret=str(secret))
        a = flickr_api.auth.AuthHandler()
        perms = "read"
        url = a.get_authorization_url(perms)
        print url
        the_stuff = a.todict()
        print the_stuff
        session['request_token_key'] = the_stuff['request_token_key']
        session['request_token_secret'] = the_stuff['request_token_secret']

        return jsonify({'url': url})

@app.route('/admin/flickr/albums/load/<id>')
@login_required
def flickr_load_album(id):
    account = FlickrAccount.query.get(1)
    print account
    # Set the api keys
    flickr_api.set_keys(api_key=account.key, api_secret=str(account.secret))
    auth_handler = flickr_api.auth.AuthHandler(access_token_key=account.oauth_token, access_token_secret=str(account.oauth_secret))

    # Set the authentication handler
    flickr_api.set_auth_handler(auth_handler)
    user = flickr_api.test.login()
    photosets = user.getPhotosets(id=id)
    print photosets
    photoset = [i for i in user.getPhotosets() if i.id == id][0]
    photos = photoset.getPhotos()
    print photoset
    for photo in photos:
        print photo
        sizes = photo.getSizes()
        print sizes['Medium 640']['source']
        #print flickr_api.Photo.getInfo(photo=photo)
    redirect(url_for('flickr_accounts'))


@app.route('/admin/flickr/accounts/<id>/albums')
@login_required
def flickr_albums(id):
    account = FlickrAccount.query.get(id)
    print account
    # Set the api keys
    flickr_api.set_keys(api_key=account.key, api_secret=str(account.secret))
    auth_handler = flickr_api.auth.AuthHandler(access_token_key=account.oauth_token, access_token_secret=str(account.oauth_secret))

    # Set the authentication handler
    flickr_api.set_auth_handler(auth_handler)
    user = flickr_api.test.login()
    photosets = user.getPhotosets()
    print photosets
    return render_template('flickr/flickr_albums.html', photosets=photosets)

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

