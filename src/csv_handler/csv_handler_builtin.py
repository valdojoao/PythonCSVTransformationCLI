

import csv
import os
from typing import List, Dict, Any
from src.csv_handler.abstract_tabular_data import TabularData
from config import METADATA
from datetime import datetime

INPUT_HEADERS = METADATA.get("input_headers", [])

#builtin CSV backend for the application.
class CSVHandler(TabularData):
    def read(self, path: str) -> List[Dict[str, Any]]:                      #Read CSV and return a list of dicts

        if not path.lower().endswith(".csv"):
            raise ValueError(f"Input file '{path}' must be a CSV file")

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            actual_headers = reader.fieldnames or []
            if actual_headers != INPUT_HEADERS:                             #csv file and config headers must be the same
                raise ValueError(
                    f"CSV file '{path}' headers do not match expected headers.\n"
                    f"Expected: {INPUT_HEADERS}\n"
                    f"Found:    {actual_headers}"
                )

            rows = [row for row in reader]

            if not rows:
                raise ValueError(f"CSV file '{path}' contains no data rows.")

            return rows

    # Write list of dicts to CSV in specified column order
    def write(self, path: str, data: List[Dict[str, Any]], columns_order: List[str]) -> None:
        # --- Generate filename with timestamp ---
        timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename    = f"output_{timestamp}.csv"
        path        = os.path.join(path, filename)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns_order)
            writer.writeheader()
            for row in data:
                writer.writerow({col: row.get(col, '') for col in columns_order})
