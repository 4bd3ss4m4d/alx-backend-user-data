#!/usr/bin/env python3

'''
Main file for the project
'''

hsh_pswd = __import__('encrypt_password').hash_password
is_vld = __import__('encrypt_password').is_valid

pswd = "MyAmazingPassw0rd"
encd_pswd = hsh_pswd(pswd)
print(encd_pswd)
print(is_vld(encd_pswd, pswd))
