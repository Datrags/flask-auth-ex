from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__ = 'users' 
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    feedback = db.relationship("Feedback", backref="user")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Registers user with hashed password"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username, 
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.checkpw(password.encode('utf-8'), u.password.encode('utf-8')):
            # return user instance
            return u
        else:
            return False
        
class Feedback(db.Model):
    """Feedback model"""

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text,nullable=False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable=False)
   