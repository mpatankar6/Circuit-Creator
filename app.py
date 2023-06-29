import json

from flask import Flask, render_template, request

from circuit_drawer import generate_drawing, calculate_circuit

app: Flask = Flask(__name__)


@app.route("/")
def start() -> str:
    return render_template("index.jinja", title="Circuit Simulator")


@app.route("/data/", methods=["GET", "POST"])
def data() -> str:
    if request.method == "GET":
        return "Invalid Request"

    if request.method == "POST":
        example_data = request.get_json()
        my_circuit_image = generate_drawing(example_data)
        circuit_stats, resistor_data = calculate_circuit(example_data)
        return render_template(
            "test.jinja",
            circuit_image=my_circuit_image,
            circuit_stats=circuit_stats,
            resistor_data=resistor_data,
        )


@app.route("/test/")
def test() -> str:
    example_data = json.load(open(r"static/example.json", encoding="UTF-8"))
    my_circuit_image = generate_drawing(example_data)
    circuit_stats, resistor_data = calculate_circuit(example_data)
    return render_template(
        "test.jinja",
        circuit_image=my_circuit_image,
        circuit_stats=circuit_stats,
        resistor_data=resistor_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
