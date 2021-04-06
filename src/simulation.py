from buffer import Buffer
from node import Node

from channel import Channel
from packet import Packet
from range import Range


class Simulation:
    """
    Simulation of network:

      ______   ______
     /      \ /      \
    A        B        C
     \______/ \______/
    """

    def __init__(self, total_packets=500, reserved_system_threshold=20):
        self.total_packages = total_packets
        self.buffer_c = Buffer(capacity=total_packets)
        self.node_c = Node(channels=[], buffer=self.buffer_c)

        self.channel_b1c = Channel(range=Range(22, 28), receiver=self.node_c)
        self.channel_b2c = Channel(range=Range(25, 25), receiver=self.node_c)

        self.threshold_reached = False

        def callback():
            if not self.threshold_reached:
                self.channel_b1c.range = Range(15, 15)
                self.channel_b2c.range = Range(15, 15)
                self.threshold_reached = True

        self.buffer_b = Buffer(capacity=25, threshold=reserved_system_threshold, on_threshold_reached=callback)

        self.node_b1 = Node(channels=[self.channel_b1c], buffer=self.buffer_b)
        self.node_b2 = Node(channels=[self.channel_b2c], buffer=self.buffer_b)

        self.channel_ab1 = Channel(range=Range(20, 20), receiver=self.node_b1)
        self.channel_ab2 = Channel(range=Range(15, 25), receiver=self.node_b2)

        self.buffer_a = Buffer(capacity=20)

        self.node_a = Node(channels=[self.channel_ab1, self.channel_ab2], buffer=self.buffer_a)

        self.channel_emitter_a = Channel(range=Range(5, 15), receiver=self.node_a)

        self.buffer_emitter = Buffer(capacity=total_packets)

        self.packets_to_send = [Packet(i) for i in range(total_packets)]

        for packet in self.packets_to_send:
            self.buffer_emitter.push(packet)

        self.node_emitter = Node(channels=[self.channel_emitter_a], buffer=self.buffer_emitter)

        self.time_aware_units = [
            self.node_emitter,
            self.channel_emitter_a,

            self.node_a,
            self.channel_ab1,
            self.channel_ab2,

            self.node_b1,
            self.channel_b1c,

            self.node_b2,
            self.channel_b2c,

            self.node_c
        ]

        self.experiment_results = None

    def run_simulation(self):
        self.threshold_reached = False

        for tick in range(self.total_packages * 50 + 1):
            for unit in self.time_aware_units:
                unit.on_clock_tick()

        self.experiment_results = (self.threshold_reached, self.total_packages - len(self.buffer_c))
