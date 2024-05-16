#!/usr/bin/env python3

'''
This module contains the following:
- filter_datum
- RedactingFormatter
- get_logger
'''


filter_datum = __import__("filtered_logger").filter_datum

fields = ["password", "date_of_birth"]
messages = [
    "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;",
]

for msg in messages:
    print(filter_datum(fields, "xxx", msg, ";"))
