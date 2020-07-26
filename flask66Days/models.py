from datetime import datetime
from flask66Days import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader # Decorator for login_manager to know to use this function to get the user
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    habits = db.relationship('Habit', backref='author', lazy=True)
    #messages = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default="IP")
    checkins = db.relationship('CheckIn', backref='cihabit', lazy=True)
    links = db.relationship('Link', primaryjoin="or_(Habit.id==Link.habit1, Habit.id==Link.habit2)")

    def __repr__(self):
        return f"Habit('{self.title}', '{self.date_created}')"

class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)

    def __repr__(self):
        return f"CheckIn(Habit '{self.habit_id}', '{self.day}')"

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit1 = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    habit2 = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)

    def __repr__(self):
        return f"Link('{self.habit1}', '{self.habit2}')"