import os

def create_container(name = 'AramusProjectDB', user='Aramus', password='1234', dbname='aramusDB', port=5409):
    command = f"docker run -d --name {name} -e POSTGERS_USER={user} -e POSTGRES_PASSWORD={password} -e POSTGRES_DB={dbname} -p {port}:5432 postgres:15.4"
    print(command)
    try:
        os.system(command)
    except:
        pass

if __name__ == "__main__":
    create_container()