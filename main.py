# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs

# Importing settings and global vars
from settings import *

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


# Main function
def main():
    global cur, conn
    global rows, totalRows
    
    if connectDB == True:
        connMySQL()                                        # Connect to MySQL
    
    if dropTables == True:
        dropTable(ta_main)                              # Drop table ta_main
        dropTable(ta_words_all)                         # Drop table ta_words_all
    
    if createTables == True:    
        # Create ta_main table
        createTableFrom(ta_main,ta_main_source)      # Create table ta_main based on monocraticas
        addPK(ta_main)                                  # Add primary key to ta_main
    
        # Create ta_word_all
        createTable(ta_words_all,ta_words_all_columns)
    
    if createIndex == True:
        # Index ta_main
        for column in ta_main_idx:
            addIndex(ta_main,column)                    # Indexing columns on ta_main

        # Index ta_word_all
        for column in ta_words_all_idx:
            addIndex(ta_words_all,column)               # Indexing columns on ta_word_all

    if populateTables == True:   
        # Populate ta_main
        populateTableFrom(ta_main,ta_main_source)
        
    # Get data from ta_main and save it to rows
    # Used to create hashes and to convert RTF to txt
    getAll(ta_main,'where txt_conteudo is not null')

    # Add hashes to ta_main
    if addHash == True:
        addHashes(ta_main,'txt_conteudo')
        addIndex(ta_main,'hash_txt_conteudo')
    
    if convertRTF2text == True:
        addPlain(ta_main,'txt_conteudo','txt_text')

    # Get data from ta_main and save it to rows
    # Used to create word frequencies
    getAll(ta_main,'where txt_text is not null')

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

