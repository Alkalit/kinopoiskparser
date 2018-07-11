import sqlite3

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

def main():
    database_path = './parser.db'

    sql_create_film_table = """
        CREATE TABLE IF NOT EXISTS projects (
            id integer PRIMARY KEY,
            name text NOT NULL,
            url text NOT NULL,
            like text NOT NULL,
            dislike integer NOT NULL
        );
    """

    conn = create_connection(database_path)
    if conn is not None:
        create_table(conn, sql_create_film_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
