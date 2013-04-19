# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs
import settings as st

# MySQL tools used by this software
from MySQLtools import *
# Functions by MySQLtools
#  - connMySQL()
#  - dropTable(table)
#  - createTableFrom(table,sourceTable)
#  - createTable(table,columns)
#  - addPK(table)
#  - addIndex(table,column)
#  - populateTableFrom(table,sourceTable)
#  - getAll(table,where)
#  - addHashes(table,sourceColumn)
#  - addPlain(table,sourceColumn,destColumn)

# Steps to run or ignore
connectDB =         True
dropTables =        True
createTables =      True
createIndex =       True
populateTables =    True
addHash =           True
convertRTF2text =   True


## Global variables and objects
# conn: MySQL connection
# cur:  MySQL cursor
# rows: MySQL resultset

# Main function
def main():
    
    if connectDB == True:
        connMySQL()                                     # Connect to MySQL
    
    if dropTables == True:
        dropTable(st.ta_main)                              # Drop table ta_main
        dropTable(st.ta_words_all)                         # Drop table ta_words_all
    
    if createTables == True:
        
        # Create ta_main table
        createTableFrom(st.ta_main,st.ta_main_source)         # Create table ta_main based on monocraticas
        addPK(st.ta_main)                                  # Add primary key to ta_main
    
        # Create ta_word_all
        createTable(st.ta_words_all,st.ta_words_all_columns)
    
    if createIndex == True:
        
        # Index ta_main
        for column in st.ta_main_idx:
            addIndex(st.ta_main,column)                    # Indexing columns on ta_main

        # Index ta_word_all
        for column in st.ta_words_all_idx:
            addIndex(st.ta_words_all,column)               # Indexing columns on ta_word_all

    if populateTables == True:
        
        # Populate ta_main
        populateTableFrom(st.ta_main,st.ta_main_source)
        
    # Get data from ta_main and save it to rows
    getAll(st.ta_main,'where txt_conteudo is not null')

    # Add hashes to ta_main
    if addHash == True:
        addHashes(st.ta_main,'txt_conteudo')
    
    if convertRTF2text == True:
        addPlain(st.ta_main,'txt_conteudo','txt_text')

    #writeFiles()
    #createCorpora()
    #print decsCorp.concordance('consumidor')


if __name__ == "__main__":
    main()

