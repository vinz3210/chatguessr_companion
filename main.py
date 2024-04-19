import threading
import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import os

from database_handler import DatabaseHandler
from global_settings import GlobalSettings
from global_settings_loader import GlobalSettingsLoader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

dashboard_instance = None
scoreboard_instance = None
global_settings_loader = GlobalSettingsLoader()
global_settings = global_settings_loader.load_global_settings()
database = DatabaseHandler(global_settings)
if global_settings.get_streamer_name() is None:
    streamer_name = database.get_streamer_name()
    global_settings.set_streamer_name(streamer_name)

@app.route('/')
def index():
    # print the current working directory
    print(os.getcwd())
    return render_template('index.html')

@app.route('/static/<path:path>')
def catch_all(path):
    # return file from the static folder
    #print static folder path
    return app.send_static_file(path)

@app.route('/scoreboard')
def index_scoreboard():
    # print the current working directory
    print(os.getcwd())
    return render_template('scoreboard.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('register_dashboard')
def register_dashboard(request_ = None):
    global dashboard_instance
    if request is not None:
        dashboard_instance = request.sid
    else:
        dashboard_instance = request_.sid
    print('Dashboard registered')
    print(global_settings.get_db_path())
    socketio.emit('get_dashboard_infos', {
        'db_path': global_settings.get_db_path(),
        'streamer_name': global_settings.get_streamer_name(),
        'db_file_exists': os.path.exists(global_settings.get_db_path()),
    }, room=dashboard_instance)

@socketio.on('register_scoreboard')
def register_client():
    global scoreboard_instance
    scoreboard_instance = request.sid
    print('scoreboard registered')

@socketio.on('save_streamer_name')
def save_streamer_name(data):
    global_settings.set_streamer_name(data)
    global_settings_loader.save_global_settings(global_settings)
    print('Streamer name saved')
    socketio.emit('snackbar', "saved streamer name: "+data, room=dashboard_instance)

@socketio.on('save_db_path')
def save_db_path(data):
    global_settings.set_file(data)
    global_settings_loader.save_global_settings(global_settings)
    print('DB path saved')
    global database
    database = DatabaseHandler(global_settings)
    streamer_name = database.get_streamer_name()
    global_settings.set_streamer_name(streamer_name)
    socketio.emit('snackbar', "saved db path: "+data, room=dashboard_instance)
    socketio.emit('refresh_register_dashboard', room=dashboard_instance)

@socketio.on('dash_test_click')
def dash_test_click():
    print('Dashboard clicked')
    # Send message to scoreboard
    socketio.emit('dash_test_click', room=scoreboard_instance)
i = 0
def count():
    while True:
        time.sleep(1)
        global i
        i += 1
        if i % 10 == 0:
            socketio.emit('count', i)

global stats_mode
stats_mode = "30_days"
def emit_leaderboard_data():
    while not os.path.exists(global_settings.get_db_path()):
        time.sleep(1)
    leaderboard_database = DatabaseHandler(global_settings)
    while True:
        time.sleep(1)
        data = {
            "30_days": leaderboard_database.getStatsLast30Days(),
            "total": leaderboard_database.getTotalStats(),
            "stats_mode": stats_mode,
        }
        socketio.emit('leaderboard', data, room=scoreboard_instance)
        
current_game_state = "finished"
def emit_current_game_state():
    
    while not os.path.exists(global_settings.get_db_path()):
        time.sleep(1)
    leaderboard_database = DatabaseHandler(global_settings)
    global current_game_state

    while True:
        time.sleep(1)
        game_state = leaderboard_database.get_current_game_state()

        if game_state != current_game_state:
            current_game_state = game_state
            socketio.emit('game_state', current_game_state, room=scoreboard_instance)

if __name__ == '__main__':
    # create a new thread for the count function
    threading.Thread(target=emit_leaderboard_data).start()
    threading.Thread(target=emit_current_game_state).start()
    
    socketio.run(app)