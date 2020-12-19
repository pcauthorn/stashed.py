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


class SqliteStore:

    def _get_now_str(self):
        return datetime.utcnow().isoformat()

    def __init__(self, data_dir, db_file_name=None):
        path = os.path.expanduser(data_dir)
        db_file_name = db_file_name or 'stash_data.db'
        self.conn = sqlite3.connect(os.path.join(path, db_file_name))
        with cursor(self.conn) as c:
            c.execute('CREATE TABLE IF NOT EXISTS data (timestamp text, key text, value text)')

    def store(self, key, obj):
        obj_pickle = pickle.dumps(obj)
        with cursor(self.conn) as c:
            data = (self._get_now_str(), str(key), obj_pickle)
            c.execute(f'INSERT INTO data VALUES (?, ?, ?)', data)

    def get(self, key, raise_key_error=False):
        key = str(key)
        with cursor(self.conn) as c:
            data = c.execute(f'SELECT value from data where key = ?', (key,))
            o = data.fetchone()
            if raise_key_error and not o:
                raise KeyError(f'{key} not in store')
            elif o:
                return pickle.loads(o[0])

    def ls(self):
        for index, item in enumerate(self._ls()):
            print(f'{index}: {item}')

    def delete(self, key):
        key = str(key)
        with cursor(self.conn) as c:
            c.execute(f'DELETE FROM data WHERE key = ?', (key,))

    def delete_by_index(self, index):
        items = self._ls()
        if index < len(items):
            self.delete(items[index])

    def delete_older(self, ref_time_utc):
        with cursor(self.conn) as c:
            c.execute('DELETE FROM data WHERE timestamp < ?', (ref_time_utc.isoformat(),))

    def _ls(self):
        items = []
        with cursor(self.conn) as c:
            for index, name in enumerate(c.execute('SELECT key FROM data')):
                items.append(name[0])
        return items

    def close(self):
        self.conn.close()


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
