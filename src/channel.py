import random
from dataclasses import dataclass

from packet import Packet
from range import Range
from simulation_unit import SimulationUnit


@dataclass
class Channel(SimulationUnit):
    range: Range

    def __init__(self, range: Range, receiver):
        self.range = range
        self.receiver = receiver
        self._packet = None
        self._ticks_left_before_sent = 0

    def on_clock_tick(self):
        if self._packet is not None:
            self._ticks_left_before_sent -= 1
            if self._ticks_left_before_sent == 0:
                self.receiver.packet_received(self._packet)
                self._packet = None

    def is_free(self) -> bool:
        return self._packet is None

    def send_packet(self, packet: Packet):
        if self._packet is None:
            self._packet = packet
            self._ticks_left_before_sent = self._generate_latency()

    def _generate_latency(self) -> int:
        return random.randint(self.range.start, self.range.end)
