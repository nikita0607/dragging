from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    def draw(self):
        pass
