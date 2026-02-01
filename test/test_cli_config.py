import pytest
from main import CLI
import tempfile
import os
from test.config import MOCK_CSV

@pytest.fixture
def tmp_csv_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.csv")
        with open(path, "w") as f:
            f.write(MOCK_CSV)
        yield path, tmpdir


#If the user tells the program what to do via CLI flags, the program must ignore the config defaults.
def test_cli_args_override_config(monkeypatch, tmp_csv_file):
    path, tmpdir = tmp_csv_file
    monkeypatch.setattr("sys.argv", ["main.py", "--input", path, "--output", tmpdir, "--backend", "builtin"])
    cli = CLI()
    assert cli.input_file == path
    assert cli.output_file == tmpdir
    assert cli.backend.__class__.__name__ == "CSVHandler"


#If the user doesn’t specify anything, the program should rely entirely on its configuration defaults.
def test_cli_defaults_to_config(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py"])
    cli = CLI()
    assert cli.input_file == "./data_input/user_sample.csv"
    assert cli.output_file == "./data_output/"
    assert cli.backend.__class__.__name__ == "CSVHandler"
