
from firebase_admin.exceptions import FirebaseError
from base64 import b64encode,b64decode

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'
def checkUsingAuth(db, token):
    try:
        print(token)
        info = b64decode(token.split(' ')[1].encode("utf-8")).decode("ascii")
        info = info.split(':')
        if db:
            try:
                ref = db.reference('/users/' + info[0])
                res = ref.get()
                if res == None: return False
                if res ["password"] != info[1]:
                    return False
                return info[0]
            except FirebaseError as e: return False
        else: return False
    except: return False