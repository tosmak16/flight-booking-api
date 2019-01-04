import dotenv

dotenv.load()


print(dotenv.get('DB_NAME'))
print(dotenv.get('DB_USER'))
print(dotenv.get('DB_PASSWORD'))
print(dotenv.get('DB_PORT'))

