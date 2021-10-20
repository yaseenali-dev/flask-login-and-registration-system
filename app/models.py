from flask import current_app
from .app import db
from .app import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as serializer

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.email == current_app.config['ADMIN_EMAIL']:
            self.is_admin = True

    def __repr__(self):
        return f'id:{self.id} name:{self.name} email: {self.email}'

    @property
    def password(self):
        raise AttributeError('password is not readalble attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        s = serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps( {'confirm_key': self.id} ).decode('utf-8')

    def confrim_token(self, token):
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm_key') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def is_token_valid(token):
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('confirm_key'))
        if user is None:
            return False
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('confirm_key'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
