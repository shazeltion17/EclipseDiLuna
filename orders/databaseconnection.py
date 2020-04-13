import psycopg2 as pg2


def connect():
    conn = pg2.connect(host='localhost', port='5432', dbname='postgres', user='postgres', password='admin')
    cur = conn.cursor()
    cur.execute('select version()')

