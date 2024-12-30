import psycopg2

def create_database(dbname='aramusDB', user='Aramus', password='1234'):#nobody's gonna hack this
    conn = psycopg2.connect(
        dbname = 'postgres',
        user = user,
        password = password,
        host = 'localhost',
        port = '5432'
    )

    conn.autocommit = True

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE pc_shop")
    print("Database created successfully")

if __name__ == "__main__":
    create_database()