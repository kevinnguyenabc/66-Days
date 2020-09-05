from flask import render_template, redirect, url_for, flash, abort, request, jsonify
from flask66Days import app, db, bcrypt
from flask66Days.forms import RegistrationForm, HabitForm, LoginForm, UpdateAccountForm
from flask66Days.models import User, Habit, CheckIn, Link, Message
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
from pytz import timezone
import sys, json, requests



@app.route('/')
@login_required
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(request.args.get("next") or url_for("home"))
        else: 
            flash("Login was unsuccessful. Please check your email and password and try again.", "delete-message")
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
    return render_template('habit_list.html', habits=habits, now=datetime.now(timezone('US/Pacific')))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_habit():
    form = HabitForm() 
    form.submit.label.text = "Create"
    if form.validate_on_submit():
        habit = Habit(title=form.title.data, content=form.content.data, user_id=current_user.id, date_created=datetime.now(timezone('US/Pacific')))
        db.session.add(habit)
        db.session.commit()
        flash('Your habit has been created!', 'success')
        return redirect(url_for('habit_list'))
    # This passes the flask form "HabitForm" into create_habit.html
    return render_template('create_habit.html', form = form, title='Create a New Habit', head='Create Habit Page', description="Begin your journey now!") 


@app.route('/single_habit/<int:habit_id>/<habit_title>', methods=['GET', 'POST'])
def single_habit(habit_id, habit_title):
    habit = Habit.query.get_or_404(habit_id)
    if habit.author != current_user:
        abort(403)
    linked_habits = []
    print(habit.checkins)
    print(habit.checkins[-1].day+1)
    for link in habit.links:
        linked_habits.append(Habit.query.get(link.habit1) if link.habit2 == habit.id else Habit.query.get(link.habit2))
    return render_template('single_habit.html', habit=habit, now=datetime.now(timezone('US/Pacific')), linked_habits=linked_habits)


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
        return redirect(url_for('single_habit', habit_id=habit.id, habit_title=habit.title))
    elif request.method == 'GET':
        form.title.data = habit.title
        form.content.data = habit.content
    return render_template('create_habit.html', form = form, title='Update Habit', head='Update Page', id=habit.id, habit_title=habit.title)


@app.route('/single_habit/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    checkins = CheckIn.query.filter_by(habit_id=habit_id).all()
    if habit.author != current_user:
        abort(403)
    for checkin in checkins:
        db.session.delete(checkin)
    db.session.delete(habit)
    db.session.commit()
    flash('Your habit has been deleted.', 'success')
    return url_for('habit_list')


@app.route('/your_habits/archived')
@login_required
def archived():
    habits = User.query.filter_by(id=current_user.id).first().habits
    archived_habits = []
    for habit in habits:
        if habit.status == "A":
            archived_habits.append(habit)
    return render_template('habit_list.html', habits=archived_habits, now=datetime.now(timezone('US/Pacific')), archive=True)


@app.route('/check_in/<int:habit_id>')
def check_in(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.author != current_user:
        abort(403)
    now = datetime.now(timezone('US/Pacific'))
    if (len(habit.checkins) == 0 or (now.date() - habit.date_created.date()).days != habit.checkins[-1].day):
        check_in = CheckIn(day=(now.date()-habit.date_created.date()).days, cihabit=habit)
        db.session.add(check_in)
        db.session.commit()
    else: 
        abort(403)
    return str(habit_id)
    

@app.route('/profile')
def profile():
    print(datetime.now(timezone('US/Pacific')))
    print(datetime.now())
    habits = User.query.filter_by(id=current_user.id).first().habits
    now = datetime.now(timezone('US/Pacific'))
    messages = current_user.messages
    inbox = []
    for message in messages:
        if message.toUser == current_user.id:
            inbox.append(message)
    completed = 0
    ip_habits = []
    times_checked_in = 0
    total = 0
    for habit in habits:
        if habit.status == "IP":
            ip_habits.append(habit)
            x = (now.date() - habit.date_created.date()).days
            if x-10 < 0:
                total += 1+x
                times_checked_in += len(habit.checkins)
            else:
                total += 10
                times_checked_in += len([i for i in habit.checkins if i.day > x-10])
        if len(habit.checkins) >= 66:
            completed += 1
    return render_template('profile.html', habits=ip_habits, now=now, completed=completed, inbox=inbox, rate=int(times_checked_in/total*100))


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


@app.route('/link_request', methods=['POST'])
def link_request():
    if request.method == "POST":
        to = User.query.filter_by(username=request.json['username']).first()
        if to and current_user.id != to.id:
            message = Message(fromUser=current_user.id, toUser=to.id, messageType="LR:"+str(request.json['id']), 
                            content=current_user.username +" would like to link their habit, " + Habit.query.get(request.json['id']).title + ".")
            db.session.add(message)
            db.session.commit()
            return json.dumps({"status": "success", "username": to.username})
        else: 
            return json.dumps({"status": "fail", "username": request.json["username"]})


@app.route('/link_habits', methods=['POST'])
def link_habits():
    habit1 = Habit.query.get(request.json["habit1"])
    habit2 = Habit.query.get(request.json["habit2"])
    # Iterate over the shorter of the two lists
    if (len(habit1.links) < len(habit2.links)):
        links = habit1.links
    else: 
        links = habit2.links
    for link in links:
        if ((link.habit1==habit1.id and link.habit2==habit2.id) or (link.habit1==habit2.id and link.habit2==habit1.id)):
            flash("This link already exists, select another habit.", "delete-message")
            return ""

    link = Link(habit1=habit1.id, habit2=habit2.id)
    db.session.add(link)
    db.session.delete(Message.query.get(request.json["messageId"]))
    db.session.commit()

    flash("You have linked your habit, " + habit2.title + ", with " + habit1.author.username + "'s habit, " + habit1.title + "!")
    return ""


@app.route('/link_habits/reject/<message_id>', methods=['POST'])
def reject_link(message_id):
    db.session.delete(Message.query.get(message_id))
    db.session.commit()
    return ""


@app.route('/profile/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm() 
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form = form)


@app.route('/calendar/<int:habit_id>')
def calendar(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return render_template('calendar.html', habit=habit)


@app.route('/update_checkins', methods=['POST'])
def update_checkins():
    habit = Habit.query.get(request.json["id"])
    checkIns = request.json["checkIns"]
    newCheckIns = request.json["newCheckIns"]
    addList = set(newCheckIns) - set(checkIns)
    removeList = set(checkIns) - set(newCheckIns)
    removeCheckIns = CheckIn.query.filter(CheckIn.habit_id==request.json["id"], CheckIn.day.in_(removeList)).all()
    for checkIn in removeCheckIns:
        db.session.delete(checkIn)
    for day in addList:
        checkIn = CheckIn(day=day, cihabit=habit)
        db.session.add(checkIn)
    db.session.commit()
    return url_for('single_habit', habit_id=habit.id, habit_title=habit.title)


@app.route('/blah')
def blah():
    response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Clone10?api_key=RGAPI-2e4f5f42-6350-46e5-af5b-51c0cc6a73d5")
    return (response.json())