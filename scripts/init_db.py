import psycopg2

def create_database(dbname='aramusDB', user='Aramus', password='1234'):#nobody's gonna hack this
    conn = psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE pc_shop")
    print("Database created successfully")

if __name__ == "__main__":
    create_database()