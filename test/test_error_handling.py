import pytest
import os
import tempfile
from src.csv_handler.csv_handler_builtin import CSVHandler
from src.utils.general import validate_col_names
from test.config import MOCK_CSV
from main import CLI



@pytest.fixture
def tmp_csv_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.csv")
        with open(path, "w") as f:
            f.write(MOCK_CSV)
        yield path, tmpdir

# -----------------------------
# Test Cases
# -----------------------------


#Ensures that the system rejects Input CSV files whose column headers do not match the expected schema
def test_invalid_headers(tmp_csv_file):
    path, _ = tmp_csv_file
    wrong_csv = MOCK_CSV.replace("user_id", "bad_id")
    with open(path, "w") as f:
        f.write(wrong_csv)
    handler = CSVHandler()
    with pytest.raises(ValueError, match="headers do not match expected headers"):
        handler.read(path)

#verifies that users cannot request output columns that don’t exist in the input schema.
def test_invalid_output_columns():
    with pytest.raises(ValueError, match="not in INPUT_HEADERS"):
        validate_col_names(["nonexistent_col"])

#checks that a CSV file must contain actual data, not just headers
def test_empty_csv_raises(tmp_csv_file):
    path, _ = tmp_csv_file
    with open(path, "w") as f:
        f.write("user_id,manager_id,name,email_address,start_date,last_login\n")
    handler = CSVHandler()
    with pytest.raises(ValueError, match="contains no data rows"):
        handler.read(path)

#ensures that the CLI rejects unknown or unsupported transformation instructions
def test_invalid_cli_transformation(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--transf", "NO_VALID_TRANSFORMER:user_id"])
    with pytest.raises(ValueError, match="Unknown transformation type"):
        CLI()


#checks that only files with a .csv extension are accepted as input.
def test_non_csv_input_raises(tmp_csv_file):
    path, _ = tmp_csv_file

    non_csv_path = path.replace(".csv", ".txt") ## Rename the file to a non-CSV extension
    os.rename(path, non_csv_path)

    handler = CSVHandler()

    with pytest.raises(ValueError, match="must be a CSV file"):
        handler.read(non_csv_path)
