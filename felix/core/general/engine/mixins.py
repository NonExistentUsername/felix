import time
from abc import abstractmethod

from .interfaces import IEngine

class EngineRunMixin(IEngine):
    def __init__(self, tickrate: int) -> None:
        super().__init__()
        self.__tickrate: int = tickrate
        # interval in secs
        self.__interval: float = 1 / tickrate
        self.__stop_engine: bool = False
    
    @property
    def tickrate(self) -> int:
        return self.__tickrate

    def stop(self) -> None:
        self.__stop_engine = True

    def run(self) -> None:
        last_update: float = time.time()
        interval_delta: float = 0
        while not self.__stop_engine:
            time.sleep(max(0, self.__interval - interval_delta))
            
            cur_time: float = time.time()
            time_delta: float = cur_time - last_update
            
            self.update_state(time_delta)

            last_update = cur_time
            interval_delta: float = time.time() - cur_time


    @abstractmethod
    def update_state(self, time_delta: float) -> None:
        pass