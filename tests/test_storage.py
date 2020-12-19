import unittest
import tempfile
from stashed.storage import SqliteStore
from datetime import date


class PickleMe:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v


class TestSqliteStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = SqliteStore(self.temp_dir.name)

    def tearDown(self):
        self.store.close()
        self.temp_dir.cleanup()

    def test_stash_and_get(self):
        self.store.store('k1', 'one')
        self.store.store('k2', None)
        self.assertEqual(self.store.get('k1'), 'one')
        self.assertIsNone(self.store.get('k2'))
        self.assertRaises(KeyError, self.store.get, 'nok', raise_key_error=True)
        self.assertIsNone(self.store.get('nok'))

    def test_stash_and_get_types(self):

        items = [1, 'two', PickleMe(3), u'score', 5.0, (6,), date(7, 7, 7)]
        for index, item in enumerate(items):
            self.store.store(index, item)
        for index, item in enumerate(items):
            self.assertEqual(self.store.get(index), item)

    def test_ls(self):
        self.assertEqual(len(self.store._ls()), 0)
        for i in range(1, 5):
            self.store.store(i, i)
            self.assertEqual(len(self.store._ls()), i)
        for i, v in enumerate(self.store._ls()):
            self.assertEqual(str(i + 1), str(v))

    def test_delete(self):
        self.assertEqual(len(self.store._ls()), 0)
        for i in range(1, 6):
            self.store.store(i, i)
        self.assertEqual(len(self.store._ls()), 5)
        self.store.delete(3)
        self.assertEqual(len(self.store._ls()), 4)
        self.assertRaises(KeyError, self.store.get, 3, raise_key_error=True)

    def test_delete_by_index(self):
        self.assertEqual(len(self.store._ls()), 0)
        for i in range(0, 5):
            self.store.store(i, i)
        self.store.delete_by_index(4)
        self.assertRaises(KeyError, self.store.get, 4, raise_key_error=True)
        self.assertEqual(len(self.store._ls()), 4)
        self.store.delete_by_index(42)
        self.assertEqual(len(self.store._ls()), 4)

    def test_delete_older(self):
        pass


if __name__ == '__main__':
    unittest.main()