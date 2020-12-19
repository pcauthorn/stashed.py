from stashed.storage import SqliteStash
import os

_Stasher = SqliteStash()


def stash(key, obj):
    _Stasher.stash(key, obj)


def ls():
    _Stasher.ls()


def delete(key):
    _Stasher.delete(key)


def delete_by_index(index):
    _Stasher.delete_by_index(index)



# 1) Look for config at ~/.stashed/config