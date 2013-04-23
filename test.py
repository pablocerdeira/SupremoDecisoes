# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb as db
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor, SSCursor


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

def main():
    connMySQL()
    sql = 'select id, nom_ministro, tip_julgamento from ta_main limit 0,10'
    cur.execute(sql)
    csv = ''
    columns = [i[0] for i in cur.description]
    csv += ('"'+'","'.join(columns)+'"\n')
    print csv
    rows = cur.fetchall()
    for row in rows:
        tmp = []
        for column in columns:
            tmp.append(str(row[column]))
        csv += ('"'+'","'.join(tmp)+'"\n')
    print csv

if __name__ == "__main__":
    main()
