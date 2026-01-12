from flask import Blueprint, request, render_template, redirect, url_for
from bson import ObjectId
from datetime import datetime

from repositories.mongo_repository import find_all_events, find_all_entries, delete_entry, update_entry_option

entries_bp = Blueprint('entries', __name__)

@entries_bp.route('/entries/list')
def entries_list():
    events = find_all_events(ascending=True)
    entries = find_all_entries()

    events_by_id = {str(event["_id"]): event for event in events}
    entry_rows = []
    for entry in entries:
        event = events_by_id.get(entry.get("eventId"))
        if event:
            event_label = f"{event['startTime'].strftime('%Y-%m-%d %H:%M')} - {event.get('place', '')}"
            event_sort = event["startTime"]
        else:
            event_label = "????????"
            event_sort = datetime.max

        entry_rows.append({
            "entry_id": str(entry.get("_id")),
            "event_label": event_label,
            "user_name": entry.get("user", {}).get("displayName", ""),
            "option_id": entry.get("selectedOptionId", ""),
            "event_sort": event_sort,
        })

    entry_rows.sort(key=lambda row: row["event_sort"], reverse=True)
    return render_template('entries_list.html', entries=entry_rows)

@entries_bp.route('/entries/edit', methods=['POST'])
def entries_edit():
    entry_id = request.form['entry_id']
    selected_option_id = request.form['selected_option_id']
    update_entry_option(ObjectId(entry_id), selected_option_id)
    return redirect(url_for('entries.entries_list'))

@entries_bp.route('/entries/delete', methods=['POST'])
def entries_delete():
    entry_id = request.form['entry_id']
    delete_entry(ObjectId(entry_id))
    return redirect(url_for('entries.entries_list'))
