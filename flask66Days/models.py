from datetime import datetime
from flask66Days import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader # Decorator for login_manager to know to use this function to get the user
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # UserMixin is a class that contains is_authenticated, is_active... required by flask_login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable= False)
    habits = db.relationship('Habit', backref='author', lazy=True)
    messages = db.relationship('Message', primaryjoin="User.id==Message.toUser", backref="to")
    sent_messages = db.relationship('Message', primaryjoin="User.id==Message.fromUser", backref="from")

    def __repr__(self):
        return f"User('{self.username}')"

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default="IP") 
    checkins = db.relationship('CheckIn', backref='cihabit', lazy=True, order_by="CheckIn.day") # order_by was necessary when updating checkins
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

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromUser = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    toUser = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text)
    messageType = db.Column(db.String(20), default="LR")

    def __repr__(self):
        return f"Message({self.fromUser}, {self.toUser})"