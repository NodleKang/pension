import yaml


class Config:
    def __init__(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.__config = yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception("Configuration file not found")
        except yaml.YAMLError:
            raise Exception("Error parsing the configuration file")

        self.active_data_source = self.__config['active_data_source']

    def get_active_data_source(self) -> dict:
        """Retrieve the active data source configuration."""
        return self.__config['data_sources'].get(self.active_data_source, {})

    def get_source_identifiers(self, source_name: str) -> (str, str):
        """
        Get the source name and table name for a given source identifier.
        Returns a tuple (source_name, table_name).
        """

        data_source = self.get_active_data_source()

        """        
        Get the spreadsheet name and worksheet name for a given source identifier.
        Returns a tuple (spreadsheet_name, worksheet_name).
        """
        if self.active_data_source == 'google_sheets':
            for data_set_key, data_set_value in data_source['data_sets'].items():
                if data_set_key == source_name:
                    return data_set_value['spreadsheet_name'], data_set_value['worksheet_name']

        return None, None

    def get_google_credentials_path(self) -> str:
        if self.active_data_source == 'google_sheets':
            data_source = self.get_active_data_source()
            return data_source['credentials_path']

        return None