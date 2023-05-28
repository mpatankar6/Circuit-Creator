import json

# JSON Format: elements is a list that everything comes from.
# An element would be an object with a type and resistor object.
# When the element is parallel there is a branches array key which is filled with resistor elements
# If branches contains a list, elements can be put in there. This will allow limitless nesting.
# A branch of series resistors can be represented, or a parallel element can be inserted

MOCK_DATA = """
{
  "elements": [
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

json_data: list = json.loads(MOCK_DATA)["elements"]


def process_parallel_elm(element: list, circuit: str) -> str:
    resistor: dict
    for resistor in element:
        if isinstance(resistor, list):  # Element list as a branch
            circuit += "|" + process_elm_list(resistor, "") + "|"
            break
        circuit += "|" + "-" + resistor.get("name") + "-" + "|"
    return circuit


def process_elm_list(elements: list, circuit: str) -> str:
    elm: dict
    for elm in elements:
        if elm.get("type") == "Series":
            circuit += "-" + elm.get("resistor").get("name") + "-"
        elif elm.get("type") == "Parallel":
            circuit = process_parallel_elm(elm.get("branches"), circuit)
        else:
            pass
    return circuit


print(process_elm_list(json_data, ""))
