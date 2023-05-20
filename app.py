from re import escape
from flask import Flask, render_template, request
from markupsafe import Markup, escape

from kirchoff_solver import generate_drawing

app: Flask = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return render_template("index.html", title="Circuit Simulator")


@app.route("/data/", methods=["GET", "POST"])
def data() -> str:
    if request.method == "GET":
        return "Invalid"
    if request.method == "POST":
        image_raw: bytes = generate_drawing(request.form.items())
        image_svg: str = str(image_raw).replace(r'\n', '\n')[2:-1]
        return render_template("data.html", form_data=request.form, circuit_image=image_svg)
