# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# MySQL connection
def connMySQL():
    global cur, conn

    if debug >= 1: print 'Connecting to MySQL'
    conn = db.Connect(
        host=MySQLhost,
        user=MySQLusername,
        passwd=MySQLpasswd,
        db=MySQLdb,
        cursorclass = db.cursors.DictCursor,
        charset='utf8')
    cur = conn.cursor()
    if debug >= 1: print 'MySQL connection successful'


# Procedural functions
def dropTable(table):
    if debug >= 1: print 'Dropping table: %s' % table
    sql = "DROP TABLE %s" % table
    try:
        cur.execute(sql)
    except Exception:
        pass


def createTableFrom(table,sourceTable):
    if debug >= 1: print 'Creating table: %s' % table
    sql = "create table %s select * from %s where 1=0 %s" % (table, sourceTable, MySQLLimit)
    cur.execute(sql)

    if debug >= 1: print 'Changing charset'
    sql = "alter table %s default character set = utf8, engine = MyISAM" % table
    cur.execute(sql)
    

def createTable(table,columns):
    if debug >= 1: print 'Creating table: %s' % table
    sql = "create table %s (" % table
    sql = sql + ', '.join(columns)
    sql = sql + ') engine = MyISAM default character set = utf8'
    cur.execute(sql)


def addPK(table):
    if debug >= 1: print 'Adding id as primary key'
    sql = "alter table %s add column id int not null auto_increment first, add primary key (id)" % table
    cur.execute(sql)


def addIndex(table,column):
    if debug >= 1: print 'Adding index idx_%s to column %s on table %s' % (column,column,table)
    sql = "alter table %s add index idx_%s(%s)" % (table,column,column)
    cur.execute(sql)


def populateTableFrom(table,sourceTable):
    if debug >= 1: print 'Inserting data into table: %s' % table
    sql = "insert into %s select * from %s %s" % (table, sourceTable, MySQLLimit)
    cur.execute(sql)


def addHashes(table,sourceColumn):
    
    if debug >= 1: print 'Adding %s hashes to table %s' % (sourceColumn,table)
    sql = "alter table %s add column hash_%s varchar(50) after id" % (tableName,sourceColumn)
    cur.execute(sql)
    for row in rows:
        try:
            sql = "update %s set hash = '%s' where id = %s" % (tableName, hashlib.md5(row[sourceColumn]).hexdigest(),row['id'])
            cur.execute(sql)
        except Exception:
            print 'ERRO: ', row[sourceColumn]
            pass
    conn.commit()


def getAll(table,where=''):
    global rows, totalRows

    if debug >= 1: print "Loading data from table %s" % table
    sql = "select * from %s %s %s" % (table, where, MySQLLimit)
    cur.execute(sql)
    rows = cur.fetchall()
    totalRows = cur.rowcount
    if debug >= 1: print "Data loaded: %s rows" % totalRows


def addPlain(table,sourceColumn,destColumn):
    if debug >= 1: print 'Converting RTF to plain text'
    sql = "alter table %s add column %s text" % (table,destColumn)
    cur.execute(sql)
    for row in rows:
        percentage = str(float(row['id'])/totalRows*100)+'%'
        if debug >= 2: print 'Converting RTF to plain text (id): %s of %s (%s)' % (row['id'],totalRows,percentage)
        sql = "update %s set %s = '%s ' where id = %s" % (tableName, destColumn, rtf2txt(row[sourceColumn]).replace("'",''),row['id'])
        try:
            cur.execute(sql)
        except Exception:
            print sql
            pass
        conn.commit()


def writeFiles():
    print 'Writing files to disk'
    sql = "select id, num_processo, txt_text from %s where txt_text is not null %s" % (tableName, MySQLLimit)
    cur.execute(sql)
    txts = cur.fetchall()
    i = 1
    for txt in txts:
        filename = str(txt['id'])+'-'+str(txt['num_processo'])+'.txt'
        print 'Writing file: %s - (%s of %s)' % (filename,i,cur.rowcount)
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


