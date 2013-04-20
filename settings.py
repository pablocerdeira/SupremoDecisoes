# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
MySQLLimit =    'limit 0,100'

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
ta_main_idx =           ['seq_objeto_incidente_principal',
                         'sig_classe_proces',
                         'num_processo',
                         'dat_autuacao',
                         'tip_julgamento',
                         'nom_ministro',
                         'dat_sessao',
                         'dat_criacao',
                         'dsc_tipo'
                         ]


# Table: Analysis Words All
# Define table name, table columns and table indexes (idx)
ta_words_all =          "ta_words_freq"           
ta_words_all_columns =  ['id int not null',
                         'id_monocratica int null',
                         'word varchar(255) null',
                         'word_count int null',
                         'primary key (id)'
                         ]
ta_words_all_idx =       ['id_monocratica','word','word_count']

# Export plain texts decisions saving it to disk
exporToDisk = False
exportFolder = '/home/pablocerdeira/corpora/decisoes_supremo/'

########################
##### GLOBAL VARS ######
########################

cur, conn
rows, totalRows

########################
##### END SETTINGS #####
########################