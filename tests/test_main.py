from unittest import TestCase

import main
import services
from repositories.data_source_factory import DataSourceFactory

TABLES = ["accounts", "month_end_assets"]

class Test(TestCase):

    def test_load_config(self):
        config = services.Config('C:/Workspace/pension/resources/config/config.yaml')
        data_source = DataSourceFactory.get_data_source(config)
        for table in TABLES:
            db_name, table_name = config.get_source_identifiers(table)
            df = data_source.load_data(db_name, table_name)
            print(df)