from scrapy.utils.project import get_project_settings

import psycopg2
from db_config import DB_CONFIG


class Database:

    def __init__(self):
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        create_query_news = """
                CREATE TABLE IF NOT EXISTS news (
                   id TEXT PRIMARY KEY,
                   source TEXT,
                   title TEXT,
                   category_id TEXT REFERENCES category(id) ON DELETE SET NULL,
                   author TEXT,
                   publish_date TEXT,
                   last_mod TEXT,
                   description TEXT,
                   content TEXT
                );
                """
        create_query_category = """
                CREATE TABLE IF NOT EXISTS category (
                   id TEXT PRIMARY KEY,
                   title TEXT
                );
                """
        cursor.execute(create_query_category)
        cursor.execute(create_query_news)
        connection.commit()
        cursor.close()
        connection.close()

    def insert_category(self, category_item):
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        insert_query = """INSERT INTO category (id, title) VALUES(%s, %s) ON CONFLICT (id) DO UPDATE SET 
                        title = EXCLUDED.title;"""
        data = (
            category_item['id'],
            category_item['title'],
        )

        cursor.execute(insert_query, data)
        connection.commit()

        cursor.close()
        connection.close()

    def insert_news(self, news_item):
        # connection = psycopg2.connect(get_project_settings().get('CONNECTION_STRING'))
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        insert_query = """
                        INSERT INTO news (id, source, title, category_id, author, publish_date, last_mod, description, content)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET 
                        source = EXCLUDED.source,
                        title = EXCLUDED.title,
                        category_id = EXCLUDED.category_id,
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
            news_item['category_id'],
            news_item['author'],
            news_item['publish_date'],
            news_item['last_mod'],
            news_item['description'],
            news_item['content'],
        )

        cursor.execute(insert_query, data)
        connection.commit()

        cursor.close()
        connection.close()
