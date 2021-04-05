from dataclasses import dataclass
from collections import deque
from typing import Callable

from packet import Packet


class BufferOverflow(Exception):
    pass


@dataclass
class Buffer:
    capacity: int
    threshold: int

    def __init__(self, capacity: int, threshold: int = 0, on_threshold_reached: Callable = None):
        self._queue = deque()
        self._on_threshold_reached = on_threshold_reached
        self.capacity = capacity
        self.threshold = threshold

    def __len__(self) -> int:
        return len(self._queue)

    def push(self, packet: Packet):
        if len(self) == self.capacity:
            raise BufferOverflow

        self._queue.appendleft(packet)

        if self._on_threshold_reached is not None and len(self) == self.threshold:
            self._on_threshold_reached()

    def pop(self) -> Packet:
        return self._queue.pop()
