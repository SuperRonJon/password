import base64
import copy
import hashlib
import json
import secrets


class Database:
    def __init__(self):
        self.users = dict()

    def add_user(self, username, password):
        salt = self._generate_salt()
        hashed_password = self._generate_hash(password, salt)
        self.users[username] = {'password': hashed_password, 'salt': salt}

    def get_user_salt(self, username):
        try:
            return self.users[username]['salt']
        except KeyError:
            return None

    def authenticate(self, username, password):
        username = username.lower().strip()
        user_salt = self.get_user_salt(username)
        if user_salt:
            hashed_password = self._generate_hash(password, user_salt)
            return hashed_password == self.users[username]['password']
        else:
            return False

    def export_database(self, filename):
        s = json.dumps(self.serialize_users(), indent=4)
        with open(filename, 'w') as f:
            f.write(s)

    def import_database(self, filename):
        with open(filename, 'rb') as f:
            user_data = json.load(f)

        for user in user_data:
            self.users[user] = {'password': bytes.fromhex(user_data[user]['password']),
                                'salt': bytes.fromhex(user_data[user]['salt'])}

    def serialize_users(self):
        user_list = copy.deepcopy(self.users)
        for user in user_list:
            user_list[user]['salt'] = user_list[user]['salt'].hex()
            user_list[user]['password'] = user_list[user]['password'].hex()

        return user_list

    @staticmethod
    def _generate_salt():
        return secrets.token_bytes(16)

    @staticmethod
    def _generate_hash(password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
