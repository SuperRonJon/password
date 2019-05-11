from database import Database

db = Database()
db_file = 'database.json'

try:
    db.import_database(db_file)
except FileNotFoundError:
    print(f'Database file at {db_file} not found. Creating empty database.')

while True:
    value = input("a. Login b. Add new user\n").lower()
    if value == 'a':
        username = input('username: ')
        password = input('password: ')

        if db.authenticate(username, password):
            print('Successfully logged in!')
        else:
            print('Incorrect information')

    elif value == 'b':
        username = input('username: ')
        password = input('password: ')
        db.add_user(username, password)

    else:
        break

db.export_database('database.json')
