from buffer import Buffer
from channel import Channel
from network import Network
from node import Node
from range import Range


def test_network():
    channel1 = Channel(range=Range(2, 2))
    channel2 = Channel(range=Range(3, 3))
    node_a = Node()
    node_b = Node(channels=[], buffer=Buffer(capacity=2, threshold=2))
    network = Network(initial_node=node_a)
