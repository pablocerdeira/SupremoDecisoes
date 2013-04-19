# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb as db
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor, SSCursor
import hashlib
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
import cStringIO
import nltk
from nltk.text import Text
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import codecs

# Global variables
MySQLLimit = "limit 0,1000"
tableName = "pablo_tmp"
filesFolder = '/home/pablocerdeira/corpora/decisoes_tmp/'
rows = 'MySQL rows'

# General functions
def md5(text):
    hash = hashlib.md5(str(text)).hexdigest()
    if hash == None:
        hash = 'aa'
    return hash


def rtf2txt(doc):
    rtf = cStringIO.StringIO()
    try:
        rtf.write(doc)
        read = Rtf15Reader.read(rtf)
        txt = PlaintextWriter.write(read).read()
        txt = txt.replace("'","")
    except Exception:
        txt = ''
        print 'Erro no rtf2txt'
        pass
    return txt.decode('utf8')


def write2disk(name,content):
    try:
        f = codecs.open(filesFolder+str(name), "w", encoding='utf8')
        try:
            f.write(content)
        finally:
            print 'Erro no write2disk'
            f.close()
    except IOError:
        pass


def connMySQL():
    global cur, conn

    print 'Connecting to MySQL'
    conn = db.Connect(
        host='172.16.4.51',
        user='pablocerdeira',
        passwd='pablo123',
        db='fredericodba',
        cursorclass = db.cursors.DictCursor,
        charset='utf8')
    cur = conn.cursor()
    print 'MySQL connection successful'


# Procedures functions
def cleanupTable():
    print 'Dropping table: %s' % tableName
    sql = "DROP TABLE %s" % tableName
    try:
        cur.execute(sql)
    except Exception:
        pass


def createTable():
    cleanupTable()
    print 'Creating table: %s' % tableName
    sql = "create table %s select * from monocraticas where 1=0 %s" % (tableName, MySQLLimit)
    cur.execute(sql)

    print 'Changing charset'
    sql = "alter table %s default character set = utf8, engine = MyISAM" % tableName
    cur.execute(sql)

    print 'Inserting data into table: %s' % tableName
    sql = "insert into %s select * from monocraticas %s" % (tableName, MySQLLimit)
    cur.execute(sql)

    print 'Adding id as primary key'
    sql = "alter table %s add column id int not null auto_increment first, add primary key (id)" % tableName
    cur.execute(sql)


def getAll(where='where txt_conteudo is not null'):
    global rows, totalRows

    print 'Loading data from table'
    sql = "select * from %s %s %s" % (tableName, where, MySQLLimit)
    cur.execute(sql)
    rows = cur.fetchall()
    totalRows = cur.rowcount


def addHashes():
    print 'Adding hashes'
    sql = "alter table %s add column hash varchar(50) after id" % tableName
    cur.execute(sql)
    for row in rows:
        try:
            sql = "update %s set hash = '%s' where id = %s" % (tableName, hashlib.md5(row['txt_conteudo']).hexdigest(),row['id'])
            cur.execute(sql)
        except Exception:
            print 'ERRO: ', row['txt_conteudo']
            pass
    conn.commit()


def addPlain():
    print 'Converting RTF to plain text'
    sql = "alter table %s add column txt_text text" % tableName
    cur.execute(sql)
    for row in rows:
        percentage = str(float(row['id'])/totalRows*100)+'%'
        print 'Converting RTF to plain text (id): %s of %s (%s)' % (row['id'],totalRows,percentage)
        sql = "update %s set txt_text = '%s ' where id = %s" % (tableName, rtf2txt(row['txt_conteudo']).replace("'",''),row['id'])
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


# Main function
def main():
    connMySQL()
    createTable()
    getAll('where txt_conteudo is not null')
    addHashes()
    addPlain()
    writeFiles()
    createCorpora()
    print decsCorp.concordance('consumidor')


if __name__ == "__main__":
    main()