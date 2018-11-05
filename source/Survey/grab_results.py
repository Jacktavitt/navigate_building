'''
grab results from sqlite instance and organize into nice pages fro reviewing
'''

import os
import sys
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", required=True,
        help="databade file from sqlite3")

args = vars(parser.parse_args())

con = sqlite3.connect(args["database"])
curse = con.cursor()
results = list(curse.execute("SELECT * FROM survey_results"))
columns = list(curse.execute("PRAGMA table_info(survey_results)"))

with open("survey_resutls.txt", 'w') as sf:
    sf.write(str(columns)+'\n')
    for response in results:
        sf.write(str(response)+'\n')

    