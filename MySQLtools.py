# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs
import settings as st
import utils as ut

# MySQL connection
def connMySQL():

    if st.debug >= 1: print 'Connecting to MySQL'
    st.conn = libs.db.Connect(
        host=st.MySQLhost,
        user=st.MySQLusername,
        passwd=st.MySQLpasswd,
        db=st.MySQLdb,
        cursorclass = libs.db.cursors.DictCursor,
        charset='utf8')
    st.cur = st.conn.cursor()
    if st.debug >= 1: print 'MySQL connection successful'


# Procedural functions
def dropTable(table):
    
    if st.debug >= 1: print 'Dropping table: %s' % table
    sql = "DROP TABLE %s" % table
    try:
        st.cur.execute(sql)
    except Exception:
        pass


def createTableFrom(table,sourceTable):
    
    if st.debug >= 1: print 'Creating table: %s' % table
    sql = "create table %s select * from %s where 1=0 %s" % (table, sourceTable, st.MySQLLimit)
    st.cur.execute(sql)

    if st.debug >= 1: print 'Changing charset'
    sql = "alter table %s default character set = utf8, engine = MyISAM" % table
    st.cur.execute(sql)
    

def createTable(table,columns):
    
    if st.debug >= 1: print 'Creating table: %s' % table
    sql = "create table %s (" % table
    sql = sql + ', '.join(columns)
    sql = sql + ') engine = MyISAM default character set = utf8'
    try:
        st.cur.execute(sql)
    except Exception:
        print 'ERROR: ', sql


def addPK(table):
    
    if st.debug >= 1: print 'Adding id as primary key'
    sql = "alter table %s add column id int not null auto_increment first, add primary key (id)" % table
    st.cur.execute(sql)


def addIndex(table,column):
    
    if st.debug >= 1: print 'Adding index idx_%s to column %s on table %s' % (column,column,table)
    sql = "alter table %s add index idx_%s(%s)" % (table,column,column)
    st.cur.execute(sql)


def populateTableFrom(table,sourceTable):
    
    if st.debug >= 1: print 'Inserting data into table: %s' % table
    sql = 'select * from %s where 1=0' % sourceTable
    st.cur.execute(sql)
    
    columns = [i[0] for i in st.cur.description]
    sql = "insert into %s (%s) select * from %s %s" % (table, ', '.join(columns), sourceTable, st.MySQLLimit)
    st.cur.execute(sql)


def addHashes(table,sourceColumn):
    
    if st.debug >= 1: print 'Adding %s hashes to table %s' % (sourceColumn,table)
    sql = "alter table %s add column hash_%s varchar(50) after id" % (table,sourceColumn)
    st.cur.execute(sql)
    for row in st.rows:
        sql = "update %s set hash_%s = '%s' where id = %s" % (table, sourceColumn, libs.hashlib.md5(row[sourceColumn]).hexdigest(), row['id'])
        st.cur.execute(sql)
    st.conn.commit()


def getAll(table,where=''):

    if st.debug >= 1: print "Loading data from table %s" % table
    sql = "select * from %s %s %s" % (table, where, st.MySQLLimit)
    st.cur.execute(sql)
    st.rows = st.cur.fetchall()
    st.totalRows = st.cur.rowcount
    if st.debug >= 1: print "Data loaded: %s rows" % st.totalRows


def addPlain(table,sourceColumn,destColumn):

    if st.debug >= 1: print 'Converting RTF to plain text'
    sql = "alter table %s add column %s text" % (table,destColumn)
    st.cur.execute(sql)
    for row in st.rows:
        percentage = str(float(row['id'])/st.totalRows*100)+'%'
        if st.debug >= 2: print 'Converting RTF to plain text (id): %s of %s (%s)' % (row['id'],st.totalRows,percentage)
        sql = "update %s set %s = '%s ' where id = %s" % (table, destColumn, ut.rtf2txt(row[sourceColumn]).replace("'",''),row['id'])
        try:
            st.cur.execute(sql)
        except Exception:
            print sql
            pass
        st.conn.commit()


def MySQL2Pandas(sql):

    return libs.psql.frame_query(sql, con=st.conn)


def writeFiles():
    print 'Writing files to disk'
    sql = "select id, num_processo, txt_text from %s where txt_text is not null %s" % (table, st.MySQLLimit)
    st.cur.execute(sql)
    txts = st.cur.fetchall()
    i = 1
    for txt in txts:
        filename = str(txt['id'])+'-'+str(txt['num_processo'])+'.txt'
        print 'Writing file: %s - (%s of %s)' % (filename,i,st.cur.rowcount)
        write2disk(filename,txt['txt_text'])
        i+=1


def createCorpora():
    global decsCorp

    print 'Reading files from disk'
    root = filesFolder
    decs = PlaintextCorpusReader(root, '.*\.txt')
    print decs.fileids()

    print 'Creating a corpora'
    decsCorp = Text(decs.words(), name="Decisoes STF")


