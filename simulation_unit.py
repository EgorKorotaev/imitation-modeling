from abc import ABC, abstractmethod


class SimulationUnit(ABC):

    @abstractmethod
    def on_clock_tick(self, ticks: int = 1):
        pass
