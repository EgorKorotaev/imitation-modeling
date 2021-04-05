from dataclasses import dataclass


@dataclass
class Packet:
    id: int
    delivery_failed: bool

    def __init__(self, id: int):
        self.id = id
        self.delivery_failed = False

    def delivery_failed(self):
        self.delivery_failed = True
