#!/usr/bin/env python3
'''Adds the Modules directory to python sys path'''
import sys
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
# print('path:'+dir_path)
project_modules_path = os.path.join(dir_path, 'Modules')

sys.path.append(project_modules_path)
print(f'{project_modules_path} added to sys.path')
