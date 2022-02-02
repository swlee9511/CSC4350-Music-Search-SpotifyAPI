import flask
import os
import json
from spotify import get_song_data, search_artist
from genius import get_lyrics_url
from flask_sqlalchemy import SQLAlchemy
from random import randint


app = flask.Flask(__name__, static_folder="./build/static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# app setup
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://qsrfkcshuiiitf:dea46cd21a57682edbbae68dcd8d86baee0dfb0294dbab2521e7e624a9ee3cb4@ec2-44-199-83-229.compute-1.amazonaws.com:5432/duvvnplak92ef"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# basic DB setup
db = SQLAlchemy(app)
# modify DB, create table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)


class ArtistID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(50), nullable=False)


# create table if it doesn't exist, if exists do nothing
db.create_all()

# for keeping track of user
current_user = ""

# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route("/main", methods=["GET", "POST"])
def main():
    items = ArtistID.query.all()
    db_artist_id = []
    for item in items:
        db_artist_id.append(item.artist_id)
    artist_name = []
    for i in db_artist_id:
        datas = get_song_data(i)
        artist_name.append(datas["artist_name"])

    # create parameter data
    if len(db_artist_id) == 0:
        tame_impala_id = "5INjqkS1o8h1imAzPqGZBb"
        song_data = get_song_data(tame_impala_id)
        lyrics_url = get_lyrics_url(song_data["artist_name"])
    else:
        song_data = get_song_data(db_artist_id[randint(0, len(db_artist_id) - 1)])
        lyrics_url = get_lyrics_url(song_data["artist_name"])

    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {
        "song_name": song_data["song_name"],
        "artist_name": song_data["artist_name"],
        "song_image": song_data["song_image"],
        "song_preview": song_data["song_preview"],
        "lyrics_url": lyrics_url,
        "artist_name_list": artist_name,
        "current_user": current_user,
        "artist_id_list": db_artist_id,
    }
    data = json.dumps(DATA)

    return flask.render_template("index.html", data=data)


app.register_blueprint(bp)


@app.route("/", methods=["GET", "POST"])
def index():
    items = User.query.all()
    user_id = []
    for item in items:
        user_id.append(item.user_id)

    if current_user == "":
        return flask.render_template(
            "front_page.html",
            length=len(user_id),
            user_id=user_id,
        )
    return flask.redirect("/main")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    # GET user_id from db
    items = User.query.all()
    user_id = []
    for item in items:
        user_id.append(item.user_id)

    if flask.request.method == "POST":
        val = flask.request.form.get("user_id")
        # check if user id already exists
        for i in user_id:
            if val == i:
                flask.flash("Same ID Already Exists in DB!")
                return flask.redirect("/")
        new_user = User(user_id=val)
        db.session.add(new_user)
        db.session.commit()

    return flask.render_template(
        "front_page.html",
        length=len(user_id),
        user_id=user_id,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    user_input = flask.request.form["user_id"]
    # GET info from db
    items = User.query.all()
    user_id = []
    for item in items:
        user_id.append(item.user_id)

    # check if user input exist in db.user_id
    for i in user_id:
        if user_input == i:
            global current_user
            current_user = user_input
            return flask.redirect("/main")

    # flash alert and redirect to front page
    flask.flash("Wrong user ID!")
    return flask.redirect("/")


@app.route("/add_artist_to_db", methods=["GET", "POST"])
def add_artist_to_db():
    artist_name_list = []

    if flask.request.method == "POST":
        input_list = flask.request.json.get("artist_name")
        for i in input_list:
            data = search_artist(i)
            if data == "-1":
                artist_error = True
            else:
                new_artist = ArtistID(artist_id=data)
                db.session.add(new_artist)
                db.session.commit()

                song_data = get_song_data(data)
                temp = song_data["artist_name"]
                artist_name_list.append(temp)
                artist_error = False

            if artist_error == True:
                return flask.jsonify({"input_server": False})

    return flask.jsonify({"input_server": artist_name_list})


@app.route("/delete_artist", methods=["GET", "POST"])
def delete_artist():
    id_to_delete = flask.request.json.get("id")
    temp = ArtistID.query.filter_by(artist_id=id_to_delete).first()
    db.session.delete(temp)
    db.session.commit()
    result = ArtistID.query.all()
    return flask.jsonify({"after_delete": result})


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
