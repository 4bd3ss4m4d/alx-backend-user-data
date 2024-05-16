#!/usr/bin/env python3
"""
Main file for the project
"""

hsh_psswd = __import__('encrypt_password').hash_password

password = "MyAmazingPassw0rd"
print(hsh_psswd(password))
print(hsh_psswd(password))
