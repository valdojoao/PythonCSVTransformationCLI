


METADATA = {
              "input_file":     "./data_input/user_sample.csv",
              "output_file":    "./data_output/",
              "input_headers": [
                                  "user_id",
                                  "manager_id",
                                  "name",
                                  "email_address",
                                  "start_date",
                                  "last_login"
                                ],
              "output_headers": [
                                  "manager_id",
                                  "email_address",
                                  "start_date",
                                  "last_login",
                                  "user_id",
                                  "name"
                                ],
              "transformations":[
                                  { "type": "UUIDMapper", "column": "user_id" },
                                  { "type": "InfoRedactor", "column": "email_address" },
                                  { "type": "DateFormatter", "column": "last_login" }
              ],
              "backend": "builtin"
}


