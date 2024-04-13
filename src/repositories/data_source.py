from abc import ABC, abstractmethod

# 데이터 액세스 인터페이스 정의
class DataSource(ABC):

    @abstractmethod
    def load_data(self, db_name, table_name):
        pass
