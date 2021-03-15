#!/usr/bin/python
# -*- coding: utf-8 -*-


#####https://docs.python.org/2/library/sqlite3.html###########


import sqlite3 as mydb
import sys

con = None

try:
    con = mydb.connect('sampleDB.db')
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data                    
except mydb.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()