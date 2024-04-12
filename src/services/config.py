import yaml


class Config:
    def __init__(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.__config = yaml.safe_load(file)
