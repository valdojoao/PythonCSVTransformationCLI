
from config import METADATA

INPUT_HEADERS = METADATA.get("input_headers", [])

def validate_col_names(output_columns) -> None:
    # Check that columns exist in INPUT_HEADERS (provided dataset)
    invalid_columns = [col for col in output_columns if col not in INPUT_HEADERS]
    if invalid_columns:
        raise ValueError(
            f"The following output_columns are not in INPUT_HEADERS: {invalid_columns}\n"
            f"Valid headers: {INPUT_HEADERS}"
        )