import os
import sqlite3
import pickle
from datetime import datetime

from contextlib import contextmanager


@contextmanager
def cursor(connection):
    c = connection.cursor()
    try:
        yield c
    finally:
        connection.commit()
        c.close()


class SqliteStash:

    def __init__(self, data_dir, db_name=None):
        path = os.path.expanduser(data_dir)
        db_name = db_name or 'stash_data.db'
        self.conn = sqlite3.connect(os.path.join(path, db_name))
        with cursor(self.conn) as c:
            c = self.conn.cursor()
            c.execute('CREATE TABLE data (date text, key text, value text)')

    def stash(self, key, obj):
        obj_pickle = pickle.dumps(obj)
        with cursor(self.conn) as c:
            data = (datetime.utcnow().isoformat(), str(key), obj_pickle)
            c.execute(f'INSERT INTO data VALUES (?, ?, ?)', data)

    def ls(self):
        items = self._ls()
        for index, item in enumerate(self._ls()):
            print(f'{index}: {item}')

    def delete(self, key):
        with cursor(self.conn) as c:
            c.execute(f'DELETE FROM data WHERE key = {key}')

    def delete_by_index(self, index):


    def _ls(self):
        items = []
        with cursor(self.conn) as c:
            for index, name in enumerate(c.execute('SELECT key FROM data')):
                items.append(name)
        return items


class NoOpStash:

    def _report(self, method):
        print(f'{method} not configured, create config in ~/.stashed/config')

    def stash(self, key, obj):
        self._report('stash')

    def ls(self):
        self._report('ls')

    def delete(self, key):
        self._report('delete')

    def delete_by_index(self, index):
        self._report('delete_by_index')

    def _ls(self):
        self._report('_ls')
