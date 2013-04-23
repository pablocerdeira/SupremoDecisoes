import libraries as lib
import settings as st

def connMySQL():
    
    if st.debug >= 1: print 'Connecting to MySQL'
    st.conn = lib.db.Connect(
        host=st.MySQLhost,
        user=st.MySQLusername,
        passwd=st.MySQLpasswd,
        db=st.MySQLdb,
        cursorclass = lib.db.cursors.DictCursor,
        charset='utf8')
    st.cur = st.conn.cursor()
    if st.debug >= 1: print 'MySQL connection successful'

def loadMySQL(sql):
    
    return lib.psql.frame_query(sql, con=st.conn)
    st.conn.close()
