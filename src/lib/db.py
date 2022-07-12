import sqlite3
import hashlib

con = sqlite3.connect('data.db')
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS `users` (`nickname` TEXT PRIMARY KEY, `password` TEXT);')
cur.execute('CREATE TABLE IF NOT EXISTS `sessions` (`ip` TEXT PRIMARY KEY, `nickname` TEXT);')
con.commit()

qolang_export = {
    "dbexec": "exec",
    "dbfetchall": "fetchall",
    "dbfetchone": "fetchone",
    "dbcommit": "commit",
    "dbhash": "hash",
}

def dbexec(Variables, args):
    cur.execute(args[0])
    return (Variables, None)

def dbfetchall(Variables, args):
    return (Variables, cur.fetchall())

def dbfetchone(Variables, args):
    return (Variables, cur.fetchone())

def dbcommit(Variables, args):
    con.commit()
    return (Variables, None)

def dbhash(Variables, args):
    encoded = args[0].encode()
    hashed1 = hashlib.md5(encoded).hexdigest().encode()
    hashed2 = hashlib.md5(hashed1).hexdigest()
    return (Variables, hashed2)
