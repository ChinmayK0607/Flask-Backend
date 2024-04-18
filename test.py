from flask import Flask, request, render_template, redirect, url_for, session,jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
from queue import  Queue
from utils import find_room, init_room_queues
#from utils import find_room
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SDKFJSDFOWEIOF'
socketio = SocketIO(app)

PREDEFINED_ROOMS = ['coding', 'interview', 'chill']
rooms = {room_name: {'members': 0, 'messages': []} for room_name in PREDEFINED_ROOMS}
coding_queue = []
interview_queue = []
chill_queue = []

#init_room_queues(PREDEFINED_ROOMS, room_queue)



@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get('name')
        room_name = request.form.get('room_name')
        if not name or room_name.lower() not in PREDEFINED_ROOMS:
            return render_template('home.html', error="Name is required and room must be one of the predefined rooms: coding, interview, chill", room_name=room_name)
        session['name'] = name
        session['room'] = room_name
        return redirect(url_for('room'))
    return render_template('home.html')

@app.route('/join_queue/<string:room_code>', methods=['POST'])
def join_queue(room_code):
    name = session.get('name')
    room = room_code
    if room == "coding":
        coding_queue.append(name)
        print(coding_queue)
    elif room == "interview":
        interview_queue.append(name)
        print(interview_queue)
    elif room == "chill":
        chill_queue.append(name)
        print(chill_queue)
    
    messages = rooms[room]['messages']
    
    return render_template('room.html', room=room, user=name, messages=messages),jsonify({'message': 'Joined the queue'}), 200
#@app.route('/show_room_queue',methods = ['GET'])
#def show_rooms():
 #   return jsonify(str(room_queue))
@app.route('/room')
def room():
    name = session.get('name')
    room = session.get('room')
    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))
    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages)

@socketio.on('connect')
def handle_connect():
    name = session.get('name')
    room = session.get('room')
    if name is None or room is None or room not in rooms:
        return
    join_room(room)
    rooms[room]["members"] += 1
    send({"sender": "", "message": f"{name} has entered the chat"}, to=room)

@socketio.on('message')
def handle_message(payload):
    room = session.get('room')
    name = session.get('name')
    if room not in rooms:
        return
    message = {"sender": name, "message": payload["message"]}
    send(message, to=room)
    rooms[room]["messages"].append(message)

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
        send({"message": f"{name} has left the chat", "sender": ""}, to=room)
    leave_room(room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
