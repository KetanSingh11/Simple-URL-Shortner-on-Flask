from user import User

def authenticate(username, password):
    print("called: authenticate once...")
    user = User.find_user_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    print("called: payload...")
    print("payload=", payload)
    user_id = payload['identity']
    return User.find_user_by_id(user_id)
