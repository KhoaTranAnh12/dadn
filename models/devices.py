from firebase_admin.exceptions import FirebaseError
import time
from Adafruit_IO import Client, Feed
def separate(input):
    input = input.replace('[','')
    input = input.replace(']','')
    input = input.replace(' ','')
    input = input.split(",")
    return input
class Devices:
    def addDevice(db,feed_name,feed_key,type,valrange):
        if db:
            try:
                #Check if device not exists
                ref = db.reference('/devices/' + feed_name)
                res = ref.get()
                if res != None:
                    return {"error": "device is existed"}
                #Add device by user
                data = {
                    "name": feed_name,
                    "key": feed_key,
                    "type": type,
                    "valrange": valrange
                }
                ref.set(data)
                return {"status": "created" , "device": data}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def deleteDevice(db,feed_name):
        if db:
            try:
                ref = db.reference('/devices/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "device not found"}
                ref.delete()
                return {"status": "deleted"}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def getAllDevices(db):
        if db:
            try:
                ref = db.reference('/devices')
                devices = ref.get()
                if devices:
                    return {"devices": list(devices.values())}
                else:
                    return {"error": "device not found"}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "database not found"}
    def getValue(db,feed_name,aio:Client):
        if db:
            try:
                #Check if device exists
                ref = db.reference('/devices/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "device not found"}
                #Adafruit
                key = res["key"]
                print(key)
                res = aio.receive(key)
                return {"value": res._asdict()["value"]}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "database not found"}
    
    def setValue(db,feed_name,value,username,aio:Client):
        if db:
            try:
                #Check if device exists
                ref = db.reference('/devices/' + feed_name)
                resFeed = ref.get()
                if resFeed == None:
                    return {"error": "device not found"}
                #Adafruit
                if "logs" in resFeed.keys(): print(resFeed["logs"])
                key = resFeed["key"]
                if(not key): return {"error": "device not found"}
                restype = resFeed["type"]
                valrange = resFeed["valrange"]
                if restype == "STR":
                    if value in resFeed["valrange"]:
                        if "logs" in resFeed.keys():
                            if type(resFeed["logs"]) is dict: resFeed["logs"] = list(resFeed["logs"].values())
                            resFeed["logs"].append(
                                {
                                    "value": value,
                                    "username": username,
                                    "timestamp": time.time()
                                }
                            )
                        else:
                            resFeed["logs"] = [{
                                    "value": value,
                                    "username": username,
                                    "timestamp": time.time()
                                }]
                        res = aio.send_data(key,value)
                        return {"value": value}
                else: #restype == "NUMBER"
                    print(resFeed["valrange"])
                    print(separate(resFeed["valrange"]))
                    if int(separate(resFeed["valrange"])[0]) <= value and int(separate(resFeed["valrange"])[1]) >= value:
                        res = aio.send_data(key,value)
                        if "logs" in resFeed.keys():
                            if type(resFeed["logs"]) is dict: resFeed["logs"] = list(resFeed["logs"].values())
                            resFeed["logs"].append(
                                {
                                    "value": value,
                                    "username": username,
                                    "timestamp": time.time()
                                }
                            )
                        else:
                            resFeed["logs"] = [{
                                    "value": value,
                                    "username": username,
                                    "timestamp": time.time()
                                }]
                        ref.set(resFeed)
                        return {"value": value}
                return {"error": "valrange error"}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "database not found"}
    def editDevice(db,feed_name,feed_key,type,valrange):
        if db:
            try:
                #Check if device not exists
                ref = db.reference('/devices/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "device not found"}
                #Add device by user
                data = {
                    "name": feed_name,
                    "key": feed_key,
                    "type": type,
                    "valrange": valrange
                }
                ref.set(data)
                return {"status": "edited" , "device": data}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def deleteDevice(db,feed_name):
        if db:
            try:
                #Check if device not exists
                ref = db.reference('/devices/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "device not found"}
                #Add device by user
                ref.delete()
                return {"status": "deleted"}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    
    def getLogs(db,feed_name):
        if db:
            try:
                #Check if device exists
                ref = db.reference('/devices/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "device not found"}
                return {"logs": res["logs"]}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "database not found"}