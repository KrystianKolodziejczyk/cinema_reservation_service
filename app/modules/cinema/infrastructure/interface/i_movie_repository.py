from abc import ABC, abstractmethod


class IMovieRepository(ABC):
    @abstractmethod
    async def fist(self):
        pass
