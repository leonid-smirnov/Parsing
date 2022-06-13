from MySQLdb._exceptions import Error
from pymongo import MongoClient
from itemadapter import ItemAdapter
from getpass import getpass
import pymysql


class MongoDBPipeline:

    def open_spider(self, spider):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['books']

    def process_item(self, item, spider):
        collection_name = 'all_books'
        self.db[collection_name].insert_one(item)

    def close_spider(self, spider):
        self.client.close()


class MySQLDBPipline:
    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host='localhost',
            port=int(3306),
            user=input("Имя пользователя: "),
            password=getpass("Пароль: "),
            db="books"
        )
        self.cursor = self.connection.cursor()

        create_table_query = '''
            CREATE TABLE all_books(
                title TEXT,
                price TEXT,
                description TEXT
                )
        '''

        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Error:
            pass

    def process_item(self, item, spider):
        insert_query = '''
        INSERT INTO all_books(title, price, description)
        VALUES (%s, %s, %s)
        '''

        self.cursor.execute(insert_query, (item.get('title'), item.get('price'), item.get('description')))
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()




