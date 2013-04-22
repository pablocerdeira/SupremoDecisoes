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
decsPerYearClass =  True
decsPerJustice =    True
decsPerJusticeClass = True
decsPerJusticeYear = True
decsPerYearJustice = True

topWords =          True


# Main function
def main():
    
    if connectDB == True:
        SQL.connMySQL()                                        # Connect to MySQL

    # Load MySQL resultset into Pandas dataframe
    if load2Pandas == True:
        sql = 'select * from tmp'
        df = SQL.MySQL2Pandas(sql)

    # Report: decisions por year
    if decsPerYear == True:
        grouped = df.groupby(df['dat_criacao'].map(lambda x: x.year)).id_ta_main.nunique()
        print grouped

    # Report: decisions por class
    if decsPerClass == True:
        grouped = df.groupby('sig_classe_proces').id_ta_main.nunique()
        print grouped

    # Report: decisions por year per class
    if decsPerYearClass == True:
        grouped = df.groupby([df['dat_criacao'].map(lambda x: x.year),'sig_classe_proces']).id_ta_main.nunique()
        print grouped

    # Report: decisions por justice
    if decsPerJustice == True:
        grouped = df.groupby('nom_ministro').id_ta_main.nunique()
        print grouped

    if decsPerJusticeClass == True:
        grouped = df.groupby(['nom_ministro','sig_classe_proces']).id_ta_main.nunique()
        print grouped

    if decsPerJusticeYear == True:
        grouped = df.groupby(['nom_ministro',df['dat_criacao'].map(lambda x: x.year)]).id_ta_main.nunique()
        print grouped

    if decsPerYearJustice == True:
        grouped = df.groupby([df['dat_criacao'].map(lambda x: x.year),'nom_ministro']).id_ta_main.nunique()
        print grouped

    if topWords == True:
        grouped = df.groupby(['word']).id_ta_main.nunique()
        print grouped

if __name__ == "__main__":
    main()

