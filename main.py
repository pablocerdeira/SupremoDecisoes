# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs
import settings as st

# Utils functions
from utils import *

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
createWordFreq =    True


## Global variables and objects
global cur, conn
global rows, totalRows


# Main function
def main():
    
    if connectDB == True:
        connMySQL()                                        # Connect to MySQL
    
    if dropTables == True:
        dropTable(st.ta_main)                              # Drop table ta_main
        dropTable(st.ta_words_all)                         # Drop table ta_words_all
    
    if createTables == True:    
        # Create ta_main table
        createTableFrom(st.ta_main,st.ta_main_source)      # Create table ta_main based on monocraticas
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
    # Used to create hashes and to convert RTF to txt
    getAll(st.ta_main,'where txt_conteudo is not null')

    # Add hashes to ta_main
    if addHash == True:
        addHashes(st.ta_main,'txt_conteudo')
        addIndex(st.ta_main,'hash_txt_conteudo')
    
    if convertRTF2text == True:
        addPlain(st.ta_main,'txt_conteudo','txt_text')

    # Get data from ta_main and save it to rows
    # Used to create word frequencies
    getAll(st.ta_main,'where txt_text is not null')

    if createWordFreq == True:
        for row in rows:
            word_frequencies = wordFrequence(row['txt_text'])
            for word in word_frequencies:
                print row['id'], word, word_frequencies[word]


    #writeFiles()
    #createCorpora()
    #print decsCorp.concordance('consumidor')


if __name__ == "__main__":
    main()

