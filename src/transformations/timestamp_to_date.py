
# Converts timestamp columns to YYYY-MM-DD format.

from typing import Any, Union, List, Dict
from src.transformations.abstract_transformation import Transformation
from dateutil import parser
from src.utils.logging_handler import logging_handler

"""
Converts timestamp or date values into a standard YYYY-MM-DD format
For example: "2025-Mar-01" → "2025-03-01" or "2025-03-23 16:54:43 CET" → "2025-03-23"
Invalid or unrecognized values are replaced with "not a valid timestamp"
"""

class DateFormatter(Transformation):
    def __init__(self, column_name: str) -> None:
        super().__init__(column_name)

    @logging_handler.catch
    @logging_handler.log
    def apply(self, data: Union[List[Dict[str, Any]], Any]) -> Union[List[Dict[str, Any]], Any]:
        if isinstance(data, list): # builtin backend
            for row in data:
                row[self.column_name] = self._format_date(row[self.column_name])
        else:
            pass    #apply here the logic for Pandas/PySpark Backend
        return data


    def _format_date(self, value: Any) -> str:
        """Convert ANY recognizable date format to YYYY-MM-DD"""
        if not value:
            return value

        try:
            dt = parser.parse(str(value), ignoretz=True)
            return dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return "not a valid timestamp"


