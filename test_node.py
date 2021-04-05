from channel import Channel
from node import Node
from buffer import Buffer
from packet import Packet
from range import Range


def test_create():
    buffer = Buffer(capacity=25, threshold=20)
    channel1 = Channel(range=Range(start=22, end=28))
    node = Node(channels=[channel1], buffer=buffer)
    assert len(node.channels) is 1
    assert node.channels[0] == Channel(Range(22, 28))
    assert node.buffer is buffer


def test_packet_received():
    buffer = Buffer(capacity=2, threshold=2)
    node = Node(channels=[], buffer=buffer)
    packet = Packet(42)
    node.packet_received(packet)
    assert len(node.buffer) == 1
    assert node.buffer.first() == Packet(42)
