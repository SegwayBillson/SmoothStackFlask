from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flasky import db, login_manager, app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''
User class to store user information in database.
Contains user id, username, email, profile picture, password (hashed), and posts
'''
class User(db.Model, UserMixin):
    # Set up database columns
    id = db.Column(db.Integer, primary_key=True)                                    # Unique ID's, primary keys
    username = db.Column(db.String(20), unique=True, nullable=False)                # Unique Usernames of max length 20
    email = db.Column(db.String(50), unique=True, nullable=False)                   # Unique Emails of max length 50
    image = db.Column(db.String(20), nullable=False, default='default.png')         # User Profile Pictures
    password = db.Column(db.String(60), nullable=False)                             # Unique Usernames of max length 20
    posts = db.relationship('Post', backref='author', lazy=True)                    # Posts made by user
    admin = db.Column(db.Boolean, default=False)                                    # Boolean for admin status

    def get_reset_token(self, expires_secs=900):
        s = Serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username},{self.email},{self.image}')"

'''
Post class to store post information in database.
Contains post id, title, date posted, content, and user ID
'''
class Post(db.Model):
    # Set up database columns
    id = db.Column(db.Integer, primary_key=True)                                # Unique ID's, primary keys
    title = db.Column(db.String(100), nullable=False)                           # Post title
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)      # Date posted
    content = db.Column(db.Text, nullable=False)                                # Body of post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # Foreign key of user id of author
    announce = db.Column(db.Boolean, default=False)                             # Boolean for announcement status

    def __repr__(self):
        return f"Post('{self.title},{self.date}')"