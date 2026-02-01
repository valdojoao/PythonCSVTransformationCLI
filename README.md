# Python CSV Transformation CLI

## Project Overview
This project is a Python command-line application that transforms an input CSV into a new CSV 
with optional transformations applied per column.

- Input CSV: first row = headers, remaining rows = data
- Output CSV: may have different column order and transformed values
- Transformations supported: UUID mapping, info redaction, timestamp formatting
  - **UUIDMapper**      : Converts UUIDs to sequential integers, preserving uniqueness  
  - **InfoRedactor**    : Anonymizes sensitive fields with random, length-preserving data  
  - **DateFormatter**   : Converts timestamps to YYYY-MM-DD format  

---

## Design Choices

- Object-Oriented Approach: each transformation is a class (polymorphism, modular, extendable)  
- Assumptions: Since it was not specified, I assume the provided input.csv is already clean. Therefore, the data was not inspected for missing values, duplicate removal, normalization, or other preprocessing steps.  
- Scalability: The project was developed using Python built-in tools for CSV manipulations. For larger datasets (e.g., ~1 million rows), it would be necessary to use more appropriate tools like Pandas. For even larger datasets, a more robust solution such as Spark is recommended.
The code is already structured to support Pandas or Spark: it is enough to implement the reading and writing operations in csv_handler_pandas.py or csv_handler_pyspark.py and make minimal adjustments inside each transformation’s apply method (e.g., src/transformations/info_redactor.py, line 28).

---

## Code Structure

```
project_root/
├── data_input/
│   └── user_sample.csv                <-- Input CSV file
├── data_output/                       <-- Output folder; contains transformed CSV files
├── src/
│   ├── csv_handler/                   <-- CSV handling scripts (backend-specific)
│   │   ├── abstract_tabular_data.py
│   │   ├── csv_handler_builtin.py
│   │   ├── csv_handler_pandas.py
│   │   └── csv_handler_pyspark.py
│   ├── transformations/               <-- Transformation logic per column
│   │   ├── abstract_transformation.py
│   │   ├── info_redactor.py
│   │   ├── timestamp_to_date.py
│   │   └── uuid_mapper.py
│   ├── utils/                         <-- Utility functions
│   │   ├── general.py
│   │   └── logging_handler.py
│   └── processor.py
├── test/                              <-- Unit tests
│   ├── config.py
│   ├── test_cli_config.py
│   ├── test_error_handling.py
│   ├── test_output_csv.py
│   └── test_transformations.py
├── config.py                          <-- Default parameters
├── main.py                            <-- Application entry point
└── requirements.txt
```

---

## How it Works

### Data Flow Diagram:

Input CSV  =====> CSV Handler (builtin / pandas / spark) =====> (Transformations per column UUIDMapper, InfoRedactor, DateFormatter) ====> Output CSV


## CLI Arguments

| Argument       | Description                                                | Example / Notes                           |
|----------------|------------------------------------------------------------|-------------------------------------------|
| `--input`      | Path to input CSV file                                     | `--input ./data_input/user_sample.csv`    |
| `--output`     | Path to output CSV file                                    | `--output ./data_output/`                 |
| `--backend`    | Backend for CSV processing                                  | Choices: `builtin`, `pandas`, `spark`    |
| `--columns`    | Output column order (space-separated)                     | `--columns user_id email last_login`      |
| `--transf`     | Column transformations in format `type:column_name`       | `--transf UUIDMapper:user_id InfoRedactor:email_address` |

---

## Example Usage

**CLI command:**

```
python .\main.py --input .\data_input\user_sample.csv --output .\data_output\ --columns manager_id email_address start_date last_login user_id --transf UUIDMapper:user_id InfoRedactor:email_address DateFormatter:last_login --backend builtin
```

**Input CSV (`user_sample.csv`):**

```
user_id,manager_id,name,email_address,start_date,last_login
EFEABEA5-981B-4E45-8F13-425C456BF7F6,CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,Ashley Hernandez,ashley.hernandez@live.com,2025-Mar-01,2025-03-23 16:54:43 CET
2AB96C22-181C-42DC-8B11-3EDAA281D4F8,A37D98B9-98E7-43ED-9B27-A79EFDDAC033,Lisa Nelson,lisa.nelson@outlook.com,2021-Feb-17,2025-02-27 16:35:22 CET
0213F1C0-01D9-422C-8737-19FBFA902082,4828D9F6-5959-4646-92AD-8A8AD49ABE4A,Amanda Roberts,amanda.roberts@live.com,2020-Jun-19,2025-03-07 17:29:50 CET
4828D9F6-5959-4646-92AD-8A8AD49ABE4A,A37D98B9-98E7-43ED-9B27-A79EFDDAC033,Jennifer Rodriguez,jennifer.rodriguez@protonmail.com,2021-Oct-01,2025-02-14 03:48:32 CET
```

**Output CSV (`output_timestamp.csv`):**

```
manager_id,email_address,start_date,last_login,user_id
CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,hduA3CyJvmwjhSwreBdD0LEWt,2025-Mar-01,2025-03-23,1
A37D98B9-98E7-43ED-9B27-A79EFDDAC033,4YoyBLdZjfTH5yFNZNfLlQ5,2021-Feb-17,2025-02-27,2
4828D9F6-5959-4646-92AD-8A8AD49ABE4A,ElCJazhqM9QO1fk3wdBD4pv,2020-Jun-19,2025-03-07,3
A37D98B9-98E7-43ED-9B27-A79EFDDAC033,nKgf5ibctyovSw7RMb4juE0t80jtvLe3M,2021-Oct-01,2025-02-14,4
```

---

## Tests
All tests are in the `test/` folder  
- **test_cli_args_override_config (test_cli.py):** Verifies CLI arguments override config defaults  
- **test_cli_defaults_to_config (test_cli.py):** Verifies CLI uses config defaults when no arguments are provided  
- **test_invalid_headers (test_csv_handler.py):** Rejects CSV files with incorrect headers  
- **test_invalid_output_columns (test_csv_handler.py):** Rejects output column names not present in input  
- **test_empty_csv_raises (test_csv_handler.py):** Rejects CSV files with no data rows  
- **test_invalid_cli_transformation (test_csv_handler.py):** CLI rejects unknown/unsupported transformation types  
- **test_non_csv_input_raises (test_csv_handler.py):** Rejects files that don’t have .csv extension  
- **test_output_file_is_csv (test_csv_write.py):** Writes CSV and checks output file exists and has .csv extension  
- **test_output_column_order_respected (test_csv_write.py):** Verifies that CSV output respects column order  
- **test_only_one_transformation_per_column (test_transformations.py):** Ensures only one transformation is applied per column; warns if multiple  
- **test_info_redactor (test_transformations.py):** Checks if InfoRedactor transformation properly anonymizes sensitive information  
- **test_date_formatter (test_transformations.py):** Tests that DateFormatter correctly standardizes dates into YYYY-MM-DD format  
- **test_uuid_mapper (test_transformations.py):** Tests that UUIDMapper correctly maps UUIDs to sequential integers and handles invalid UUIDs  


Run tests:

```
pytest ./test/
```

---

## Dependencies

- Python 3.12  
- Windows 11 (built and tested on)  
- Install the dependencies using the following command: pip install -r requirements.txt 


---

## AI Disclosure

AI tools were used to:  
- Enforce type hints eg. def read(self, path **: str) -> List[Dict[str, Any]]:**   
- Double check my time and space complexity assumptions  
- Check that all specified requirements are covered by the test units. 
- Review and polish this README


---

