

from src.transformations.abstract_transformation import Transformation
from src.utils.logging_handler import logging_handler
from typing import Any, Union, List, Dict
import uuid

"""
Converts UUIDs UUID strings to unique integers while maintaining uniqueness
Example:
        "550e8400-e29b-41d4-a716-446655440000" -> 1
        "123e4567-e89b-12d3-a456-426614174000" -> 2
        "550e8400-e29b-41d4-a716-446655440000" -> 1  # same UUID as before
"""

class UUIDMapper(Transformation):
    def __init__(self, column_name: str) -> None:
        super().__init__(column_name)
        self.uuid_map   = {}              # store mapping of UUID -> int
        self.counter    = 1

    @logging_handler.catch
    @logging_handler.log
    def apply(self, data: Union[List[Dict[str, Any]], Any] ) -> Union[List[Dict[str, Any]], Any]:

        if isinstance(data, list): # builtin backend
            for row in data:
                row[self.column_name] = self._map_uuid(row[self.column_name])
        else:
            pass    #apply here the logic for Pandas/PySpark Backend
        return data

    def _map_uuid(self, uuid_str: Any) -> int:

        """
        Map a UUID string to a unique integer.
        If the value is not a valid UUID, return the value
        """
        try:
            # Validate if value is a UUID
            uuid_obj = uuid.UUID(str(uuid_str))
        except (ValueError, TypeError):
            return "not a valid UUID"

        """
        use a dict to store UUIDs we've already seen.
        Each UUID is a key, and its assigned integer is the value.
        When a UUID appears again, we just look it up in the dict
        to return the same integer instead of assigning a new one
        """
        if uuid_str not in self.uuid_map:
            self.uuid_map[uuid_str] = self.counter
            self.counter += 1
        return self.uuid_map[uuid_str]


