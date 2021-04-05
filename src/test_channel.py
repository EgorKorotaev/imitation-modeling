from channel import Channel
from packet import Packet
from range import Range
from node import Node
from src.buffer import Buffer


def test_channel_business():
    node = Node(channels=[], buffer=Buffer(capacity=10))
    channel = Channel(range=Range(2, 2), receiver=node)
    assert channel.is_free() is True

    channel.send_packet(Packet(id=42))
    assert channel.is_free() is False

    channel.on_clock_tick()
    assert channel.is_free() is False

    channel.on_clock_tick()
    assert channel.is_free() is True


def test_packet_delivered():
    # given
    node = Node(channels=[], buffer=Buffer(capacity=10))
    channel = Channel(range=Range(2, 2), receiver=node)

    # when
    channel.send_packet(Packet(id=42))
    channel.on_clock_tick()
    channel.on_clock_tick()

    # then
    assert channel.is_free()
    assert len(channel.receiver.buffer) == 1
    assert channel.receiver.buffer.pop().id == 42
