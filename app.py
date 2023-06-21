import json

from flask import Flask, render_template, request

from circuit_drawer import generate_drawing, calculate_circuit

app: Flask = Flask(__name__)


@app.route("/")
def start() -> str:
    return render_template("index.html", title="Circuit Simulator")


@app.route("/data/", methods=["GET", "POST"])
def data() -> str:
    if request.method == "GET":
        return "Invalid Request"

    if request.method == "POST":
        print(request.form.to_dict().items())
        for key, val in request.form.to_dict().items():
            print(f"{key} {val}")
        return render_template(
            "data.html",
            form_data=request.form,
        )


@app.route("/test/")
def test() -> str:
    example_data = json.load(open(r"static/example.json", encoding="UTF-8"))
    my_circuit_image = generate_drawing(example_data)
    circuit_stats, resistor_data = calculate_circuit(example_data)
    return render_template(
        "test.html",
        circuit_image=my_circuit_image,
        circuit_stats=circuit_stats,
        resistor_data=resistor_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
