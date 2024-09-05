from flask import *
import json
import os

app = Flask(__name__)


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
    with open(
        os.path.join(app.root_path, "data", "Referenzen.json"),
        "r",
        encoding="utf-8-sig",
    ) as f:
        data = json.load(f)

    return render_template_("referenzen.html", data=data)


@app.route("/Referenzen/<Projekt>")
def projekt(Projekt):
    return render_template_("projekt.html")


@app.route("/Karriere")
def karriere():
    with open(
        os.path.join(app.root_path, "data", "Stellenanzeigen.json"),
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    return render_template_("karriere.html", data=data)


@app.route("/Karriere/<Stelle>")
def stelle(Stelle):
    with open(
        os.path.join(app.root_path, "data", "Stellenanzeigen.json"),
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    for item in data:
        if item['Name'][:-7] == Stelle:
            return render_template_("stelle.html", item=item)


@app.route("/Geschaeftsfelder/<Geschaeftsfeld>")
def geschaeftsfelder(Geschaeftsfeld):
    return render_template_(f"Geschaeftsfelder/{Geschaeftsfeld}.html")


if __name__ == "__main__":
    app.config["SERVER_NAME"] = "semen.net:666"
    app.run()
