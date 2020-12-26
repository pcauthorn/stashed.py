from stashed.storage import SqliteStore
import os

_Stasher = SqliteStore()


def stash(key, obj, group=None):
    _Stasher.store(key, obj, group=group)


def retrieve(key):
    _Stasher.get(key)


def ls():
    _Stasher.ls()


def delete(key):
    _Stasher.delete(key)


def exists(key):
    _Stasher.exists(key)


def delete_by_index(index):
    _Stasher.delete_by_index(index)

# 1) Look for config at ~/.stashed/config
