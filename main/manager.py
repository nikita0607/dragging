from main import Main
from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    def start(self, main: Main):
        pass

    @abstractmethod
    def draw(self, win):
        pass

    @abstractmethod
    def update(self, main: Main):
        pass
