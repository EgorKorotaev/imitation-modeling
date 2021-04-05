from dataclasses import dataclass
from typing import List

from buffer import Buffer
from channel import Channel


@dataclass
class Node:
    channels: List[Channel]
    buffer: Buffer
