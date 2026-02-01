


from src.utils.logging_handler import logging_handler
from src.utils.general import validate_col_names
from typing import Any, List, Optional

"""
-   This Class Handles CSV transformations from start to finish
-   It takes care of the entire process of transforming CSV data. 
-   It reads data from a chosen backend (builtin, Pandas, or PySpark), 
    then applies the transformations defined, and  writes the results to output CSV.
-   It validates columns, logs important actions, and handles errors
"""

class Processor:
    def __init__(self, data_backend: Any = None, transformations: Optional[List[Any]] = None, output_columns: Optional[List[str]] = None) -> None:

        self.data_backend   = data_backend     # tabularData interface, uses dependency injection for the CSV backend to support builtins, Pandas, or PySpark.
        self.transformations= transformations  # list of Transformation objects
        self.output_columns = output_columns   # final order of columns in output CSV

    @logging_handler.catch
    @logging_handler.log
    def process(self, input_path: str, output_path: str) -> None:
        validate_col_names(self.output_columns)
        data = self._read_csv(input_path)
        data = self._apply_transformations(data)
        self._write_csv(output_path, data)

    @logging_handler.catch
    @logging_handler.log
    def _read_csv(self, path: str) -> Any:
        return self.data_backend.read(path)

    @logging_handler.catch
    @logging_handler.log
    def _apply_transformations(self, data: Any) -> Any:
        for transform in self.transformations:
            data = transform.apply(data)
        return data

    @logging_handler.catch
    @logging_handler.log
    def _write_csv(self, path: str, data: Any) -> None:
        self.data_backend.write(path, data, self.output_columns)


