from flask import *
import json
import os
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = "uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

with open(os.path.join(app.root_path, "data", "keys.json"), "r") as file:
    keys = json.load(file)

RECAPTCHA_SITE_KEY = keys["RECAPTCHA_SITE_KEY"]
RECAPTCHA_SECRET_KEY = keys["RECAPTCHA_SECRET_KEY"]
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_SITE_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_SECRET_KEY

class Formular(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    massage = TextAreaField('Massage')
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['pdf'], '*.pdf only!')
        ])
    recaptcha = RecaptchaField('reCAPTCHA', validators=[DataRequired()])
    submit = SubmitField('Senden')

with open(
    os.path.join(app.root_path, "data", "Referenzen.json"),
    "r",
    encoding="utf-8-sig",
) as file:
    Referenzen = json.load(file)

with open(
    os.path.join(app.root_path, "data", "Stellenanzeigen.json"),
    "r",
    encoding="utf-8",
) as file:
    Stellenanzeigen = json.load(file)


def render_template_(html, **context):
    return render_template(html, menu_bar="menuBar.html", **context)


@app.route("/")
def index():
    return render_template_("index.html")


@app.route("/Impressum")
def impressum():
    return render_template_("impressum.html")


@app.route("/Datenschutz")
def datenschutz():
    return render_template_("datenschutz.html")


@app.template_filter("format_number")
def format_number(value):
    return f"{int(value):_}".replace("_", " ")


@app.route("/Referenzen")
def referenzen():
    return render_template_("referenzen.html", data=Referenzen)


@app.route("/Referenzen/<Projekt>")
def projekt(Projekt):
    for item in Referenzen:
        if item["Bild"][:-4] == Projekt:
            return render_template_("projekt.html", item=item)


@app.route("/Karriere")
def karriere():
    return render_template_("karriere.html", data=Stellenanzeigen)


@app.route("/Karriere/<Stelle>")
def stelle(Stelle):
    form = Formular()

    for item in Stellenanzeigen:
        if item["Name"][:-7] == Stelle:
            return render_template_(
                "stelle.html", item=item, recaptcha_site_key=RECAPTCHA_SITE_KEY, form=form
            )


@app.route("/Geschaeftsfelder/<Geschaeftsfeld>")
def geschaeftsfelder(Geschaeftsfeld):
    return render_template_(f"Geschaeftsfelder/{Geschaeftsfeld}.html")


@app.route("/Bilder/<Bild>")
def bild(Bild):
    return send_from_directory("static/Bilder", Bild)
