from flask import *
import json
import os
from distutils.util import strtobool
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, EmailField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

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

smtp_email = "it@b-a-e.eu"
password = keys["password"]
hr_email = "hr@b-a-e.eu"


class Formular(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    ort = SelectField(
        "Standort", choices=[("", "Standort*")], validators=[DataRequired()]
    )
    message = TextAreaField("Message")
    file = FileField(
        "File", validators=[FileRequired(), FileAllowed(["pdf"], "*.pdf only!")]
    )
    recaptcha = RecaptchaField("reCAPTCHA")
    submit = SubmitField("Senden")


def send_email(form, Stelle):
    Name = form.name.data
    Email = form.email.data
    Standort = form.ort.data
    Message = form.message.data
    File = form.file.data

    body = f"Name: {Name}\nEmail: {Email}\nStandort: {Standort}\nMessage: \n{Message}\n"

    message = EmailMessage()
    message["From"] = smtp_email
    message["To"] = hr_email
    message["Subject"] = "Bewerbung " + Stelle
    message.set_content(body)

    file_data = File.read()
    file_name = File.filename
    message.add_attachment(
        file_data, maintype="application", subtype="octet-stream", filename=file_name
    )

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(smtp_email, password)
        server.send_message(message)

    route = request.path

    if "/en/" in route:
        flash("Application has been sent and is being processed.", "success")
    else:
        flash("Bewerbung wurde geschickt und wird bearbeitet.", "success")


def language(html):
    route = request.path
    html = "en/" + html if "/en/" in route else html
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
    consent = request.cookies.get("cookie_consent")
    return render_template(
        language(html), menu_bar=language("menuBar.html"), consent=consent, **context
    )


@app.route("/")
@app.route("/en/")
def index():
    route = request.path
    data = Referenzen_en if "/en/" in route else Referenzen
    if "/en/" in route:
        if request.cookies.get("language") == "de":
            return redirect("/")
    else:
        if request.cookies.get("language") == "en":
            return redirect("/en/")
        
    return render_template_("index.html", data=data)


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
    data = Referenzen_en if "/en/" in route else Referenzen

    return render_template_("referenzen.html", data=data)


@app.route("/Referenzen/<Projekt>")
@app.route("/en/Referenzen/<Projekt>")
def projekt(Projekt):
    route = request.path
    data = Referenzen_en if "/en/" in route else Referenzen

    for item in data:
        if item["Bild"][:-4] == Projekt:
            return render_template_("projekt.html", item=item)


@app.route("/Karriere")
@app.route("/en/Karriere")
def karriere():
    route = request.path
    data = Stellenanzeigen_en if "/en/" in route else Stellenanzeigen

    return render_template_("karriere.html", data=data)


@app.route("/Karriere/<Stelle>", methods=["GET", "POST"])
@app.route("/en/Karriere/<Stelle>", methods=["GET", "POST"])
def stelle(Stelle):
    route = request.path
    data = Stellenanzeigen_en if "/en/" in route else Stellenanzeigen

    form = Formular()

    for item in data:
        if item["Name"][:-7] == Stelle:
            for Standort in item["Standort"].split(", "):
                form.ort.choices.append((Standort, Standort))

            if form.validate_on_submit():
                send_email(form, Stelle)
                return redirect("/en/Karriere" if "/en/" in route else "/Karriere")
            else:
                if str(form.errors)[1:-1] != "":
                    if "/en/" in route:
                        flash("Errors occurred during transmission", "danger")
                        flash("Send an e-mail to hr@b-a-e.eu", "danger")
                    else:
                        flash("Beim Senden sind Fehler aufgetreten", "danger")
                        flash("Schicken Sie eine E-Mail auf hr@b-a-e.eu", "danger")
                    print(form.errors)
                    return redirect("/en/Karriere" if "/en/" in route else "/Karriere")

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


@app.route("/Bilder/TextBilder/<Bild>")
@app.route("/Bilder/TextBilder/en/<Bild>")
@app.route("/Bilder/<Bild>")
def bild(Bild):
    route = request.path
    if "/TextBilder/" in route:
        if "/en/" in route:
            return send_from_directory("static/Bilder/TextBilder/en", Bild)
        else:
            return send_from_directory("static/Bilder/TextBilder", Bild)
    else:
        return send_from_directory("static/Bilder", Bild)


@app.route("/set_cookie_consent/<value>", methods=["POST"])
def set_cookie(value):
    response = make_response(redirect("/"))
    value = strtobool(value)
    if value:
        response.set_cookie("cookie_consent", str(value), max_age=60 * 60 * 24 * 365)
    else:
        response.set_cookie("cookie_consent", str(value))
    
    return response


@app.route('/set_language/<lang>', methods=['POST'])
def set_language(lang):
    if lang == "en":
        response = make_response(redirect("/en/"))
    elif lang == "de":
        response = make_response(redirect("/"))
    else:
        response = make_response(redirect("/"))
        return response
    
    if strtobool(request.cookies.get("cookie_consent")):
        response.set_cookie("language", lang, max_age=60 * 60 * 24 * 365)
    return response

