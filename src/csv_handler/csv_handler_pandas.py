
from src.csv_handler.abstract_tabular_data import TabularData
from src.utils.logging_handler import logging_handler


class PandasHandler(TabularData):
    def __init__(self):
        logging_handler.error("Backend Pandas not supported yet")
        exit()

    def read(self, ):
        pass

    def write(self,):
        pass