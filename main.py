from flask import Flask, session, request, render_template, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "hy572"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)

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
        return render_template("main.html", name=name)
    else:
        return redirect(url_for("entername"))

@app.route("/home")
def home():
    if "name" in session:
        return "hello"
    return redirect(url_for("entername"))

@app.route("/")
def redirects():
    if "name" in session:
        return redirect(url_for("home"))
    return redirect(url_for("home"))

@app.route("/entername", methods=["POST","GET"])
def entername():
    if "name" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        return redirect(url_for("main", room_name="f"))
    return render_template("entername.html")

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)