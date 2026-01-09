import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = {} # Format: {'username': 'hashed_password_string'}
        self.load_users()

    def register(self, username, password):
        if username in self.users:
            return False, "User already exists."
        
        # SECURITY CRITICAL: We hash the password before saving.
        # "pbkdf2:sha256" is a standard industrial hashing algorithm.
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        self.users[username] = password_hash
        self.save_users()
        return True, "User created successfully."

    def verify_user(self, username, password):
        if username not in self.users:
            return False
        
        stored_hash = self.users[username]
        # check_password_hash handles the math to see if the password matches the hash
        return check_password_hash(stored_hash, password)

    def save_users(self):
        with open(self.filename, "w") as f:
            json.dump(self.users, f, indent=4)

    def load_users(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r") as f:
            self.users = json.load(f)
