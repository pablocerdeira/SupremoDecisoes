# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import importLibraries

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


## Global variables and objects
# conn: MySQL connection
# cur:  MySQL cursor
# rows: MySQL resultset


########################
### PROGRAM SETTINGS ###
########################

# Debug level
#  - Debug = 0: no debug
#  - Debug = 1: return basic information
#  - Debug = 2: return detailed information
debug = 2

# MySQL settings
MySQLhost =     '172.16.4.51'
MySQLusername = 'pablocerdeira'
MySQLpasswd =   'pablo123'
MySQLdb =       'fredericodba'

# Rows limit when reading/writing from/to MySQL
MySQLLimit =    'limit 0,1000'

# Analysis tables
# We are going to adopt some table prefixies
#  - t: table
#  - a: analysis
#  - vw: view
#  - rep: view saved as table (reports)

# Main table
# Define table name, source table and table indexes (idx)
ta_main =               "ta_main"
ta_main_source =        'monocraticas'
ta_main_idx =           ['num_processo','ministro']


# Table: Analysis Words All
# Define table name, table columns and table indexes (idx)
ta_words_all =          "ta_words_all"           
ta_word_all_columns =   ['id int not null auto_increment',
                        'id_monocratica int null',
                        'word varchar(255) null',
                        'word_count int null'
                        ]
ta_words_all_idx =      ['id_monocratica','word','word_count']

# Export plain texts decisions saving it to disk
exporToDisk = False
exportFolder = '/home/pablocerdeira/corpora/decisoes_supremo/'

# Steps to run or ignore
connectDB =         True
dropTables =        True
createTables =      True
createIndex =       True
populateTables =    True
addHash =           True
convertRTF2text =   True

########################
##### END SETTINGS #####
########################

# Main function
def main():
    
    if connectDB == True:
        connMySQL()                                     # Connect to MySQL
    
    if dropTables == True:
        dropTable(ta_main)                              # Drop table ta_main
        dropTable(ta_words_all)                         # Drop table ta_words_all
    
    if createTables == True:
        
        # Create ta_main table
        createTableFrom(ta_main,ta_main_source)         # Create table ta_main based on monocraticas
        addPK(ta_main)                                  # Add primary key to ta_main
    
        # Create ta_word_all
        createTable(ta_word_all,ta_word_all_columns)
    
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
    getAll(ta_main,'where txt_conteudo is not null')

    # Add hashes to ta_main
    if addHash == True:
        addHashes(ta_main,'txt_conteudo')
    
    if convertRTF2text == True:
        addPlain(ta_main,'txt_conteudo','txt_text')

    #writeFiles()
    #createCorpora()
    #print decsCorp.concordance('consumidor')


if __name__ == "__main__":
    main()

