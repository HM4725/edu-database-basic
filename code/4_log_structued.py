"""
CREATE: 검증하지 않고, 뒤에 레코드 추가
READ  : 키를 시간으로 설정, 이진탐색을 통해 읽기
UPDATE: Method Not Allowed
DELETE: Method Not Allowed

특징:
- CREATE와 READ 메소드만 지원
- 키 (timestamp)가 정렬되어 있음
- 정렬된 키를 통해 READ 성능 개선 (이진 탐색)
- 정형화된 데이터를 통해 READ의 Space Complexity 개선
-- {"key": bytes[17], "value": "bytes[36]"}

문제:
- UPDATE, DELETE 메소드도 필요
- Timestamp처럼 auto increment가 아닌,
  데이터베이스 중간에 레코드를 CREATE하는 경우도 필요
- 정형데이터가 아닌 비정형데이터의 처리 필요
"""

from mod.dbinterface import DbInterface
from mod.random_message import structured_random_message
from datetime import datetime
import json
import io
import os
import time


class DbLogTimestamp(DbInterface):
    def __init__(self, filename: str = "test.db"):
        self.filename = filename
        try:
            self._db = open(filename, mode="rb+")
        except FileNotFoundError:
            self._db = open(filename, mode="xb+")

    def __del__(self):
        if hasattr(self, "_db"):
            self._db.close()

    def create(self, key: int, value: str):
        """
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if len(str(key)) != 17:
            raise KeyError(f"len(key) != 17: {key}")
        if len(value) != 36:
            raise ValueError(f"len(value) != 36: {value}")
        record = {"key": key, "value": value}
        self._db.seek(0, io.SEEK_END)
        log = (json.dumps(record) + "\n").encode()
        self._db.write(log)

    def read(self, key: int) -> str:
        """
        Time Complexity: O(logN)
        Space Complexity: O(1)
        """
        LINE_SIZE = 76
        self._db.seek(0, os.SEEK_END)
        NUM_LINES = self._db.tell() // LINE_SIZE
        idx_l = 0
        idx_r = NUM_LINES
        while idx_l < idx_r:
            idx_m = (idx_l + idx_r) // 2
            self._db.seek(idx_m * LINE_SIZE)
            line = self._db.read(LINE_SIZE)
            key_m = int(line[8:25])
            if key_m < key:
                idx_l = idx_m + 1
            else:
                idx_r = idx_m
        if idx_r < NUM_LINES:
            self._db.seek(idx_r * LINE_SIZE)
            line = self._db.read(LINE_SIZE)
            key_r = int(line[8:25])
            if key_r == key:
                value = line[37:73].decode()
                return value
        raise KeyError(key)


def prepare(filename: str, n: int):
    db = DbLogTimestamp(filename)
    for _ in range(n):
        ts = int(datetime.now().timestamp() * 10000000)
        db.create(ts, structured_random_message())


def run(filename: str, n: int):
    db = DbLogTimestamp(filename)
    ts = int(datetime.now().timestamp() * 10000000)
    start = time.time()
    db.create(ts, structured_random_message())
    end = time.time()
    time_c = (end - start) * 1000
    start = time.time()
    db.read(ts)
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
            print(f"op: {op:>6}, n: {n:6}, t: {t:4.2f}ms")
