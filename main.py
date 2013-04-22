# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs
import settings as st
import utils as ut

# MySQL tools used by this software
import MySQLtools as SQL
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
### WARNING ###
### IMPORTANT ###
# If you are testing, please, CHANGE TABLE NAMES in settings.py!
# AGAIN: if you are testing, please, CHANGE TABLE NAMES in settings.py!
# And then, change the variables below to True

connectDB =         True
dropTables =        False
createTables =      False
createIndex =       False
populateTable =     False
addHash =           False
convertRTF2text =   False
createWordFreq =    False
createViews =       True


# Main function
def main():
    
    if connectDB == True:
        SQL.connMySQL()                                        # Connect to MySQL
    
    if dropTables == True:
        SQL.dropTable(st.ta_main)                              # Drop table ta_main
        SQL.dropTable(st.ta_words_all)                         # Drop table ta_words_all
    
    if createTables == True:    
        # Create ta_main table
        SQL.createTableFrom(st.ta_main,st.ta_main_source)      # Create table ta_main based on monocraticas
        SQL.addPK(st.ta_main)                                  # Add primary key to ta_main
    
        # Create ta_word_all
        SQL.createTable(st.ta_words_all,st.ta_words_all_columns)
    
    if createIndex == True:
        # Index ta_main
        for column in st.ta_main_idx:
            SQL.addIndex(st.ta_main,column)                    # Indexing columns on ta_main

        # Index ta_word_all
        for column in st.ta_words_all_idx:
            SQL.addIndex(st.ta_words_all,column)               # Indexing columns on ta_word_all

    if populateTable == True:   
        # Populate ta_main
        SQL.populateTableFrom(st.ta_main,st.ta_main_source)
        
    # Add hashes to ta_main
    if addHash == True:
        
        # Get data from ta_main and save it to rows
        # Used to create hashes and to convert RTF to txt
        SQL.getAll(st.ta_main,'where txt_conteudo is not null')

        SQL.addHashes(st.ta_main,'txt_conteudo')
        SQL.addIndex(st.ta_main,'hash_txt_conteudo')
    
    if convertRTF2text == True:
        if st.totalRows < 1:
            SQL.getAll(st.ta_main,'where txt_conteudo is not null')
            
        SQL.addPlain(st.ta_main,'txt_conteudo','txt_text')

    if createWordFreq == True:

        # Get data from ta_main and save it to rows
        # Used to create word frequencies
        SQL.getAll(st.ta_main,'where txt_text is not null')

        for row in st.rows:
            word_frequencies = ut.wordFrequence(row['txt_text'])
            for word in word_frequencies:
                if st.debug >= 2: print row['id'], word, word_frequencies[word]
                sql = "insert into %s (id_monocratica,word,word_count) values (%s,'%s',%s)" % (st.ta_words_all, row['id'], word, word_frequencies[word])
                try:
                    st.cur.execute(sql)
                except Exception:
                    print sql
                st.conn.commit()
                
    if createViews == True:
        #Create main view
        sql = 'drop view vw_words_freq_main'
        try:
            st.cur.execute(sql)
        except Exception:
            pass
        if st.debug >= 1: print 'Creating view vw_words_freq_main'
        sql = '''
            create view vw_words_freq_main as 
            select 
              m.id id_ta_main, m.hash_txt_conteudo,
              m.seq_objeto_incidente_principal,
              m.sig_classe_proces,
              m.num_processo,
              m.dat_autuacao,
              m.cod_recurso,
              m.tip_julgamento,
              m.seq_objeto_incidente,
              m.cod_ministro,
              m.nom_ministro,
              m.dat_sessao,
              m.dat_criacao,
              m.cod_tipo_texto,
              m.dsc_tipo,
              wf.id id_wf,
              wf.word,
              wf.word_count
            from
              {0} m,
              {1} wf
            where
              m.id = wf.id_monocratica
            '''.format(st.ta_main,st.ta_words_all)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Done: view vw_words_freq_main'
        

    #writeFiles()
    #createCorpora()
    #print decsCorp.concordance('consumidor')


if __name__ == "__main__":
    main()

