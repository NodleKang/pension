from abc import ABC, abstractmethod

# 데이터 액세스 인터페이스 정의
class DataRepository(ABC):
    @abstractmethod
    def get_all_data(self, db_name, table_name):
        pass