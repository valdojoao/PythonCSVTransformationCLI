


from typing import Any, Union, List, Dict
from src.transformations.abstract_transformation import Transformation
from src.utils.logging_handler import logging_handler
import random
import string

"""
Redacts sensitive data by replacing it with random characters that look similar.
For example, it can transform alice@example.com into G7kLp2xFjR9bT3hVq0, 
while keeping the same length (17 characters) to preserve  structure of original data
"""
class InfoRedactor(Transformation):
    def __init__(self, column_name: str):
        super().__init__(column_name)

    @logging_handler.catch
    @logging_handler.log
    def apply(self, data: Union[List[Dict[str, Any]], Any]) -> Union[List[Dict[str, Any]], Any]:

        if isinstance(data, list): # builtin backend
            for row in data:
                if self.column_name in row:
                    row[self.column_name] = self._redact(row[self.column_name])
        else:
            pass    #apply here the logic for Pandas/PySpark Backend
        return data

    # Replace value with random characters of the same length
    def _redact(self, value: Any) -> str:

        if not value:
            return value
        length = len(str(value))
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


