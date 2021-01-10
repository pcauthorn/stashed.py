import os

from stashed.storage import SqliteStore

DEFAULT_DIR = os.path.expanduser('~/.reiteration')

_Stasher = SqliteStore(DEFAULT_DIR)


def stash(key, obj, group=None):
    _Stasher.store(key, obj, group=group)


def retrieve(key):
    return _Stasher.get(key)


def ls():
    _Stasher.ls()


def delete(key):
    _Stasher.delete(key)


def exists(key):
    return _Stasher.exists(key)


def delete_by_index(index):
    _Stasher.delete_by_index(index)

# 1) Look for config at ~/.stashed/config
