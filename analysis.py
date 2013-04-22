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
decsPerJustice =    True

# Main function
def main():
    
    if connectDB == True:
        SQL.connMySQL()                                        # Connect to MySQL

    if load2Pandas == True:
        sql = 'select * from tmp'
        df = SQL.MySQL2Pandas(sql)

    if decsPerJustice == True:
        grouped = df.groupby('nom_ministro').id_ta_main.nunique()
        print grouped

if __name__ == "__main__":
    main()

