from flask_wtf import Form
from wtforms import TextAreaField, TextField, PasswordField, validators
from werkzeug.security import check_password_hash
from models import User
from app import db


class LoginForm(Form):
    login = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def validate_login(self, field):
        user = self.get_user()
        print user
        if user is None:
            raise validators.ValidationError('Invalid user')

        if not(check_password_hash(user.password, self.password.data)):
            print "oh no!"
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).first()

class AddPostForm(Form):
    blog_post_title = TextField('Post Title', [validators.Required()])
    blog_post_markdown = TextAreaField('Post Content', [validators.Required()])
