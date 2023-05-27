from typing import Dict
from flask import Flask, render_template, request

from kirchoff_solver import calculate_circuit_properties, generate_drawing, parse_circuit_data

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
        circuit_props = calculate_circuit_properties(
            request.form.items())
        print(request.form.to_dict().items())
        for key, val in request.form.to_dict().items():
            print(f"{key} {val}")
        return render_template("data.html",
                               form_data=request.form,
                               circuit_image=image_svg,
                               circuit_props=circuit_props)
