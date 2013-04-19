# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import libs
import settings as st

# General functions
def md5(text):
    hash = hashlib.md5(str(text)).hexdigest()
    if hash == None:
        hash = ''
    return hash


def rtf2txt(doc):
    rtf = libs.cStringIO.StringIO()
    try:
        rtf.write(doc)
        read = libs.Rtf15Reader.read(rtf)
        txt = libs.PlaintextWriter.write(read).read()
        txt = txt.replace("'","")
    except Exception:
        txt = ''
        print 'Erro no rtf2txt'
        pass
    return txt.decode('utf8')


def write2disk(name,content):
    try:
        f = libs.codecs.open(st.exportFolder+str(name), "w", encoding='utf8')
        try:
            f.write(content)
        finally:
            print 'Erro no write2disk'
            f.close()
    except IOError:
        pass


def createCorpora():
    global decsCorp

    print 'Reading files from disk'
    root = st.exportFolder
    decs = libs.PlaintextCorpusReader(root, '.*\.txt')
    print decs.fileids()

    print 'Creating a corpora'
    decsCorp = Text(decs.words(), name="Decisoes STF")
