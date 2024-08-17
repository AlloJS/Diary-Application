from flask import Blueprint,request, render_template, redirect, url_for, flash
import diary.diary.diary_DB
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard',methods=['GET'])
def dashboard():
    if request.method == 'GET':
        try:
            message = ""
            id_diary = request.args.get('id_diary')
            d = diary.diary.diary_DB .DiarySQL(host='localhost',database='Diary',user='root',password='root')
            d.start_diary(id_diary)
            d.orderby_startdata('crescente')
            # Diario esistente 65592250285068942839
            d.set_name(id_diary)
            name_diary = d.name
            list_events = d.diary
            name_event = request.args.get('search-event')
            print("name_event ->")
            print(name_event)
            if name_event is not None:
                list_events = [diz for diz in list_events if name_event in diz['name']]
                if len(list_events) == 0:
                    message = "Nessun evento trovato."

            return render_template('dashboard.html',id_diary=id_diary,name_diary=name_diary,list_events=list_events,message=message)
        except  ValueError as e:
            err = e
            return render_template('index.html',err=err)

@bp.route('/aggiungiEvento', methods=['GET'])
def aggiungi_evento():
    id_diary = request.args.get('id_diary')
    return render_template('aggiungiEvento.html',id_diary=id_diary)




