from flask import Blueprint, request, render_template, session, redirect, url_for
from bson import ObjectId
from datetime import datetime
import calendar
from repositories.mongo_repository import find_recent_events, insert_event, find_all_events, delete_event, update_event

events_bp = Blueprint('events', __name__)

def generate_dates(year, month, weekday):
    cal = calendar.monthcalendar(year, month)
    dates = []
    for week in cal:
        if week[weekday] != 0:
            dates.append(datetime(year, month, week[weekday]))
    return dates

@events_bp.route('/events')
def show_events():
    events = find_recent_events(30)
    return render_template('events.html', events=events)

@events_bp.route('/events/register', methods=['GET', 'POST'])
def events_register():
    if request.method == 'POST':
        session['location'] = request.form.get('location', '◯◯体育館')
        session['description'] = request.form.get('description', '説明を入力')
        session['selected_year'] = int(request.form.get('selected_year', datetime.now().year))
        session['selected_month'] = int(request.form.get('selected_month', (datetime.now().month % 12) + 1))
        session['selected_dayofweek'] = int(request.form.get('dayOfWeek', 6))
        session['start_hour'] = int(request.form['start_hour'])
        session['start_minute'] = int(request.form['start_minute'])
        session['end_hour'] = int(request.form['end_hour'])
        session['end_minute'] = int(request.form['end_minute'])

        selected_dates = request.form.getlist('selected_dates')

        if 'apply_button' in request.form:
            for date_str in selected_dates:
                location = session.get('location', '◯◯体育館')
                description = session.get('description', '説明を入力')
                start_hour = session.get('start_hour', 0)
                start_minute = session.get('start_minute', 0)
                end_hour = session.get('end_hour', 0)
                end_minute = session.get('end_minute', 0)

                start_time = datetime.strptime(f"{date_str} {start_hour}:{start_minute}", "%Y-%m-%d %H:%M")
                end_time = datetime.strptime(f"{date_str} {end_hour}:{end_minute}", "%Y-%m-%d %H:%M")

                event_document = {
                    "startTime": start_time,
                    "endTime": end_time,
                    "place": location,
                    "description": description,
                    "entryOptions": [
                        {"id": "1", "text": "参加"},
                        {"id": "2", "text": "途中参加"},
                        {"id": "3", "text": "不参加"}
                    ]
                }
                insert_event(event_document)
            session['selected_dayofweek'] = 6
            session['dates'] = [date.strftime('%Y-%m-%d') for date in generate_dates(session['selected_year'], session['selected_month'], 6)]
            return redirect(url_for('events.events_register'))
        else:
            session['dates'] = [date.strftime('%Y-%m-%d') for date in generate_dates(session['selected_year'], session['selected_month'], session['selected_dayofweek'])]
            return redirect(url_for('events.events_register'))

    return render_template('events_register.html',
        place=session.get('location', '◯◯体育館'),
        description=session.get('description', '説明を入力'),
        selected_year=session.get('selected_year', datetime.now().year),
        selected_month=session.get('selected_month', (datetime.now().month % 12) + 1),
        selected_dayofweek=session.get('selected_dayofweek', 6),
        dates=session.get('dates', [date.strftime('%Y-%m-%d') for date in generate_dates(datetime.now().year, (datetime.now().month % 12) + 1, 6)]),
        start_hour=session.get('start_hour', 9),
        start_minute=session.get('start_minute', 0),
        end_hour=session.get('end_hour', 12),
        end_minute=session.get('end_minute', 0),
    )

@events_bp.route('/events/edit', methods=['POST'])
def events_edit():
    event_id = request.form['event_id']
    location = request.form['location']
    description = request.form['description']

    update_event(ObjectId(event_id), {"place": location, "description": description})

    return redirect(url_for('events.events_delete'))

@events_bp.route('/events/delete', methods=['GET', 'POST'])
def events_delete():
    if request.method == 'POST':
        if 'delete_event' in request.form:
            event_id = request.form['delete_event']
            delete_event(ObjectId(event_id), True)
            return redirect(url_for('events.events_delete'))

    events = find_all_events(ascending=True)
    return render_template('events_delete.html', events=events)
