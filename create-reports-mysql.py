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

connectDB =             True
totalDecs =             False

# Simple specs reports
totalDecsPerJustice =   False
totalDecsPerClass =     False
totalDecsPerJudType =   False
totalDecsPerDecType =   False

# Complex specs reports
totalDecsPerJustClass =     False
totalDecsPerClassJust =     False
totalDecsPerJustDecType =   False
totalDecsPerDecTypeJust =   False
totalDecsPerClassDecT =     False
totalDecsPerDecTClass =     False

# Time reports
totalDecsPerCaseYear =  False
totalDecsPerYear =      False



# Main function
def main():
    
    if connectDB == True:
        SQL.connMySQL()                                        # Connect to MySQL

    # Report: Total decisions decisions
    if totalDecs == True:
        SQL.dropTable('rep_total_decs')
        if st.debug >= 1: print 'Creating rep_total_decs'
        sql = '''
            create table rep_total_decs
            select count(*) total_decs from {0}
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print 'Total decs: {0}'.format(row['total_decs'])


    #############################
    ### Simple specs reports  ###
    #############################
    # Report: Total decisions per Justice
    if totalDecsPerJustice == True:
        SQL.dropTable('rep_total_decs_justice')
        if st.debug >= 1: print 'Creating rep_total_decs_justice'
        sql = '''
            create table rep_total_decs_justice
            select nom_ministro, count(nom_ministro) total_decs 
            from {0}
            group by nom_ministro
            order by count(nom_ministro) desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_justice created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_justice')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}'.format(row['nom_ministro'],row['total_decs'])

    # Report: Total decisions per Class
    if totalDecsPerClass == True:
        SQL.dropTable('rep_total_decs_class')
        if st.debug >= 1: print 'Creating rep_total_decs_class'
        sql = '''
            create table rep_total_decs_class
            select sig_classe_proces, count(sig_classe_proces) total_decs 
            from {0}
            group by sig_classe_proces
            order by count(sig_classe_proces) desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_class created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_class')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}'.format(row['sig_classe_proces'],row['total_decs'])

    # Report: Total decisions per judgement type
    if totalDecsPerJudType == True:
        SQL.dropTable('rep_total_decs_judtype')
        if st.debug >= 1: print 'Creating rep_total_decs_judtype'
        sql = '''
            create table rep_total_decs_judtype
            select tip_julgamento, count(tip_julgamento) total_decs 
            from {0}
            group by tip_julgamento
            order by count(tip_julgamento) desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_judtype created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_judtype')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}'.format(row['tip_julgamento'],row['total_decs'])

    # Report: Total decisions per decision type
    if totalDecsPerDecType == True:
        SQL.dropTable('rep_total_decs_dectype')
        if st.debug >= 1: print 'Creating rep_total_decs_dectype'
        sql = '''
            create table rep_total_decs_dectype
            select dsc_tipo, count(dsc_tipo) total_decs 
            from {0}
            group by dsc_tipo
            order by count(dsc_tipo) desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_dectype created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_dectype')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}'.format(row['dsc_tipo'],row['total_decs'])


    #############################
    ### Complex specs reports ###
    #############################
    # Report: Total decisions per Justice and Class
    if totalDecsPerJustClass == True:
        SQL.dropTable('rep_total_decs_justice_class')
        if st.debug >= 1: print 'Creating rep_total_decs_justice_class'
        sql = '''
            create table rep_total_decs_justice_class
            select nom_ministro, sig_classe_proces, count(sig_classe_proces) total_decs 
            from {0}
            group by nom_ministro, sig_classe_proces
            order by nom_ministro, sig_classe_proces desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_justice_class created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_justice_class')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}\t{2}'.format(row['nom_ministro'],row['sig_classe_proces'],row['total_decs'])

    # Report: Total decisions per Class and Justice
    if totalDecsPerJustClass == True:
        SQL.dropTable('rep_total_decs_class_justice')
        if st.debug >= 1: print 'Creating rep_total_decs_class_justice'
        sql = '''
            create table rep_total_decs_class_justice
            select sig_classe_proces, nom_ministro, count(nom_ministro) total_decs 
            from {0}
            group by sig_classe_proces, nom_ministro
            order by sig_classe_proces, nom_ministro desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_class_justice created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_class_justice')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}\t{2}'.format(row['sig_classe_proces'],row['nom_ministro'],row['total_decs'])

    # Report: Total decisions per Justice and Decision Type
    if totalDecsPerJustDecType == True:
        SQL.dropTable('rep_total_decs_justice_dectype')
        if st.debug >= 1: print 'Creating rep_total_decs_justice_dectype'
        sql = '''
            create table rep_total_decs_justice_dectype
            select nom_ministro, dsc_tipo, count(dsc_tipo) total_decs 
            from {0}
            group by nom_ministro, dsc_tipo
            order by nom_ministro, dsc_tipo desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_justice_dectype created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_justice_dectype')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}\t{2}'.format(row['nom_ministro'],row['dsc_tipo'],row['total_decs'])

    # Report: Total decisions per Decision Type and Justice
    if totalDecsPerDecTypeJust == True:
        SQL.dropTable('rep_total_decs_dectype_justice')
        if st.debug >= 1: print 'Creating rep_total_decs_dectype_justice'
        sql = '''
            create table rep_total_decs_dectype_justice
            select dsc_tipo, nom_ministro, count(nom_ministro) total_decs 
            from {0}
            group by dsc_tipo, nom_ministro
            order by dsc_tipo, nom_ministro desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_dectype_justice created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_dectype_justice')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}\t{2}'.format(row['dsc_tipo'],row['nom_ministro'],row['total_decs'])

    # Report: Total decisions per Class and Decision Type
    if totalDecsPerClassDecT == True:
        SQL.dropTable('rep_total_decs_class_dectype')
        if st.debug >= 1: print 'Creating rep_total_decs_class_dectype'
        sql = '''
            create table rep_total_decs_class_dectype
            select sig_classe_proces, dsc_tipo, count(dsc_tipo) total_decs 
            from {0}
            group by sig_classe_proces, dsc_tipo
            order by sig_classe_proces, dsc_tipo desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_class_dectype created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_class_dectype')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}\t{2}'.format(row['sig_classe_proces'],row['dsc_tipo'],row['total_decs'])

    # Report: Total decisions per Decision Type and Class
    if totalDecsPerDecTClass == True:
        SQL.dropTable('rep_total_decs_dectype_class')
        if st.debug >= 1: print 'Creating rep_total_decs_dectype_class'
        sql = '''
            create table rep_total_decs_dectype_class
            select dsc_tipo, sig_classe_proces, count(sig_classe_proces) total_decs 
            from {0}
            group by dsc_tipo, sig_classe_proces
            order by dsc_tipo, sig_classe_proces desc
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_dectype_class created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_dectype_class')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}\t{2}'.format(row['dsc_tipo'],row['sig_classe_proces'],row['total_decs'])


    #############################
    ###      Time reports     ###
    #############################
    # Report: Total decisions per case year
    if totalDecsPerCaseYear == True:
        SQL.dropTable('rep_total_decs_case_year')
        if st.debug >= 1: print 'Creating rep_total_decs_case_year'
        sql = '''
            create table rep_total_decs_case_year
            select year(dat_autuacao) case_year, count(id) total_decs 
            from {0}
            group by year(dat_autuacao)
            order by year(dat_autuacao)
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_case_year created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_case_year')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}'.format(row['case_year'],row['total_decs'])

    # Report: Total decisions per year
    if totalDecsPerYear == True:
        SQL.dropTable('rep_total_decs_year')
        if st.debug >= 1: print 'Creating rep_total_decs_year'
        sql = '''
            create table rep_total_decs_year
            select year(dat_criacao) dec_year, count(id) total_decs 
            from {0}
            group by year(dat_criacao)
            order by year(dat_criacao)
        '''.format(st.ta_main)
        st.cur.execute(sql)
        if st.debug >= 1: print 'Table rep_total_decs_year created'
        if st.debug >= 2:
            SQL.getAll('rep_total_decs_year')
            print 'Rows: {0}'.format(st.totalRows)
            for row in st.rows: print '{0}\t{1}'.format(row['dec_year'],row['total_decs'])


if __name__ == "__main__":
    main()

