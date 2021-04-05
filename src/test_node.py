from channel import Channel
from node import Node
from buffer import Buffer
from packet import Packet
from range import Range


def test_create():
    buffer = Buffer(capacity=25)
    channel1 = Channel(range=Range(start=22, end=28), receiver=Node(channels=[], buffer=Buffer(capacity=10000)))
    node = Node(channels=[channel1], buffer=buffer)
    assert len(node.channels) is 1
    assert node.buffer is buffer


def test_packet_received():
    buffer = Buffer(capacity=2)
    node = Node(channels=[], buffer=buffer)
    packet = Packet(42)
    node.packet_received(packet)
    assert len(node.buffer) == 1
    result = node.buffer.pop()
    assert result.id == 42


def test_packet_sent_to_channel():
    buffer = Buffer(capacity=25)
    channel1 = Channel(range=Range(start=20, end=20), receiver=Node(channels=[], buffer=Buffer(capacity=10000)))
    node = Node(channels=[channel1], buffer=buffer)
    packet = Packet(42)
    node.packet_received(packet)
    node.on_clock_tick()
    assert channel1.is_free() is False


def test_packet_delivery_failed():
    buffer = Buffer(capacity=1)
    channel1 = Channel(range=Range(start=20, end=20), receiver=Node(channels=[], buffer=Buffer(capacity=10000)))
    node = Node(channels=[channel1], buffer=buffer)

    packet = Packet(42)
    node.packet_received(packet)
    node.on_clock_tick()
    assert channel1.is_free() is False

    packet = Packet(22)
    node.packet_received(packet)
    node.on_clock_tick()

    assert len(node.buffer) == 1
    assert channel1.is_free() is False

    packet = Packet(12)
    node.packet_received(packet)
    node.on_clock_tick()

    assert len(node.buffer) == 1
    assert channel1.is_free() is False
