from buffer import Buffer, BufferOverflow
from packet import Packet


def test_empty_buffer():
    buffer = Buffer(capacity=2)
    assert len(buffer) == 0


def test_buffer_size():
    buffer = Buffer(capacity=3)
    buffer.push(Packet(1))
    assert len(buffer) == 1

    buffer.push(Packet(2))
    assert len(buffer) == 2

    assert buffer.pop() == Packet(1)
    assert len(buffer) == 1

    assert buffer.pop() == Packet(2)
    assert len(buffer) == 0


def test_buffer_overflow():
    buffer = Buffer(capacity=2)
    buffer.push(Packet(1))
    buffer.push(Packet(2))

    try:
        buffer.push(Packet(3))
    except BufferOverflow:
        assert len(buffer) == 2
    else:
        assert False


def test_threshold_reached():
    called = False

    def callback():
        nonlocal called
        called = True

    buffer = Buffer(capacity=2, threshold=1, on_threshold_reached=callback)
    buffer.push(Packet(1))

    assert called is True
