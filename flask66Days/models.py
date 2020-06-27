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

    def __repr__(self):
        return f"User('{self.username}')"

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Habit('{self.title}', '{self.date_created}')"

class CheckIns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)

    def __repr__(self):
        return f"CheckIns(Habit '{self.habit_id}', '{self.day}')"
