import sqlite3
import requests
from bs4 import BeautifulSoup

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
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

    response = requests.get(link)
    bs = BeautifulSoup(response.content, 'html.parser')

    name = bs.find('h1', {'class': 'moviename-big'}).text
    likes = bs.find('li', {'class': 'pos'}).find('b').text
    dislikes = bs.find('li', {'class': 'neg'}).find('b').text

    return (name, link, int(likes), int(dislikes))

def main():
    database_path = './parser.db'

    sql_create_film_table = """
        CREATE TABLE IF NOT EXISTS film (
            id integer PRIMARY KEY,
            name text NOT NULL,
            url text NOT NULL,
            like text NOT NULL,
            dislike integer NOT NULL
        );
    """

    conn = create_connection(database_path)
    cursor = conn.cursor()
    if conn is not None:
        create_table(conn, sql_create_film_table)
    else:
        print("Error! cannot create the database connection.")

    links = get_links()

    for link in links:
        name, link, likes, dislikes = parse_a_page(link)
        print(name, link, likes, dislikes) # TODO logging
        cursor.execute("INSERT INTO film (name, url, like, dislike) VALUES (?,?, ?,?)", [name, link, likes, dislikes])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
