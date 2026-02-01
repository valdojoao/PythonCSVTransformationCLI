



from abc import ABC, abstractmethod

#Base class for all transformations, each transformation applies to a specific column.
class Transformation(ABC):
    def __init__(self, column_name: str) -> None:
        self.column_name = column_name

    @abstractmethod
    def apply(self, data):
        """
        Apply transformation to data.
        `data` can be:
            - list of dicts (built-ins)
            - Pandas DataFrame
            - Spark DataFrame
        Returns transformed data.
        """
        pass

