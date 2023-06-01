from website import create_app
from flask import request
import json
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, send
import random
import cv2
import numpy as np
app = create_app()
socketio = SocketIO(app)

@socketio.event
def askQuestion (data):
    im = cv2.imdecode(np.array(data["data"], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imshow('image',im)
    cv2.waitKey(0)

if __name__ == '__main__':
    socketio.run(app, debug=True)
