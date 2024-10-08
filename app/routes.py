from flask import Blueprint,request, render_template, redirect, url_for, flash
import diary.diary.diary_DB
import diary.diary.daily
import diary.diary.monthly
import diary.diary.period
import diary.diary.new_diary
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard',methods=['GET'])
def dashboard():
    if request.method == 'GET':
        try:
            with diary.diary.diary_DB.create_connection('localhost', 'Diary', 'root', 'root') as connection:
                message = ''
                id_diary = request.args.get('id_diary')
                name_new_diary = request.args.get('name_new_diary')
                list_id = diary.diary.diary_DB.read_is_diary_exist(connection)
                list_events = []
                name_event = ''

                if id_diary in list_id:
                    list_events = get_list_events(connection,id_diary)
                    name_event = request.args.get('search-event')
                    if name_event is not None:
                        list_events = [diz for diz in list_events if name_event in diz['name']]
                        if len(list_events) == 0:
                            message = "Nessun evento trovato."


                    return render_template('dashboard.html',list_events=list_events,id_diary=id_diary,name_event=name_event,message=message)
                else:
                    raise ValueError('Il diario non esiste')
        except ValueError as err:
            print(err)
            return render_template('index.html',err=err,)


@bp.route('/aggiungiEvento', methods=['GET'])
def aggiungi_evento():
    id_diary = request.args.get('id_diary')
    return render_template('aggiungiEvento.html',id_diary=id_diary)


@bp.route('/writeDB', methods=['GET'])
def write_DB():
    with diary.diary.diary_DB.create_connection('localhost', 'Diary', 'root', 'root') as connection:
        id_diary = request.args.get('id_diary')
        existing_or_new_diary = diary.diary.diary_DB.start_diary(connection, id_diary=id_diary)
        name = request.args.get('name')
        type_event = request.args.get('type-event')
        description = request.args.get('description')
        date_start = request.args.get('date_start')
        date_and = request.args.get('date_and')
        hour_start = request.args.get('hour_start')
        minute_start = request.args.get('minute_start')
        hour_and = request.args.get('hour_and')
        minute_and = request.args.get('minute_and')
        month_to_month = request.args.get('choose-month')
        year_to_month = request.args.get('year')
        # Formatted date to write events
        if(type_event != '2'):
            data_start_split = date_start.split('-')
            data_and_split = date_and.split('-')
            year_start = data_start_split[0]
            mounth_start = data_start_split[1]
            day_start = data_start_split[2]
            year_and = data_and_split[0]
            mounth_and = data_and_split[1]
            day_and = data_and_split[2]
        if type_event == '1':
            duration_hour = int(hour_and) - int(hour_start) * 60
            duration_minut = int(minute_and) - int(minute_start)
            duration = duration_hour + duration_minut
            event_daily = diary.diary.daily.daily_note(name=name,description=description,year=int(year_start),month=int(mounth_start),day=int(day_start),hour=int(hour_start),minute=int(minute_start),minut_duration=int(duration),do=False,id_diary=id_diary)
            diary.diary.diary_DB.write_events_DB(connection,event_daily)
        elif type_event == '2':
            event_monthly = diary.diary.monthly.monthly_note(name=name,description=description,year=int(year_to_month),month=int(month_to_month),do=False,id_diary=id_diary)
            diary.diary.diary_DB.write_events_DB(connection,event_monthly)
        elif type_event == '3':
            period_event_start = diary.diary.period.get_period_to(year=int(year_start),month=int(mounth_start),day=int(day_start),hour=int(hour_start),minute=int(minute_start))
            period_event_and = diary.diary.period.get_period_from(year=int(year_and),month=int(mounth_and),day=int(day_and),hour=int(hour_and),minute=int(minute_and))
            period_event = diary.diary.period.period_note(name=name,description=description,period_from=period_event_start,period_to=period_event_and,do=False,id_diary=id_diary)
            diary.diary.diary_DB.write_events_DB(connection,period_event)

    return render_template('aggiungiEvento.html', id_diary=id_diary)


@bp.route('/delete_event', methods=['GET'])
def delete_event():
    try:
        with diary.diary.diary_DB.create_connection('localhost', 'Diary', 'root', 'root') as connection:
            id_diary = request.args.get('id_diary')
            univoc_id = request.args.get('univoc_id')
            diary.diary.diary_DB.delete_event_DB(connection,id_diary,univoc_id)
            list_events = get_list_events(connection,id_diary)
            return render_template('dashboard.html', list_events=list_events, id_diary=id_diary)
    except:
        message = 'Errore Cancellazione'


@bp.route('/modify_event', methods=['GET'])
def modify_event():
    try:
        with diary.diary.diary_DB.create_connection('localhost', 'Diary', 'root', 'root') as connection:
            id_diary = request.args.get('id_diary')
            univoc_id = request.args.get('univoc_id')
            list_events = get_list_events(connection,id_diary)
            return render_template('dashboard.html', list_events=list_events, id_diary=id_diary)
    except:
        message = 'Errore Cancellazione'


def get_list_events(connection,id_diary):
    diary.diary.diary_DB.start_diary(connection, id_diary=id_diary)
    list_events = diary.diary.diary_DB.read_events_DB(connection, id_diary=id_diary)
    list_events = diary.diary.new_diary.orderby_startdata(list_events, 'decrescente')
    return list_events





