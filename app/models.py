from app import db
import json

tags_relationship_table=db.Table('relationship_table',

                             db.Column('post_id', db.Integer,db.ForeignKey('post.id'), nullable=False),
                             db.Column('tags_id',db.Integer,db.ForeignKey('tag.id'),nullable=False),
                             db.PrimaryKeyConstraint('post_id', 'tags_id') )

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(128), index = True)
    fullname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password,
            'fullname' : self.fullname,
            'email' : self.email
        }

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    tagline = db.Column(db.Text)
    body_markdown = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    published = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags=db.relationship('Tag', secondary=tags_relationship_table, backref='posts' )

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'body' : self.body,
            'tagline' : self.tagline,
            'published' : self.published,
            'body_markdown' : self.body_markdown
        }

    def __repr__(self):
        return '<Post %r>' % (self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.Text)



# Image gallery model

class PhotoCategory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, unique = True)
    slug = db.Column(db.Text)

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'slug' : self.slug,
        }

    def __repr__(self):
        return '<PhotoCategory %r>' % (self.name)


class PhotoAlbum(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('photocategory.id'))
    name = db.Column(db.Text, unique = True)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
        }

    def __repr__(self):
        return '<PhotoAlbum %r>' % (self.name)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    album_id = db.Column(db.Integer, db.ForeignKey('photoalbum.id'))
    thumbnail_path = db.Column(db.Text)
    path = db.Column(db.Text)

    def serialize(self):
            return {
                'id' : self.id,
                'name' : self.name,
                'thumbnail_path' : self.thumbnail_path,
                'path' : self.path
            }

    def __repr__(self):
            return '<Photo %r>' % (self.name)





