from services.config import Config
from repositories.data_source import DataSource
from repositories.google_sheets_source import GoogleSheetsSource

class DataSourceFactory:
    @staticmethod
    def get_data_source(config: Config) -> DataSource:
        if config.active_data_source == "google_sheets":
            return GoogleSheetsSource(config.get_google_credentials_path())
        elif config.active_data_source == "mysql":
            return None
        elif config.active_data_source == "elasticsearch":
            return None
        else:
            raise ValueError("Unknown data source type")