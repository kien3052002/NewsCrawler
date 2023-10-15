import psycopg2
from vnexscrapy.db_config import *


class DatabasePipeline:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def db_init(self):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

        self.cursor.execute(create_query_category)
        self.cursor.execute(create_query_source)
        self.cursor.execute(create_query_news)
        self.cursor.execute(create_query_config)
        for data in domain_config:
            self.insert_data('config', data)

        self.connection.commit()

        self.cursor.close()
        self.connection.close()

    def open_spider(self, spider):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def process_item(self, item, spider):
        item_class = item.__class__.__name__
        if item_class == 'CategoryItem':
            self.insert_data('category', item)
        elif item_class == 'NewsItem':
            self.insert_data('news', item)
        elif item_class == 'SourceItem':
            self.insert_data('source', item)
        self.connection.commit()
        return item

    def insert_data(self, table_name, data):
        columns = list(data.keys())
        placeholders = ', '.join(['%s' for col in columns])

        insert_query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE SET
        """
        update_query = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != 'id'])
        insert_query += update_query

        values = [data[col] for col in columns]

        self.cursor.execute(insert_query, values)

    def get_data(self, table_name, condition):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

        get_query = f"SELECT * FROM {table_name} WHERE {condition} LIMIT 1;"
        self.cursor.execute(get_query)

        row_data = self.cursor.fetchone()
        column_fields = [desc[0] for desc in self.cursor.description]

        if row_data:
            data = dict(zip(column_fields, row_data))
        return data

    def table_exists(self, table_name):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1;")
            return True
        except psycopg2.Error as e:
            return False

        self.cursor.close()
        self.connection.close()
