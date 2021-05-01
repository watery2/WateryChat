from flask import Flask, session, request, render_template, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "hy572"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.main'
socketio = SocketIO(app)

db = SQLAlchemy(app)

class Msg(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String,nullable=False)
    name = db.Column(db.String,nullable=False)
    msg = db.Column(db.String,nullable=False)

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
        messages = Msg.query.filter_by(room_name=room_name).all()
        msgs = []
        names = []
        try:
            for i in messages:
                msgs.append(i.msg)
                names.append(i.name)
        except AttributeError:
            pass
        if len(msgs) > 100:
            del msgs[:len(msgs) - 100]
            del names[:len(names) - 100]
        msgs_len = len(msgs)
        return render_template("main.html", name=name, room_name=room_name, msgs=msgs, names=names, msg_len=msgs_len)
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

@app.route("/save", methods=["POST"])
def save():
    if request.is_json:
        req = request.get_json()
        new_msg = Msg(room_name = req["room_name"],name = req["name"],msg = req["msg"])
        db.session.add(new_msg)
        db.session.commit()

        return "working"
    return "not"


if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)