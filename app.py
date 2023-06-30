import json

from flask import Flask, render_template, request

from circuit_drawer import generate_drawing, calculate_circuit

app: Flask = Flask(__name__)


@app.route("/")
def start() -> str:
    return render_template("index.jinja", title="Circuit Maker")


@app.route("/data/", methods=["GET", "POST"])
def data() -> str:
    if request.method == "POST":
        form_data = request.get_json()
        return load_data_page(form_data)
    return "Invalid HTTP Request"


@app.route("/example/", methods=["GET", "POST"])
def example() -> str:
    if request.method == "GET":
        with open(r"static/example.json", encoding="UTF-8") as json_file:
            example_data = json.load(json_file)
            return load_data_page(example_data)
    return "Invalid HTTP Request"


def load_data_page(json_data: str) -> str:
    circuit_image = generate_drawing(json_data)
    circuit_stats, resistor_data = calculate_circuit(json_data)
    return render_template(
        "data.jinja",
        title="Circuit Data",
        circuit_image=circuit_image,
        circuit_stats=circuit_stats,
        resistor_data=resistor_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
