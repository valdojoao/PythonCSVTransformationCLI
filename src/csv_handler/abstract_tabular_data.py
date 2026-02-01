

from typing import Any, List
from abc import ABC, abstractmethod

# All backends (built-ins, pandas, pyspark) must implement this interface
class TabularData(ABC):
    @abstractmethod
    # Read CSV and return data in backend format
    def read(self, path: str) -> Any:
        pass

    @abstractmethod
    #Write data to CSV in the specified column order
    def write(self, path: str, data: Any, columns_order: List[str]) -> None:
        pass
