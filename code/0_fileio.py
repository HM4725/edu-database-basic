"""
[fileio 기본 API]
1. open: 파일 열기
2. write: 파일 쓰기
- 현재 file pointer 부터 특정 길이만큼 덮어쓰기
- 이후 file pointer += 특정 길이
3. read: 파일 읽기
- 현재 file pointer 부터 특정 길이만큼 읽기
- 이후 file pointer += 특정 길이
4. close: 파일 닫기

[file 제어 API]
1. seek: file pointer 설정
2. tell: 현재 file pointer 위치 구하기

[python의 file open mode]
1. r/w/a/x: 읽기/쓰기/추가/파일생성 전용
2. b/t: bytes/string 전용
3. +: 읽기쓰기 허용
"""

# First try
f = open("file.txt", mode="wt+")
# fp == 0
f.write("hello world\n")
# fp == len("hello world") == 11
# offset 11부터 "\n"가 나올 때까지 읽기
line = f.readline()
# offset 11부터는 데이터가 없음
assert len(line) == 0
f.close()

# Second try
f = open("file.txt", mode="at+")
f.write("hi fileio\n")
f.seek(0)
print(f.readline().rstrip())
print(f.readline().rstrip())
f.seek(0)
f.close()
