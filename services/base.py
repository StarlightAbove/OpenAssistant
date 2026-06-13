from abc import ABC, abstractmethod


class BaseConnector(ABC):
    
    @abstractmethod
    def fetch(self) -> dict:
        """Fetch today's data and return as a dict."""
        pass

    def get_name(self) -> str:
        return self.__class__.__name__.lower().replace("connector", "")