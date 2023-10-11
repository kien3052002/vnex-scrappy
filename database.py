from scrapy.utils.project import get_project_settings

import psycopg2


class Database:

    def __init__(self):
        con = self.db_connection()
        cursor = con.cursor()
        create_query = """
                CREATE TABLE IF NOT EXISTS news (
                   id TEXT PRIMARY KEY,
                   source TEXT,
                   title TEXT,
                   category TEXT,
                   author TEXT,
                   publish_date TEXT,
                   last_mod TEXT,
                   description TEXT,
                   content TEXT
                );
                """
        cursor.execute(create_query)
        con.commit()
        cursor.close()
        con.close()

    def db_connection(self):
        connection = psycopg2.connect(
            database='vnexpress',
            user='postgres',
            password='30052002',
            host='localhost',
            port='5432',
        )
        return connection

    def insert_news(self, news_item):
        # connection = psycopg2.connect(get_project_settings().get('CONNECTION_STRING'))
        con = self.db_connection()
        cursor = con.cursor()

        insert_query = """
                        INSERT INTO news (id, source, title, category, author, publish_date, last_mod, description, content)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET 
                        source = EXCLUDED.source,
                        title = EXCLUDED.title,
                        category = EXCLUDED.category,
                        author = EXCLUDED.author,
                        publish_date = EXCLUDED.publish_date,
                        last_mod = EXCLUDED.last_mod,
                        description = EXCLUDED.description,
                        content = EXCLUDED.content;
                        """
        data = (
            news_item['id'],
            news_item['source'],
            news_item['title'],
            news_item['category'],
            news_item['author'],
            news_item['publish_date'],
            news_item['last_mod'],
            news_item['description'],
            news_item['content'],
        )

        cursor.execute(insert_query, data)
        con.commit()

        cursor.close()
        con.close()
