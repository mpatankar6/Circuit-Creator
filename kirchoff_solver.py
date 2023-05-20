from typing import Iterator

import numpy as np
import schemdraw
import schemdraw.elements as element
from scipy import linalg


def generate_drawing(data: Iterator[tuple[str, str]]) -> bytes:
    # a: enumerate = enumerate(data)
    with schemdraw.Drawing(show=False) as drawing:
        drawing.add(element.Battery())
        for entry in data:
            if entry[0].startswith("R"):
                drawing.add(element.Resistor().label(entry[1] + "Ω"))
                print("RESISTOR")
    return drawing.get_imagedata("svg")
