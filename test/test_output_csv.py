import os
import csv
import pytest
from src.csv_handler.csv_handler_builtin import CSVHandler
from test.config import SAMPLE_DATA

@pytest.fixture
def csv_handler():
    return CSVHandler()


@pytest.fixture
def sample_data():
    return SAMPLE_DATA


def test_output_file_is_csv(csv_handler, sample_data, tmp_path):
    csv_handler.write(tmp_path, sample_data, columns_order=["user_id", "manager_id", "name"])
    files = os.listdir(tmp_path)
    csv_files = [f for f in files if f.endswith(".csv")]
    assert csv_files
    output_file = os.path.join(tmp_path, csv_files[0])
    with open(output_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
    assert headers == ["user_id", "manager_id", "name"]

def test_output_column_order_respected(csv_handler, sample_data, tmp_path):
    desired_order = ["manager_id", "email_address", "user_id"]
    csv_handler.write(tmp_path, sample_data, columns_order=desired_order)
    csv_files = [f for f in os.listdir(tmp_path) if f.endswith(".csv")]
    assert csv_files
    output_file = os.path.join(tmp_path, csv_files[0])
    with open(output_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
    assert headers == desired_order
