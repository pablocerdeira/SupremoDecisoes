# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs
import settings as st
import utils as ut
import MySQLtools as SQL

# Steps to run or ignore
### WARNING ###
### IMPORTANT ###
# If you are testing, please, CHANGE TABLE NAMES in settings.py!
# AGAIN: if you are testing, please, CHANGE TABLE NAMES in settings.py!
# And then, change the variables below to True

connectDB =         True
load2Pandas =       True
decsPerYear =       True
decsPerClass =      True
decsPerJustice =    True
decsPerJusticeClass = True

# Main function
def main():
    
    if connectDB == True:
        SQL.connMySQL()                                        # Connect to MySQL

    if load2Pandas == True:
        sql = 'select * from tmp'
        df = SQL.MySQL2Pandas(sql)

    if decsPerYear == True:
        grouped = df.groupby('dat_criacao'.split('-')[0]).id_ta_main.nunique()
        print grouped

    if decsPerClass == True:
        grouped = df.groupby('sig_classe_proces').id_ta_main.nunique()
        print grouped

    if decsPerJustice == True:
        grouped = df.groupby('nom_ministro').id_ta_main.nunique()
        print grouped

    if decsPerJusticeClass == True:
        grouped = df.groupby(['nom_ministro','sig_classe_proces']).id_ta_main.nunique()
        print grouped

if __name__ == "__main__":
    main()

