from firebase_admin.exceptions import FirebaseError
import functools
from functools import reduce
from auth.auth import basic_auth

class User:
    
    def createUser(db, username, password, name):
        if db:
            try:
                ref = db.reference('/users/' + username)
                res = ref.get()
                if res != None:
                    return {"error": "user is existed"}
                data = {
                    "username": username,
                    "password": password,
                    "name": name
                }
                ref.set(data)
                return {"status": "created" , "user": data}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    
    def login(db,username,password):
        if db:
            try:
                ref = db.reference('/users')
                query = ref.order_by_key().equal_to(username)
                res = query.get()
                print(res)
                print(username)
                if len(res)==0:
                    return {"error": "No user found"}
                if res[username]["password"] != password:
                    return {"error": "Wrong password"}
                else:
                    return {"auth": basic_auth(username,password)}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "Database not found"}
    
    def getAllUsers(db):
        if db:
            try:
                ref = db.reference('/users')
                res = ref.get()
                if res == None:
                    return {"error": "No user found"}
                print(res)
                return {"users": res}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def editUser(db, username, password, name):
        if db:
            try:
                ref = db.reference('/users/' + username)
                query = ref.order_by_key().equal_to(username)
                res = query.get()
                if res == None:
                    return {"error": "No user found"}
                data = {
                    "username": username,
                    "password": password,
                    "name": name
                }
                ref.set(data)
                return {"user": data}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def getUserInfo(db,username):
        if db:
            try:
                ref = db.reference('/users')
                query = ref.order_by_key().equal_to(username)
                res = query.get()
                if res == None:
                    return {"error": "No user found"}
                return {"user": res}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def deleteUser(db,username):
        if db:
            try:
                ref = db.reference('/users/'+ username)
                res = ref.get()
                print(res)
                if res == None:
                    return {"error": "User not found"}
                ref.delete()
                return {"status": "deleted"}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "Database not found"}