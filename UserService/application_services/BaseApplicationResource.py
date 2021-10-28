from abc import ABC, abstractmethod
from database_services.RDBService import RDBService


class BaseApplicationException(Exception):

    def __init__(self):
        pass


class BaseApplicationResource(ABC):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_by_template(cls, template):
        pass

    @classmethod
    @abstractmethod
    def get_links(self, resource_data):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(self):
        pass
    
    @classmethod
    @abstractmethod
    def create_data_resource(cls, template):
        pass


class BaseRDBApplicationResource(BaseApplicationResource):

    def __init__(self):
        pass

    @classmethod
    def get_by_template(cls, template, limit="10", offset="0"):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.find_by_template(db_name, table_name,
                                          template, limit, offset)
        return res

    @classmethod
    @abstractmethod
    def get_links(self, resource_data):
        pass

    @classmethod
    def create_data_resource(cls, template):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.create(db_name, table_name, template)
        return res
    
    @classmethod
    def get_next_id(cls, id_column):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.next_id(db_name, table_name, id_column)
        return res
