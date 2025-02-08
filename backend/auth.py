import bcrypt
from database import users_collection

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def register_user(name, email, password):
    # Check if email already exists
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        print("⚠️ User already exists!")
        return False

    hashed_password = hash_password(password)
    user = {"name": name, "email": email, "password": hashed_password}
    
    print("✅ Registering user:", user)  # Debugging line
    users_collection.insert_one(user)
    print("✅ User saved to MongoDB!")  # Debugging line
    return True

def login_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user
    return None