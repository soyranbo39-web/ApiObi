from dataclasses import dataclass

VALID_ACTUATORS = {"riego", "ventilador"}
VALID_STATES    = {"ON", "OFF"}


@dataclass
class Actuator:
    name: str
    state: str = "OFF"
