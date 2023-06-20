import math

from schemdraw import Drawing, elements
from schemdraw.types import Point

LINE_LENGTH = 3  # In accordance with schemdraw
PRECISION = 4


def generate_drawing(json_data: dict) -> str:
    with Drawing(show=False) as drawing:
        drawing.config(color="white")
        drawing.add(elements.Battery())
        draw_element_list(json_data["components"], drawing)

    print(calculate_circuit(json_data))
    raw_image_data: bytes = drawing.get_imagedata("svg")
    return str(raw_image_data).replace(r"\n", "\n")[2:-1]


def draw_element_list(components: list, drawing: Drawing) -> dict:
    element_list: dict = {}
    for component in components:
        if component.get("type") == "Series":
            resistor: dict = component.get("resistor")
            drawing.add(_r := elements.Resistor().label(get_resistor_label(resistor)))
            element_list[resistor.get("name")] = _r
        elif component.get("type") == "Parallel":
            element_list = element_list | draw_parallel_element(
                component.get("branches"), drawing
            )
        else:
            raise RuntimeError("Invalid JSON?")
    return element_list


def draw_parallel_element(branches: list, drawing: Drawing) -> dict:
    element_list: dict = {}
    circuit_height: int = get_circuit_height(branches)
    circuit_width: int = get_circuit_width(branches)
    start_point: Point = drawing.here
    # This is 3 units above the top resistor
    top_bound: int = math.floor(circuit_height / 2) * LINE_LENGTH
    print(f"Height: {circuit_height}, Width {circuit_width}")
    drawing.move_from(drawing.here, 0, top_bound)
    for resistor in branches:
        drawing.move(0, -3)
        if isinstance(resistor, list):
            element_list = element_list | draw_element_list(resistor, drawing)
            break
        start_pos: Point = drawing.here
        drawing.add(_r := elements.Resistor().label(get_resistor_label(resistor)))
        element_list[resistor.get("name")] = _r
        for _ in range(circuit_width - 1):
            drawing.add(elements.Line())
        _dx, _dy = calc_delta(start_pos, drawing.here)
        drawing.move(-_dx, 0)
    drawing.theta = 270
    drawing.move_from(start_point, 0, top_bound - 3)
    for _ in range(len(branches) - 1):
        drawing.add(elements.Line())
    # Overlapping lines but who cares
    drawing.move_from(start_point, circuit_width * LINE_LENGTH, top_bound - 3)
    for _ in range(circuit_height - 1):
        drawing.add(elements.Line())
    drawing.move_from(start_point, circuit_width * LINE_LENGTH, 0, 0)
    return element_list


def calc_delta(p_i: Point, p_f: Point) -> tuple:
    x_delta = p_f.x - p_i.x
    y_delta = p_f.y - p_i.y
    return x_delta, y_delta


def get_resistor_label(resistor: dict) -> str:
    return f"${resistor.get('name')}$"


def get_circuit_height(branches: list) -> int:
    height: int = len(branches)
    for component_list in filter(lambda x: isinstance(x, list), branches):
        for component in get_components_of_type("Parallel", component_list):
            height += get_circuit_height(component.get("branches")) - 1
    return height


def get_circuit_width(branches: list) -> int:
    width: int = 1
    for component_list in filter(lambda x: isinstance(x, list), branches):
        series_components = get_components_of_type("Series", component_list)
        width += len(list(series_components)) - 1
        for component in get_components_of_type("Parallel", component_list):
            width += get_circuit_width(component.get("branches"))
    return width


def get_components_of_type(r_type: str, component_list: list) -> iter:
    return filter(lambda x: x.get("type") == r_type, component_list)


def calculate_circuit(json_data: dict) -> tuple:
    component_data: list = json_data.get("components")
    r_t: float = calc_series_resistance(component_data)
    v_t: float = json_data.get("voltage")
    i_t: float = v_t / r_t
    circuit_stats = {
        "Total Resistance": str(round(r_t, PRECISION)) + " Ohms",
        "Total Voltage": str(round(v_t, PRECISION)) + " V",
        "Total Current": str(round(i_t, PRECISION)) + " A",
    }
    return circuit_stats, assign_resistor_properties(component_data, i_t, v_t)


def calc_series_resistance(components: list) -> float:
    resistance: float = 0
    resistance += sum(
        component.get("resistor").get("resistance")
        for component in get_components_of_type("Series", components)
    )
    for component in get_components_of_type("Parallel", components):
        resistance += calc_parallel_resistance(component.get("branches"))
    return resistance


def calc_parallel_resistance(branches: list) -> float:
    resistance: float = 0
    individual_resistances: list = []
    for resistor in branches:
        individual_resistances.append(
            resistor.get("resistance")
            if not isinstance(resistor, list)
            else calc_series_resistance(resistor)
        )
    resistance = sum(1 / r for r in individual_resistances) ** -1
    return resistance


def create_resistor(
    resistance: float, current: float, voltage: float, power: float
) -> dict:
    new_resistor: dict = {}
    new_resistor.setdefault("resistance", str(round(resistance, PRECISION)) + " Ohms")
    new_resistor.setdefault("current", str(round(current, PRECISION)) + " A")
    new_resistor.setdefault("voltage", str(round(voltage, PRECISION)) + " V")
    new_resistor.setdefault("power", str(round(power, PRECISION)) + " W")
    return new_resistor


def assign_resistor_properties(components: list, current, voltage) -> dict:
    resistor_data: dict = {}
    remaining_voltage = voltage
    for component in components:
        if "branches" not in component:
            resistor = component.get("resistor")
            resistance: float = resistor.get("resistance")
            resistor_data.setdefault(resistor.get("name"), {})
            voltage = current * resistance
            power = current * voltage
            remaining_voltage -= voltage
            resistor_data[resistor.get("name")] = create_resistor(
                resistance, current, voltage, power
            )
        else:
            branches: list = component.get("branches")
            for branch in branches:
                if isinstance(branch, list):
                    equiv_r = calc_series_resistance(branch)
                    resistor_data = resistor_data | assign_resistor_properties(
                        branch, remaining_voltage / equiv_r, remaining_voltage
                    )
                    break
                resistance: float = branch.get("resistance")
                resistor_data.setdefault(branch.get("name"), {})
                branch_current = remaining_voltage / resistance
                branch_voltage = remaining_voltage
                power = branch_current * branch_voltage
                resistor_data[branch.get("name")] = create_resistor(
                    resistance, branch_current, branch_voltage, power
                )
    return resistor_data
