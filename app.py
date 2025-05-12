from flask import *
import json
import os
from distutils.util import strtobool
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, EmailField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

with open(os.path.join(app.root_path, "data", "keys.json"), "r") as file:
    keys = json.load(file)

app.config["SECRET_KEY"] = keys["SECRET_KEY"]
app.config["SESSION_COOKIE_SECURE"] = True
app.config["WTF_CSRF_SSL_STRICT"] = False

RECAPTCHA_SITE_KEY = keys["RECAPTCHA_SITE_KEY"]
RECAPTCHA_SECRET_KEY = keys["RECAPTCHA_SECRET_KEY"]
app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_SITE_KEY
app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_SECRET_KEY

smtp_email = "noreply@b-a-e.eu"
password = keys["password"]


class KarriereFormular(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    telefon = StringField(
        "Telefonnummer",
        validators=[
            DataRequired(),
            Regexp(r"^\+?[0-9\s]{7,15}$", message="Invalid phone number."),
        ],
    )
    ort = SelectField(
        "Standort", choices=[("", "Standort*")], validators=[DataRequired()]
    )
    erfahrungTyp = SelectField(
        "Berufserfahrung",
        choices=[
            ("", "Berufserfahrung*"),
            ("Ja, innerhalb von Deutschland", "Ja, innerhalb von Deutschland"),
            ("Ja, außerhalb von Deutschland", "Ja, außerhalb von Deutschland"),
            ("Nein", "Nein"),
        ],
        validators=[DataRequired()],
    )
    erfahrung = SelectField(
        "Berufserfahrung",
        choices=[
            ("", "Berufserfahrung*"),
            ("Weniger als 3 Jahre", "Weniger als 3 Jahre"),
            ("Mehr als 3 Jahre", "Mehr als 3 Jahre"),
            ("Über 10 Jahre", "Über 10 Jahre"),
        ],
        validators=[DataRequired()],
    )
    deutsch = SelectField(
        "Deutschkenntnisse",
        choices=[
            ("", "Deutschkenntnisse*"),
            ("B1", "B1"),
            ("B2 bis C1", "B2 bis C1"),
            ("Muttersprache", "Muttersprache"),
        ],
        validators=[DataRequired()],
    )
    message = TextAreaField("Message")
    file = FileField("File", validators=[FileAllowed(["pdf"], "*.pdf only!")])
    recaptcha = RecaptchaField("reCAPTCHA")
    submit = SubmitField("Absenden")


class KontaktFormular(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    message = TextAreaField("Message")
    recaptcha = RecaptchaField("reCAPTCHA")
    submit = SubmitField("Absenden")


def send_email_karriere(form, Stelle):
    Name = form.name.data
    Email = form.email.data
    Telefon = form.telefon.data
    Standort = form.ort.data
    ErfahrungTyp = form.erfahrungTyp.data
    Erfahrung = form.erfahrung.data
    Deutsch = form.deutsch.data
    Message = form.message.data
    File = form.file.data

    body = f"""
    <html>
        <body>
            <p>
                <b>Name:</b> {Name} <br>
                <b>Email:</b> {Email} <br>
                <b>Telefonnummer:</b> {Telefon} <br>
                <b>Standort:</b> {Standort} <br>
                <b>Erfahrungstyp:</b> {ErfahrungTyp} <br>
                <b>Erfahrung:</b> {Erfahrung} <br>
                <b>Deutsch:</b> {Deutsch}
            </p>
            <p>
                <b>Message:</b> <br>
                {Message}
            </p>
        </body>
    </html>
    """

    message = EmailMessage()
    message["From"] = smtp_email
    message["To"] = "hr@b-a-e.eu"
    message["Subject"] = "Bewerbung " + Stelle

    if File:
        file_data = File.read()
        file_name = File.filename
        message.add_attachment(
            file_data, maintype="application", subtype="octet-stream", filename=file_name
        )
    else:
        body += "\nKeine Datei angehängt."
        
    message.add_alternative(body, subtype='html')

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(smtp_email, password)
        server.send_message(message)

    route = request.path

    if "/en/" in route:
        flash("Application has been sent and is being processed.", "success")
    else:
        flash("Bewerbung wurde geschickt und wird bearbeitet.", "success")


def send_email_kontakt(form):
    Name = form.name.data
    Email = form.email.data
    Message = form.message.data

    body = f"""
    <html>
        <body>
            <p>
                <b>Name:</b> {Name} <br>
                <b>Email:</b> {Email}
            </p>
            <p>
                <b>Message:</b> <br>
                {Message}
            </p>
        </body>
    </html>
    """

    message = EmailMessage()
    message["From"] = smtp_email
    message["To"] = "office@b-a-e.eu"
    message["Subject"] = "Kontaktformular Webseite"
    message.add_alternative(body, subtype='html')

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(smtp_email, password)
        server.send_message(message)

    route = request.path

    if "/en/" in route:
        flash("Contact form has been sent and is being processed.", "success")
    else:
        flash("Kontaktformular wurde geschickt und wird bearbeitet.", "success")


def language(html):
    route = request.path
    html = "en/" + html if "/en/" in route else html
    return html


with open(
    os.path.join(app.root_path, "data", "Standorte.json"),
    "r",
    encoding="utf-8-sig",
) as file:
    Standorte = json.load(file)

with open(
    os.path.join(app.root_path, "data", "en/Standorte.json"),
    "r",
    encoding="utf-8-sig",
) as file:
    Standorte_en = json.load(file)

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
    contactform = KontaktFormular()

    if contactform.validate_on_submit():
        send_email_kontakt(contactform)
        return redirect("/")
    else:
        if str(contactform.errors)[1:-1] != "":
            flash("Beim Senden sind Fehler aufgetreten", "danger")
            flash("Schicken Sie eine E-Mail auf hr@b-a-e.eu", "danger")
            print(contactform.errors)
            return redirect("/")

    return render_template(
        language(html),
        menu_bar=language("menuBar.html"),
        footer=language("footer.html"),
        consent=consent,
        contactform=contactform,
        **context,
    )


@app.route("/", methods=["GET", "POST"])
@app.route("/en/", methods=["GET", "POST"])
def index():
    route = request.path
    data = Referenzen_en if "/en/" in route else Referenzen
    standorte = Standorte_en if "/en/" in route else Standorte
    # if "/en/" in route:
    #     if request.cookies.get("language") == "de":
    #         return redirect("/")
    # else:
    #     if request.cookies.get("language") == "en":
    #         return redirect("/en/")

    return render_template_("index.html", data=data, standorte=standorte)


@app.route("/Impressum", methods=["GET", "POST"])
@app.route("/en/Impressum", methods=["GET", "POST"])
def impressum():
    return render_template_("impressum.html")


@app.route("/Datenschutz", methods=["GET", "POST"])
@app.route("/en/Datenschutz", methods=["GET", "POST"])
def datenschutz():
    return render_template_("datenschutz.html")


@app.template_filter("format_number")
def format_number(value):
    return f"{int(value):_}".replace("_", " ")


@app.route("/Referenzen", methods=["GET", "POST"])
@app.route("/en/Referenzen", methods=["GET", "POST"])
def referenzen():
    route = request.path
    data = Referenzen_en if "/en/" in route else Referenzen

    return render_template_("referenzen.html", data=data)


@app.route("/Referenzen/<Projekt>", methods=["GET", "POST"])
@app.route("/en/Referenzen/<Projekt>", methods=["GET", "POST"])
def projekt(Projekt):
    route = request.path
    data = Referenzen_en if "/en/" in route else Referenzen

    for item in data:
        if item["Bild"][:-4] == Projekt:
            return render_template_("projekt.html", item=item)


@app.route("/Karriere", methods=["GET", "POST"])
@app.route("/en/Karriere", methods=["GET", "POST"])
def karriere():
    route = request.path
    data = Stellenanzeigen_en if "/en/" in route else Stellenanzeigen

    return render_template_("karriere.html", data=data)


@app.route("/Karriere/<Stelle>", methods=["GET", "POST"])
@app.route("/en/Karriere/<Stelle>", methods=["GET", "POST"])
def stelle(Stelle):
    route = request.path
    data = Stellenanzeigen_en if "/en/" in route else Stellenanzeigen

    form = KarriereFormular()

    for item in data:
        if item["Name"][:-7] == Stelle:
            for Standort in item["Standort"].split(", "):
                form.ort.choices.append((Standort, Standort))

            if form.validate_on_submit():
                send_email_karriere(form, Stelle)
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
                # recaptcha_site_key=RECAPTCHA_SITE_KEY,
                form=form,
            )


@app.route("/Geschaeftsfelder/<Geschaeftsfeld>", methods=["GET", "POST"])
@app.route("/en/Geschaeftsfelder/<Geschaeftsfeld>", methods=["GET", "POST"])
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


# @app.route("/set_language/<lang>", methods=["POST"])
# def set_language(lang):
#     if lang == "en":
#         response = make_response(redirect("/en/"))
#     elif lang == "de":
#         response = make_response(redirect("/"))
#     else:
#         response = make_response(redirect("/"))
#         return response

#     if strtobool(request.cookies.get("cookie_consent")):
#         response.set_cookie("language", lang, max_age=60 * 60 * 24 * 365)
#     return response
