import argparse
from typing import List, Any

from src.processor import Processor
from src.transformations.uuid_mapper import UUIDMapper
from src.transformations.info_redactor import InfoRedactor
from src.transformations.timestamp_to_date import DateFormatter

from src.csv_handler.csv_handler_builtin import CSVHandler
from src.csv_handler.csv_handler_pandas import PandasHandler
from src.csv_handler.csv_handler_pyspark import SparkHandler

from src.utils.general import validate_col_names
from src.utils.logging_handler import logging_handler
from config import METADATA

"""
-   This is the main entry point of the application.
-   It parses the arguments provided, chooses the right CSV backend (builtin, Pandas, or Spark), 
    sets up and validates any column transformations, and handles input/output files, 
    then it runs the Processor to apply the transformations. 
"""


class CLI:
    def __init__(self, ) -> None:

        self.config         = METADATA
        self.args           = self._parse_args()
        self.backend        = self._select_backend(self.args.backend or self.config.get("backend"))
        self.transformations= self._create_transformations()
        self.input_file     = self.args.input or self.config.get("input_file")
        self.output_file    = self.args.output or self.config.get("output_file")
        self.output_columns = self.args.columns or self.config.get("output_headers")

    def _parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Transform CSV files with configurable column transformations.")
        parser.add_argument("--input", help="Input CSV file path")
        parser.add_argument("--output", help="Output CSV file path")
        parser.add_argument("--backend", choices=["builtin", "pandas", "spark"], help="Backend to use for CSV processing")
        parser.add_argument("--columns", nargs="+", help="Output column order")
        parser.add_argument("--transf", nargs="+", help="List of column transformations in format type:column_name")
        return parser.parse_args()

    def _select_backend(self, backend_name: str) -> Any:
        if backend_name == "pandas":
            return PandasHandler()
        elif backend_name == "spark":
            return SparkHandler()
        else:
            return CSVHandler()

    def _create_transformations(self) -> List:
        transf_classes  = { "UUIDMapper": UUIDMapper, "InfoRedactor": InfoRedactor, "DateFormatter": DateFormatter }
        transformations = []
        seen_columns    = set()  # track columns already transformed

        # Use CLI args if provided, otherwise use JSON config
        transf_list = self.args.transf
        if not transf_list and self.config.get("transformations"):
            transf_list = [f"{t['type']}:{t['column']}" for t in self.config["transformations"]]

        for t in transf_list:
            try:
                type_name, column_name = t.split(":", 1)
            except ValueError:
                raise ValueError(f"Invalid transformation format: '{t}'. Expected type:column_name")

            validate_col_names([column_name])

            if column_name in seen_columns:
                logging_handler.warning(
                    f"WARNING: Multiple transformations defined for column '{column_name}'. Skipping '{type_name}'")
                continue

            seen_columns.add(column_name)

            cls = next((cls for key, cls in transf_classes.items() if key.lower() == type_name.lower()), None)
            if cls is None:
                raise ValueError(f"Unknown transformation type '{type_name}'")

            transformations.append(cls(column_name=column_name))

        return transformations

    def run(self) -> None:
        processor = Processor(
            data_backend=self.backend,
            transformations=self.transformations,
            output_columns=self.output_columns
        )
        processor.process(self.input_file, self.output_file)
        logging_handler.info(f"CSV transformation complete! Output saved to {self.output_file}")

if __name__ == "__main__":
    cli = CLI()
    cli.run()