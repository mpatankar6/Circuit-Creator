from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    component_type: str
    name: str
    branch: int
    value: float


def read_circuit_data() -> list(Component):
    pass
