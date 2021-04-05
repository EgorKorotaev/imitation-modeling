from abc import ABC, abstractmethod


class SimulationUnit(ABC):

    @abstractmethod
    def on_clock_tick(self):
        pass
