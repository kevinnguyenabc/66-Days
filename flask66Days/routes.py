from flask import render_template, redirect, url_for, flash, abort, request
from flask66Days import app, db
from flask66Days.forms import RegistrationForm, HabitForm 
from flask66Days.models import User, Habit
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
import sys



x = {"author": "Me", "hello": "asdf"}

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', x = x)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
        else:
            user = User(username=form.username.data)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/your_habits')
@login_required
def habit_list():
    habits = Habit.query.all()
    habits_list = User.query.filter_by(id=current_user.id).first()
    print(habits_list.habits, file=sys.stderr)
    return render_template('habit_list.html', habits=habits)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_habit():
    form = HabitForm() 
    if form.validate_on_submit():
        print(current_user.id)
        habit = Habit(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(habit)
        db.session.commit()
        flash('Your habit has been created!', 'success')
        return redirect(url_for('habit_list'))
    return render_template('create_habit.html', form = form, title='Create a New Habit', head='Create Habit Page') 
    # This passes the flask form "HabitForm into create_habit.html"


@app.route('/single_habit/<int:habit_id>', methods=['GET', 'POST'])
def single_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return render_template('single_habit.html', habit=habit)


@app.route('/single_habit/<int:habit_id>/update', methods=['GET', 'POST'])
@login_required
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.author != current_user:
        abort(403)
    form = HabitForm()
    if form.validate_on_submit():
        habit.title = form.title.data
        habit.content = form.content.data
        db.session.commit()
        flash('Your habit has been updated', 'success')
        return redirect(url_for('single_habit', habit_id=habit.id))
    elif request.method == 'GET':
        form.title.data = habit.title
        form.content.data = habit.content
    return render_template('create_habit.html', form = form, title='Update Habit', head='Update Page')


@app.route('/single_habit/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.author != current_user:
        abort(403)
    db.session.delete(habit)
    db.session.commit()
    flash('Your habit has been deleted', 'success')
    return redirect(url_for('home'))

@app.route('/your_habits/<int:habit_id>')
def check_in(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    print(habit.content)
    print(habit_id, file=sys.stderr)
    print(habit.date_created, file=sys.stderr)
    print(datetime.utcnow(), file=sys.stderr)
    print("Dattimenow", datetime.now())
    print((datetime.utcnow()-habit.date_created).days)
    now = datetime.utcnow()
    if (now > habit.date_created and now.day != habit.date_created.day):
        print("This check in should work!", file=sys.stderr)
    return redirect(url_for('home'))


@app.route('/interactive', methods=['GET', 'POST'])
def interactive():
    print("hello", file=sys.stderr)
    form = RegistrationForm()
    if form.validate_on_submit():
        print("hello", file=sys.stderr)
    return render_template('interactive.html')