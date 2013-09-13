from flask.ext.wtf import Form, TextField, PasswordField, validators
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

        if user.password != self.password.data:
            print "oh no!"
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).first()
