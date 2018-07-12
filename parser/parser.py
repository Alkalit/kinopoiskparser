import threading
import logging
import sqlite3
import requests

from bs4 import BeautifulSoup

DATABASE_PATH = 'parser.db'
DB_LOCK = threading.Lock()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def get_links():

    url = 'https://www.kinopoisk.ru/top/'

    response = requests.get(url)
    bs = BeautifulSoup(response.content, 'html.parser')

    arr = bs.select('table.js-rum-hero a.all')
    return [''.join(['https://www.kinopoisk.ru', tag.attrs['href']]) for tag in arr]

def parse_a_page(link):

    conn = create_connection(DATABASE_PATH)
    cursor = conn.cursor()

    response = requests.get(link)
    bs = BeautifulSoup(response.content, 'html.parser')

    name = bs.find('h1', {'class': 'moviename-big'}).text
    likes = bs.find('li', {'class': 'pos'}).find('b').text
    dislikes = bs.find('li', {'class': 'neg'}).find('b').text

    logging.debug('inserting {} {} {} {} into the DB'.format(name, link, likes, dislikes))

    with DB_LOCK:
        cursor.execute("INSERT INTO film (name, url, like, dislike) VALUES (?,?, ?,?)", [name, link, int(likes), int(dislikes)])
        conn.commit()
        conn.close()

def initialte_db():

    sql_create_film_table = """
        CREATE TABLE IF NOT EXISTS film (
            id integer PRIMARY KEY,
            name text NOT NULL,
            url text NOT NULL,
            like text NOT NULL,
            dislike integer NOT NULL
        );
    """

    conn = create_connection(DATABASE_PATH)
    cursor = conn.cursor()

    if conn is not None:
        create_table(conn, sql_create_film_table)
    else:
        print("Error! cannot create the database connection.")

def main():

    initialte_db()

    links = get_links()

    threads = []

    for link in links:

        thread = threading.Thread(target=parse_a_page, args=(link,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
