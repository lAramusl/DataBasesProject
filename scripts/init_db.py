import os
import psycopg2
import time

def create_container_and_db(name = 'AramusProjectDB', user='Aramus', password='1234', dbname='pc_shop', port=5432):
    command = (f'docker run --name {name} -e POSTGRES_USER={user} -e'
      f'POSTGRES_PASSWORD={password} -e POSTGRES_DB={dbname} -d -p {port}:{port} postgres:15.4')
    print(command)
    try:
        os.system(command)
    except:
        print("Could not create a container")

def create_tables():
    conn = psycopg2.connect(
        dbname = "pc_shop",
        user = "Aramus",
        password = "1234",
        host = 'localhost',
        port = '5432'
    )

    conn.autocommit = True

    cursor = conn.cursor()

    cursor.execute(
                    'CREATE TABLE Laptop('
                    'id SERIAL NOT NULL PRIMARY KEY, '
                    'Model VARCHAR(20) NOT NULL, '
                    'CPU VARCHAR(20) NOT NULL, '
                    'GPU VARCHAR(20) NOT NULL, '
                    'RAM VARCHAR(20) NOT NULL, '
                    'ScreenSize VARCHAR(10) NOT NULL, '
                    'Matrix VARCHAR(10) NOT NULL);'
                    )
    print("Laptop added")

    cursor.execute(
                   'CREATE TABLE Producer('
                   'id SERIAL NOT NULL PRIMARY KEY,'
                   'Name Text NOT NULL,'
                   'Country Text NOT NULL,'
                   'Placement Text,'
                   'Warranty Boolean);'
                   )
    print("Producer added")

    cursor.execute(
                   'CREATE TABLE MarketOffer('
                   'id SERIAL NOT NULL PRIMARY KEY,'
                   'LaptopID INT NOT NULL references Laptop(id),'
                   'ProducerID INT NOT NULL references Producer(id),'
                   'Price FLOAT NOT NULL,'
                   'Date TIMESTAMP NOT NULL);'
                   )
    print("MarketOffer added")

if __name__ == "__main__":
    create_container_and_db()
    time.sleep(2)
    create_tables()