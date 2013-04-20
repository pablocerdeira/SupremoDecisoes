# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Database libraries
import MySQLdb as db
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor, SSCursor

# Hash library used to extract MD5 sum from decisions
import hashlib

# Libraries used to convert RTF to TXT
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
import cStringIO
import codecs

# Natural language processing libraries
import nltk
from nltk.text import Text
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import FreqDist
from nltk.corpus import stopwords
import string
