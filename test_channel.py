from channel import Channel
from packet import Packet
from range import Range


def test_channel_business():
    channel = Channel(range=Range(2, 2))
    assert channel.is_free() is True

    channel.send_packet(Packet(id=42))
    assert channel.is_free() is False

    channel.on_clock_tick()
    assert channel.is_free() is False

    channel.on_clock_tick()
    assert channel.is_free() is True

def test_packet_delivered():
    channel = Channel(range=Range(2, 2))
    assert channel.recipient