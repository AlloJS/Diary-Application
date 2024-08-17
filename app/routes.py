from flask import Blueprint,request, render_template, redirect, url_for, flash
import diary.diary.diary_DB
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard',methods=['POST'])
def dashboard():
    if request.method == 'POST':
        try:
            id_diary = request.form.get('id_diary')
            d = diary.diary.diary_DB .DiarySQL('default','localhost','Diary','root','root')
            d.start_diary(id_diary)
            d.orderby_startdata('crescente')
            list_events = d.diary
            return render_template('dashboard.html',list_events=list_events)
        except ValueError as e:
            err = e
            return render_template('index.html',err=err)



