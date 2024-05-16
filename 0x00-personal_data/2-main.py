#!/usr/bin/env python3

'''
This module contains the following:
- get_logger
- PII_FIELDS
- filter_datum
- get_filtered_logger
- RedactingFormatter
- main
'''

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))
