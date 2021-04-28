from flask import Flask, session, request, render_template, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = "hy572"
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(msg):
    print('got the msg ' + msg["msg"])
    room = msg["url"]
    name = session["name"]
    msg_name = {"msg": msg["msg"],"name":name}
    join_room(room)
    send(msg_name, to=room)

@app.route("/room/<room_name>")
def main(room_name):
    if "name" in session:
        name = session["name"]
        room_name = room_name
        return render_template("main.html", name=name, room_name=room_name)
    else:
        return redirect(url_for("entername"))

@app.route("/home")
def home():
    if "name" in session:
        return render_template("home.html")
    return redirect(url_for("entername"))

@app.route("/")
def redirects():
    if "name" in session:
        return redirect(url_for("home"))
    return redirect(url_for("home"))

@app.route("/entername", methods=["POST","GET"])
def entername():
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        return redirect(url_for("home"))
    return render_template("entername.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)