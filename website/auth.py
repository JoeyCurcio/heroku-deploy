from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.validators import Length, ValidationError
from wtforms import StringField
from .models import User, Note
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required,logout_user, current_user
from . import db

from .models import User



#create a blueprint
bp = Blueprint('auth', __name__)

#This will log the user in correctly
@bp.route('/login', methods=['GET', 'POST'])
def login():
    #This will get the persons email and password
    if request.method == 'POST':
        email = request.form.get('email')
        password_t = request.form.get('pwd')

        #This will then query the db to find the right person
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password_t): #idk wtf this shit is
                flash('Logged ub successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist.', category='error')


    return render_template("login.html", user=current_user)

#This will just check the length of the passed variables
def lengthCheck(form, field):
    if len(field.data) < 2:
        raise ValidationError('Feild must be greater then 7')


# this is the hint for a logout function
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# this is the hint for a signup function
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('name')
        middleName = request.form.get('middlename')
        lastName = request.form.get('lastname')
        dob = request.form.get('dob')
        pNumber = request.form.get('pnumber')
        adress = request.form.get('adress')
        password1 = request.form.get('pwd')
        password2 = request.form.get('pwdrepeat')

        #These are the validation checks
        pWordLengthCheck = StringField(password1, [lengthCheck])
        fNameLengthCheck = StringField(firstName, [lengthCheck])
        eailLengthCheck = StringField(email, [lengthCheck])
        pwdHash = generate_password_hash(password1)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exsits', category='error')
        elif not eailLengthCheck:
            flash('email must be greater then 4 characters', category='error')
        elif not  fNameLengthCheck:
            flash('First name must be greater then 2 characters')
        elif password1 != password2:
            flash('Password must match', category='error')
        elif not  pWordLengthCheck :
            flash('Password must be greater then 7 characters', category='error')
        else:
            new_user = User(email = email, name=firstName,middle_name = middleName, last_name = lastName, password=pwdHash, dob=dob, pnumber=pNumber, address = adress)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
            


    return render_template("sign_up.html", user=current_user)

#This is for the event page
@bp.route('/event', methods=['GET', 'POST'])
def event():
    return render_template("event.html", user=current_user)

#This is for the create event page
@bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    return render_template("create_event.html", user=current_user)