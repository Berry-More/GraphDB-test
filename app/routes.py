from app import app
from app.models import ObjectDB
from app.forms import FriendsForm
from flask import jsonify, render_template, redirect, url_for


uri = '#'
user = '#'
password = '#'


@app.route('/users/<username>', methods=['GET'])
def print_data(username):
    db = ObjectDB(uri, user, password)
    user_data = db.find_connect(username)
    db.close()
    return jsonify(user_data)


@app.route('/connect', methods=['GET', 'POST'])
def new_connect():
    form = FriendsForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        second_name = form.second_name.data

        db = ObjectDB(uri, user, password)
        if db.is_user_not_exist(first_name):
            db.create_person(first_name)
        if db.is_user_not_exist(second_name):
            db.create_person(second_name)
        db.create_event(first_name, second_name)
        db.close()

        return redirect(url_for('new_connect'))
    return render_template('connect.html', title='Connect', form=form)


@app.route('/users', methods=['GET', 'POST'])
def users():
    db = ObjectDB(uri, user, password)
    all_users = db.get_all()
    db.close()
    return render_template('users.html', title='Users', all_users=all_users)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Greetings')


@app.route('/about')
def about():
    return render_template('about.html', title='About')
