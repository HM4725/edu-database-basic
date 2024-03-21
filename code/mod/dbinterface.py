class DbInterface:
    def __init__(self):
        raise TypeError("인터페이스는 객체를 직접 생성하지 마세요.")
    
    def create(self, key: int, value: str):
        raise NotImplementedError

    def read(self, key: int) -> str:
        raise NotImplementedError
    
    def update(self, key: int, value: str):
        raise NotImplementedError
    
    def delete(self, key: int):
        raise NotImplementedError
