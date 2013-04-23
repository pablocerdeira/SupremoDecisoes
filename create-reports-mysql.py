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
totalDecs =             True
totalDecsPerCaseYear =  True
totalDecsPerYear =      True


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

