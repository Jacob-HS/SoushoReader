from website import create_app
from flask import request
import json
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, send
import random
app = create_app()
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app, debug=True)
