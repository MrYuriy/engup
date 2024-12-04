from flask import Blueprint, json, render_template, redirect, url_for, request
from app.forms import LoginForm
from utils.create_moc_translation import create_mock_translation


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/exercises')
def exercises():
    return render_template('exercises.html')

@main.route('/dictionary')
def dictionary():
    return render_template('dictionary.html')

@main.route('/settings')
def settings():
    return render_template('settings.html')

@main.route('/user_dictionary')
def user_dictionary():
    return render_template('user_dictionary.html')

@main.route('/general_dictionary')
def general_dictionary():
    return render_template('general_dictionary.html')

@main.route('/create-data')
def create_translation():
    create_mock_translation()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
