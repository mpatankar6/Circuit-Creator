import json
from typing import Dict

from flask import Flask, render_template, request

from kirchoff_solver import (
    calculate_circuit_properties,
    parse_circuit_data,
)

from circuit_drawer import generate_drawing

app: Flask = Flask(__name__)


@app.route("/")
def start() -> str:
    return render_template("index.html", title="Circuit Simulator")


@app.route("/data/", methods=["GET", "POST"])
def data() -> str:
    if request.method == "GET":
        return "Invalid"

    if request.method == "POST":
        circuit_props = calculate_circuit_properties(request.form.items())

        print(request.form.to_dict().items())

        for key, val in request.form.to_dict().items():
            print(f"{key} {val}")
        return render_template(
            "data.html",
            form_data=request.form,
            circuit_props=circuit_props,
        )


@app.route("/test/")
def test() -> str:
    mock_data = """{
  "components": [
    {
      "type": "Series",
      "resistor": {
        "name": "R0",
        "resistance": 100
      }
    },
    {
      "type": "Series",
      "resistor": {
        "name": "R1",
        "resistance": 150
      }
    },
    {
      "type": "Parallel",
      "branches": [
        {
          "name": "R2",
          "resistance": 200
        },
        {
          "name": "R3",
          "resistance": 30
        },
        [
          {
            "type": "Series",
            "resistor": {
              "name": "R4",
              "resistance": 600
            }
          },
          {
            "type": "Parallel",
            "branches": [
              {
                "name": "R5",
                "resistance": 100
              },
              {
                "name": "R6",
                "resistance": 900
              }
            ]
          }
        ],
        {
          "type": "Parallel",
          "name": "R7",
          "resistance": 5000
        }
      ]
    },
    {
      "type": "Series",
      "resistor": {
        "name": "R7",
        "resistance": 150
      }
    }
  ]
}
"""
    my_circuit_image = generate_drawing(json.loads(mock_data))
    return render_template("test.html", circuit_image=my_circuit_image)


if __name__ == "__main__":
    app.run(debug=True)
