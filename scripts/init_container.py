import os

def create_container(name = 'AramusProjectDB', user='Aramus', password='1234', dbname='aramusDB', port=5432):
    command = f"docker run --name {name} -e POSTGERS_USER={user} -e POSTGRES_PASSWORD={password} -e POSTGRES_DB={dbname} -d -p {port}:{port} postgres:15.4"
    print(command)
    try:
        os.system(command)
    except:
        pass

if __name__ == "__main__":
    create_container()