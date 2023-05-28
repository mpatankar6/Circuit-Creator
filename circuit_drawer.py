import schemdraw
import schemdraw.elements as elements


def generate_drawing(json_data: str) -> str:
    with schemdraw.Drawing(show=False) as drawing:
        drawing.add(elements.Resistor().label("Ω"))
        # drawing.add_elements(*draw_element_list(json_data["components"]))
    raw_image_data: bytes = drawing.get_imagedata("svg")
    return str(raw_image_data).replace(r"\n", "\n")[2:-1]


def draw_element_list(components: list) -> list[elements.Element]:
    element_list: list = list()
    component: dict
    for component in components:
        if component.get("type") == "Series":
            element_list.append(
                elements.Resistor().label(get_resistor_label(component.get("resistor")))
            )
        elif component.get("type") == "Parallel":
            element_list.extend(draw_parallel_element(component.get("branches")))
            # element_list.append(elements.Resistor().color("red"))
        else:
            pass
    return element_list


def draw_parallel_element(branches: list) -> list:
    element_list: list = list()
    resistor: dict
    for resistor in branches:
        if isinstance(resistor, list):  # Element list as a branch
            element_list.extend(draw_element_list(resistor))
            break
        element_list.append(
            elements.Resistor().color("brown").label(get_resistor_label(resistor))
        )
    return element_list


def get_resistor_label(resistor: dict):
    return "Ω"
    # return f"{resistor.get('name')} {resistor.get('resistance')}"
