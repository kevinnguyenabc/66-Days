from flask import render_template, redirect, url_for, flash, abort, request
from flask66Days import app, db
from flask66Days.forms import RegistrationForm, HabitForm 
from flask66Days.models import User, Habit, CheckIn
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
import sys



@app.route('/')
@login_required
def index():
    return redirect(url_for('habit_list'))

@app.route('/home')
def home():
    return render_template('home.html')

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
        return redirect(request.args.get("next") or url_for("home"))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/your_habits')
@login_required
def habit_list():
    habits = User.query.filter_by(id=current_user.id).first().habits
    habits = [habit for habit in habits if habit.status=="IP"]
    return render_template('habit_list.html', habits=habits, now=datetime.now())


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_habit():
    form = HabitForm() 
    form.submit.label.text = "Create"
    if form.validate_on_submit():
        print(current_user.id)
        habit = Habit(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
        flash('Your habit has been created!', 'success')
        return redirect(url_for('habit_list'))
    return render_template('create_habit.html', form = form, title='Create a New Habit', head='Create Habit Page', method="Begin your journey now!") 
    # This passes the flask form "HabitForm into create_habit.html"


@app.route('/single_habit/<int:habit_id>', methods=['GET', 'POST'])
def single_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    print(habit.status)
    print(habit.checkins[0].cihabit)
    if habit.author != current_user:
        flash("not author")
        return redirect(url_for('habit_list'))
    return render_template('single_habit.html', habit=habit, now=datetime.now())


@app.route('/single_habit/<int:habit_id>/update', methods=['GET', 'POST'])
@login_required
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.author != current_user:
        abort(403)
    form = HabitForm()
    form.submit.label.text = "Update"
    if form.validate_on_submit():
        habit.title = form.title.data
        habit.content = form.content.data
        db.session.commit()
        flash('Your habit has been updated', 'success')
        return redirect(url_for('single_habit', habit_id=habit.id))
    elif request.method == 'GET':
        form.title.data = habit.title
        form.content.data = habit.content
    return render_template('create_habit.html', form = form, title='Update Habit', head='Update Page', id=habit.id)


@app.route('/single_habit/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    checkins = CheckIn.query.filter_by(habit_id=habit_id).all()
    print(checkins)
    print(habit.checkins)
    if habit.author != current_user:
        abort(403)
    for checkin in checkins:
        db.session.delete(checkin)
    db.session.delete(habit)
    db.session.commit()
    flash('Your habit has been deleted', 'success')
    return url_for('habit_list')


@app.route('/your_habits/archived')
@login_required
def archived():
    habits = User.query.filter_by(id=current_user.id).first().habits
    archived_habits = []
    for habit in habits:
        if habit.status == "A":
            archived_habits.append(habit)
    return render_template('habit_list.html', habits=archived_habits, now=datetime.now(), archive=True)


@app.route('/background_process_test/<habit_id>')  
def background_process_test(habit_id):
    print ("Hello", habit_id)
    return {"nothing": "nothing"}


@app.route('/check_in/<int:habit_id>')
def check_in(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    now = datetime.now()
    print("Now", now)
    print("Habit date_created", habit.date_created)
    print("If habit.checkins = 0 or now.date != last_checkin_date, then check in!")
    if (len(habit.checkins) == 0 or (now.date() - habit.date_created.date()).days != habit.checkins[-1].day):
        check_in = CheckIn(day=(now.date()-habit.date_created.date()).days, cihabit=habit)
        db.session.add(check_in)
        db.session.commit()
        # habit = Habit(title=form.title.data, content=form.content.data, user_id=current_user.id)
        print("This check in should work!")
    else: 
        print("check in not available")
    return str(habit_id)
    

@app.route('/profile')
def profile():
    habits = User.query.filter_by(id=current_user.id).first().habits
    completed = 0
    ip_habits = []
    for habit in habits:
        if habit.status == "IP":
            ip_habits.append(habit)
        if len(habit.checkins) >= 66:
            completed += 1
    return render_template('profile.html', habits=ip_habits, user=current_user.username, now=datetime.now(), completed=completed)


@app.route('/testnum15')
def testnum15():
    habit = Habit.query.get(3)
    for i in range(0,67):
        check_in = CheckIn(day=i, cihabit=habit)
        db.session.add(check_in)
    db.session.commit()
    return "success"


@app.route('/single_habit/<int:habit_id>/archive', methods=['POST'])
def archive_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    habit.status = "A"
    db.session.commit()
    return url_for('archived')


@app.route('/single_habit/<int:habit_id>/unarchive', methods=['GET'])
def unarchive_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    habit.status = "IP"
    db.session.commit()
    return redirect(url_for('habit_list'))