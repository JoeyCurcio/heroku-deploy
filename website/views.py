from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Note
from . import db

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required #This will then allow us to use the user
def index():
    if request.method == 'POST':
        eventName = request.form.get('ename')
        eventDescription = request.form.get('description')

        new_note = Note(title=eventName, description=eventDescription, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
    return  render_template("event.html", user=current_user)


    