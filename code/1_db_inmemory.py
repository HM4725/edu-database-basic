"""
기능: 데이터 CRUD가 가능
문제: 프로세스가 종료되면, 자료구조의 데이터도 사라짐
"""

from mod.dbinterface import DbInterface
from mod.random_message import random_message


class DbInmemory(DbInterface):
    def __init__(self):
        self._db = []

    def create(self, key: int, value: str):
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        for record in self._db:
            if record["key"] == key:
                raise KeyError(key)
        record = {"key": key, "value": value}
        self._db.append(record)

    def read(self, key: int) -> str:
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        for record in self._db:
            if record["key"] == key:
                return record["value"]
        raise KeyError(key)

    def update(self, key: int, value: str):
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        for record in self._db:
            if record["key"] == key:
                record["value"] = value
                return
        raise KeyError(key)

    def delete(self, key: int):
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        for i, record in enumerate(self._db):
            if record["key"] == key:
                self._db = self._db[:i] + self._db[i + 1 :]
                return
        raise KeyError(key)


# First try
seq = 0
db = DbInmemory()
for _ in range(10):
    db.create(seq, random_message())
    seq += 1
db.update(0, random_message())
db.delete(seq-1)
print(f"db.read(0): {db.read(0)}")

# Reboot
print("Reboot...")
del db

# Second try
db = DbInmemory()
try:
    print(f"db.read(0): {db.read(0)}")
except KeyError:
    print(f"[ERROR] db.read(0): not exist")
