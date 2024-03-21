"""
CREATE: 검증하지 않고, 뒤에 레코드 추가
READ  : 모든 레코드 읽기
UPDATE: Method Not Allowed
DELETE: Method Not Allowed

특징: 
- CREATE와 READ 메소드만 지원
- 키가 정렬되어 있지 않음
- CREATE의 성능 최고
"""

from mod.dbinterface import DbInterface
from mod.random_message import random_message
import json
import io
import os
import time


class DbLog(DbInterface):
    def __init__(self, filename: str = "test.db"):
        self.filename = filename
        try:
            self._db = open(filename, mode="rt+")
        except FileNotFoundError:
            self._db = open(filename, mode="xt+")

    def __del__(self):
        if hasattr(self, "_db"):
            self._db.close()

    def create(self, key: int, value: str):
        """
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        record = {"key": key, "value": value}
        self._db.seek(0, io.SEEK_END)
        log = json.dumps(record) + "\n"
        self._db.write(log)

    def read(self, key: int) -> str:
        """
        Time Complexity: O(N)
        Space Complexity: O(1)
        """
        self._db.seek(0)
        found = None
        for line in self._db:
            record = json.loads(line)
            if record["key"] == key:
                found = record["value"]
        if found != None:
            return found
        raise KeyError(key)


def prepare(filename: str, n: int):
    db = DbLog(filename)
    for key in range(n):
        db.create(key, random_message())


def run(filename: str, n: int):
    db = DbLog(filename)
    start = time.time()
    db.create(n, random_message())
    end = time.time()
    time_c = (end - start) * 1000
    start = time.time()
    db.read(n - 1)
    end = time.time()
    time_r = (end - start) * 1000
    return time_c, time_r


def cleanup(filename: str):
    os.remove(filename)


if __name__ == "__main__":
    FILENAME = "test.db"
    records = []
    for n in [1, 10, 100, 1000, 10000, 100000]:
        prepare(FILENAME, n)
        time_c, time_r = run(FILENAME, n)
        record_c = {"op": "Create", "n": n, "t": time_c}
        record_r = {"op": "Read", "n": n, "t": time_r}
        records.append(record_c)
        records.append(record_r)
        cleanup(FILENAME)
    for op in ["Create", "Read"]:
        for record in filter(lambda rec: rec["op"] == op, records):
            n = record["n"]
            t = record["t"]
            print(f"op: {op:>6}, n: {n:6}, t: {t:6.2f}ms")
