from dataclasses import dataclass
from typing import List

from buffer import Buffer, BufferOverflow
from packet import Packet
from simulation_unit import SimulationUnit
from channel import Channel


@dataclass
class Node(SimulationUnit):
    channels: List[Channel]
    buffer: Buffer

    def on_clock_tick(self):
        self._push_to_channels()

    def packet_received(self, packet: Packet):
        try:
            self.buffer.push(packet)
        except BufferOverflow:
            pass  # TODO process delivery failure
        self._push_to_channels()

    def _push_to_channels(self):
        while len(self.buffer) > 0:
            channel = self._get_free_channel()
            if channel is not None:
                channel.send_packet(self.buffer.pop())
            else:
                break

    def _get_free_channel(self):
        for channel in self.channels:
            if channel.is_free():
                return channel
