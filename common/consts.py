SHOW_NEXT_EVENT = "show_next"
SHOW_EVENTS = "show_events"
SELECT_EVENT_TO_ENTRY = "select_event"
SELECT_EVENT_TO_ENTRY_EVENT = "event"
ENTRY_WITH_OPTION = "entry"
ENTRY_WITH_OPTION_EVENT = "event"
ENTRY_WITH_OPTION_OPTION = "option"
AKIO_BUTTON = "akio"
#
# POSTBACK_EVENTS = {
#     "ENTRY_START": {
#         "name": "entry_start",
#     },
#     "SELECT_EVENT_TO_ENTRY": {
#         "name": "select_event",
#         "params": { "EVENT": "event" }
#     },
#     "ENTRY_WITH_OPTION": {
#         "name": "entry",
#         "params": { "EVENT": "event", "OPTION": "option" }
#     }
# }

# def postback_data_text(event_key, params_with_key):
#     text = f'{POSTBACK_EVENTS[event_key]}'
#     if (params_with_key):
#         params_target = {}
#         for key, value in params_with_key.items():
#             if key in POSTBACK_EVENTS[event_key]["params"]:
#                 target_key = POSTBACK_EVENTS[event_key]["params"][key]
#                 params_target[target_key] = value
#
#         text += f'/?{urlencode(params_with_key)}'
