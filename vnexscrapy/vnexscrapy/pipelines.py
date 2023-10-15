import psycopg2
from vnexscrapy.config import DB_CONFIG, DOMAIN_CONFIG



class DatabasePipeline:

    def __init__(self):
        self.connection = None
        self.cursor = None

        self.create_query_news = """
                        CREATE TABLE IF NOT EXISTS news (
                           id TEXT PRIMARY KEY,
                           title TEXT,
                           source_id TEXT REFERENCES source(id) ON DELETE CASCADE,
                           category_id TEXT REFERENCES category(id) ON DELETE SET NULL,
                           author TEXT,
                           description TEXT,
                           content_html TEXT,
                           content_text TEXT,
                           keywords TEXT
                        );
                        """
        self.create_query_category = """
                        CREATE TABLE IF NOT EXISTS category (
                           id TEXT PRIMARY KEY,
                           title TEXT
                        );
                        """

        self.create_query_source = """
                        CREATE TABLE IF NOT EXISTS source (
                           id TEXT PRIMARY KEY,
                           url TEXT,
                           domain TEXT,
                           title TEXT,
                           publish_date TEXT,
                           last_mod TEXT,
                           author TEXT
                        );
                        """
        self.create_query_config = """
                        CREATE TABLE IF NOT EXISTS config (
                            id TEXT PRIMARY KEY,
                            domain TEXT,
                            news_id_selector TEXT,
                            news_from_list_selector TEXT,
                            news_title_selector TEXT,
                            publish_date_selector TEXT,
                            last_mod_selector TEXT,
                            author_selector TEXT,
                            description_selector TEXT,
                            content_html_selector TEXT,
                            content_text_selector TEXT,
                            keywords_selector TEXT,
                            category_id_selector TEXT,
                            category_url_list_selector TEXT,
                            category_title_selector TEXT,
                            next_page_selector TEXT
                        );
        """



    def open_spider(self, spider):

        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

        self.cursor.execute(self.create_query_category)
        self.cursor.execute(self.create_query_source)
        self.cursor.execute(self.create_query_news)
        self.cursor.execute(self.create_query_config)
        for data in DOMAIN_CONFIG:
            self.insert_data('config', data)


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
            self.insert_data('news',item)
        elif item_class == 'SourceItem':
            self.insert_data('source',item)
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
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

        get_query = f"SELECT * FROM {table_name} WHERE {condition} LIMIT 1;"
        self.cursor.execute(get_query)

        row_data = self.cursor.fetchone()
        column_fields = [desc[0] for desc in self.cursor.description]

        if row_data:
            data = dict(zip(column_fields, row_data))
        return data


