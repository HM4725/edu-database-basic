"""
기능: 프로세스가 종료되더라도 데이터는 유효함
문제: CRUD의 Time/Space Complexity

특징: 
- 키가 정렬되어 있지 않음
- Update, Delete시에 뒤쪽 모든 데이터를 덮어쓰기함

참고: self._db.seek(0)가 python&OS buffer flush를 유발함.
https://stackoverflow.com/questions/41620533/does-python-automatically-flush-its-buffer-when-calling-seek-and-or-read-operati
"""

from mod.dbinterface import DbInterface
from mod.random_message import random_message
import json
import os


class DbOndisk(DbInterface):
    def __init__(self, filename: str = "test.db"):
        try:
            self._db = open(filename, mode="rt+")
        except FileNotFoundError:
            self._db = open(filename, mode="xt+")

    def __del__(self):
        if hasattr(self, "_db"):
            self._db.close()

    def create(self, key: int, value: str):
        """
        Time Complexity: O(N)
        Space Complexity: O(1)
        """
        self._db.seek(0)
        for line in self._db:
            record = json.loads(line)
            if record["key"] == key:
                raise KeyError(key)
        record = {"key": key, "value": value}
        self._db.write(json.dumps(record) + "\n")

    def read(self, key: int) -> str:
        """
        Time Complexity: O(N)
        Space Complexity: O(1)
        """
        self._db.seek(0)
        for line in self._db:
            record = json.loads(line)
            if record["key"] == key:
                return record["value"]
        raise KeyError(key)

    def update(self, key: int, value: str):
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        self._db.seek(0)
        records = list(map(json.loads, self._db.readlines()))
        for record in records:
            if record["key"] == key:
                record["value"] = value
                self._db.seek(0)
                self._db.writelines(list(map(lambda s: json.dumps(s) + "\n", records)))
                self._db.truncate(self._db.tell())
                return
        raise KeyError(key)

    def delete(self, key: int):
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        self._db.seek(0)
        records = list(map(json.loads, self._db.readlines()))
        for i, record in enumerate(records):
            if record["key"] == key:
                records = records[:i] + records[i + 1 :]
                self._db.seek(0)
                self._db.writelines(list(map(lambda s: json.dumps(s) + "\n", records)))
                self._db.truncate(self._db.tell())
                return
        raise KeyError(key)


FILENAME = "test.db"

# First try
seq = 0
db = DbOndisk(FILENAME)
for _ in range(10):
    db.create(seq, random_message())
    seq += 1
db.update(0, random_message())
db.delete(seq - 1)
print(f"db.read(0): {db.read(0)}")

# Reboot
print("Reboot...")
del db

# Second try
db = DbOndisk(FILENAME)
try:
    print(f"db.read(0): {db.read(0)}")
except KeyError:
    print(f"[ERROR] db.read(0): not exist")

# Cleanup
del db
os.remove(FILENAME)
