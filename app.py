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
app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_SITE_KEY
app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_SECRET_KEY


class Formular(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    massage = TextAreaField("Massage")
    file = FileField(
        "File", validators=[FileRequired(), FileAllowed(["pdf"], "*.pdf only!")]
    )
    recaptcha = RecaptchaField("reCAPTCHA", validators=[DataRequired()])
    submit = SubmitField("Senden")


def language(html):
    route = request.path
    if "/en/" in route:
        html = "en/" + html
    return html


with open(
    os.path.join(app.root_path, "data", "Referenzen.json"),
    "r",
    encoding="utf-8-sig",
) as file:
    Referenzen = json.load(file)

with open(
    os.path.join(app.root_path, "data", "en/Referenzen.json"),
    "r",
    encoding="utf-8-sig",
) as file:
    Referenzen_en = json.load(file)

with open(
    os.path.join(app.root_path, "data", "Stellenanzeigen.json"),
    "r",
    encoding="utf-8",
) as file:
    Stellenanzeigen = json.load(file)

with open(
    os.path.join(app.root_path, "data", "en/Stellenanzeigen.json"),
    "r",
    encoding="utf-8",
) as file:
    Stellenanzeigen_en = json.load(file)


def render_template_(html, **context):
    return render_template(language(html), menu_bar=language("menuBar.html"), **context)


@app.route("/")
@app.route("/en/")
def index():
    return render_template_("index.html")


@app.route("/Impressum")
@app.route("/en/Impressum")
def impressum():
    return render_template_("impressum.html")


@app.route("/Datenschutz")
@app.route("/en/Datenschutz")
def datenschutz():
    return render_template_("datenschutz.html")


@app.template_filter("format_number")
def format_number(value):
    return f"{int(value):_}".replace("_", " ")


@app.route("/Referenzen")
@app.route("/en/Referenzen")
def referenzen():
    route = request.path
    data = Referenzen
    if "/en/" in route:
        data = Referenzen_en

    return render_template_("referenzen.html", data=data)


@app.route("/Referenzen/<Projekt>")
@app.route("/en/Referenzen/<Projekt>")
def projekt(Projekt):
    route = request.path
    data = Referenzen
    if "/en/" in route:
        data = Referenzen_en

    for item in data:
        if item["Bild"][:-4] == Projekt:
            return render_template_("projekt.html", item=item)


@app.route("/Karriere")
@app.route("/en/Karriere")
def karriere():
    route = request.path
    data = Stellenanzeigen
    if "/en/" in route:
        data = Stellenanzeigen_en

    return render_template_("karriere.html", data=data)


@app.route("/Karriere/<Stelle>")
@app.route("/en/Karriere/<Stelle>")
def stelle(Stelle):
    form = Formular()

    route = request.path
    data = Stellenanzeigen
    if "/en/" in route:
        data = Stellenanzeigen_en

    for item in data:
        if item["Name"][:-7] == Stelle:
            return render_template_(
                "stelle.html",
                item=item,
                recaptcha_site_key=RECAPTCHA_SITE_KEY,
                form=form,
            )


@app.route("/Geschaeftsfelder/<Geschaeftsfeld>")
@app.route("/en/Geschaeftsfelder/<Geschaeftsfeld>")
def geschaeftsfelder(Geschaeftsfeld):
    return render_template_(f"Geschaeftsfelder/{Geschaeftsfeld}.html")


@app.route("/Bilder/<Bild>")
@app.route("/en/Bilder/<Bild>")
def bild(Bild):
    return send_from_directory("static/Bilder", Bild)
