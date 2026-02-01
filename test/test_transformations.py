
from src.transformations.info_redactor import InfoRedactor
from src.transformations.uuid_mapper import UUIDMapper
from src.transformations.timestamp_to_date import DateFormatter
import copy
from main import CLI
from unittest.mock import patch

# -----------------------------
# Test Cases
# -----------------------------

def test_info_redactor():

    sample_data = [
        {"email_address": "alice@example.com"},
        {"email_address": "bob123@test.org"},
        {"email_address": "charlie@domain.net"},
        {"email_address": ""},   # empty string
        {"email_address": None}, # None value
    ]

    original_data = copy.deepcopy(sample_data)

    redactor = InfoRedactor("email_address")
    transformed = redactor.apply(sample_data)

    for original, row in zip(original_data, transformed):
        val_original = original.get("email_address")
        val_transformed = row.get("email_address")

        # Empty or None should remain unchanged
        if not val_original:
            assert val_transformed == val_original
            continue

        # Length is preserved
        assert len(val_transformed) == len(val_original)

        # Value is actually changed
        assert val_transformed != val_original

        # Only contains letters or digits
        assert all(c.isalnum() for c in val_transformed)



def test_date_formatter():
    # Input data with different date/time formats and an invalid value
    input_data = [
        {"last_login": "2025-Mar-01"},                 # month as name
        {"last_login": "2025-03-23 16:54:43 CET"},     # timestamp with time and timezone
        {"last_login": "invalid"},                     # invalid date
        {"last_login": ""},                            # empty string
        {"last_login": None},                          # None value
    ]

    # Expected output after formatting
    expected_output = [
        {"last_login": "2025-03-01"},
        {"last_login": "2025-03-23"},
        {"last_login": "not a valid timestamp"},
        {"last_login": ""},                            # empty stays empty
        {"last_login": None},                          # None stays None
    ]

    formatter = DateFormatter("last_login")
    transformed = formatter.apply(input_data)

    # Assert the transformed data matches exactly what we expect
    assert transformed == expected_output




def test_uuid_mapper():
    # Input data includes both a valid UUID column and a non-UUID column
    input_data = [
        {"user_id": "550e8400-e29b-41d4-a716-446655440000", "last_login": "2025-03-23 16:54:43 CET"},
        {"user_id": "123e4567-e89b-12d3-a456-426614174000", "last_login": "2025-Mar-01"},
        {"user_id": "550e8400-e29b-41d4-a716-446655440000", "last_login": "invalid"},
    ]

    # Map the 'user_id' column
    user_id_mapper = UUIDMapper("user_id")
    transformed = user_id_mapper.apply(input_data)

    # Check uniqueness and sequential mapping for user_id
    user_ids = [row["user_id"] for row in transformed]
    assert len(set(user_ids)) == 2                   # two unique UUIDs in input
    assert set(user_ids) == {1, 2}                   # mapped to 1,2
    assert user_ids[0] == 1                          # first occurrence mapped to 1
    assert user_ids[2] == 1                          # repeated UUID maps to same integer

    # Check that non-UUID column 'last_login' is flagged as "not a valid UUID"
    mapper = UUIDMapper("last_login")
    transformed = mapper.apply(input_data)
    assert all(row["last_login"] == "not a valid UUID" for row in transformed)



def test_only_one_transformation_per_column(monkeypatch):
    test_args = [
        "main.py",
        "--input", "./data_input/user_sample.csv",
        "--output", "./data_output/",
        "--transf", "UUIDMapper:user_id", "InfoRedactor:user_id"
    ]
    with patch("sys.argv", test_args):
        warnings = []
        def fake_warning(msg):
            warnings.append(msg)
        from src.utils.logging_handler import logging_handler
        monkeypatch.setattr(logging_handler, "warning", fake_warning)
        cli = CLI()
        transformations = [t.column_name for t in cli.transformations]
        assert transformations.count("user_id") == 1
        assert any("Multiple transformations defined for column 'user_id'" in w for w in warnings)
