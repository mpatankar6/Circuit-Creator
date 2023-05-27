from typing import Dict, Iterator

import numpy as np
import schemdraw
import schemdraw.elements as element
from scipy import linalg


def generate_drawing(data: Iterator[tuple[str, str]]) -> bytes:
    circuit_dim = [0, 0]
    info: Dict[str, str] = parse_circuit_data(data)
    with schemdraw.Drawing(show=False) as drawing:
        drawing.add(element.Battery().label(f"{info['battery_voltage']} V"))
        for key, value in info.items():
            if key.endswith("series"):
                draw_series_resistors(value, circuit_dim, drawing)
        complete_circuit(circuit_dim, drawing)
    return drawing.get_imagedata("svg")


def draw_series_resistors(resistor_list: list, circuit_dim, drawing: schemdraw.Drawing):
    for resistor in resistor_list:
        drawing.add(element.Resistor().label(f"{resistor} Ω"))
        circuit_dim[0] += 1


def complete_circuit(circuit_dim, drawing: schemdraw.Drawing) -> None:
    drawing.add(element.Line().down())
    for _ in range(circuit_dim[0] + 1):
        drawing.add(element.Line().left())
    drawing.add(element.Line().up())


def calculate_circuit_properties(data: Iterator[tuple[str, str]]) -> Dict[str, str]:
    info: Dict[str, str] = parse_circuit_data(data)
    total_resistance: float = 0
    total_current: float = 0
    total_voltage: float = float(info["battery_voltage"])
    for key, value in info.items():
        if key.endswith("series"):
            for resistor in value:
                total_resistance += int(resistor)
    total_current = round(total_voltage / total_resistance, 5)
    return {
        "V_t": f"{total_voltage} V",
        "R_t": f"{total_resistance} Ω",
        "I_t": f"{total_current} A"
    }


def parse_circuit_data(data: Iterator[tuple[str, str]]) -> dict:
    info: dict = dict()
    resistor_list: list = list()
    index: int = 0
    was_parallel: bool = False
    for key, value in data:
        if key.startswith("B"):
            info["battery_voltage"] = value
        if key.startswith("R"):
            is_parallel = key.endswith("Parallel")
            # Detect switch in type
            if is_parallel is not was_parallel:
                was_parallel = not was_parallel
                # Defends against edge case where parallel comes first
                if info.keys().__len__() >= 2:
                    index += 1
                resistor_list = list()
            resistor_list.append(value)
            element_type: str = "parallel" if is_parallel else "series"
            info[f"resistor_element {index} {element_type}"] = resistor_list
    return info


class Component:
    def __init__(self) -> None:
        pass
