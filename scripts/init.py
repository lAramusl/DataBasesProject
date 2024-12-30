import os

def create_container_and_db(name = 'AramusProjectDB', user='Aramus', password='1234', dbname='pc_shop', port=5432):
    command = f"docker run --name {name} -e POSTGRES_USER={user} -e POSTGRES_PASSWORD={password} -e POSTGRES_DB={dbname} -d -p {port}:{port} postgres:15.4"
    print(command)
    try:
        os.system(command)
    except:
        pass

if __name__ == "__main__":
    create_container_and_db()