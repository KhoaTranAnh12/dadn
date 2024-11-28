from firebase_admin.exceptions import FirebaseError
import time
from Adafruit_IO import Client, Feed

class Sensors:
    def addSensor(db,feed_name,feed_key):
        if db:
            try:
                #Check if sensor not exists
                ref = db.reference('/sensors/' + feed_name)
                res = ref.get()
                if res != None:
                    return {"error": "sensor is existed"}
                #Add sensor by user
                data = {
                    "name": feed_name,
                    "key": feed_key,
                }
                ref.set(data)
                return {"status": "created" , "sensor": data}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def deleteSensor(db,feed_name):
        if db:
            try:
                ref = db.reference('/sensors/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "sensor not found"}
                ref.delete()
                return {"status": "deleted"}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def getAllSensors(db):
        if db:
            try:
                ref = db.reference('/sensors')
                sensors = ref.get()
                if sensors:
                    return {"sensors": list(sensors.values())}
                else:
                    return {"error": "sensor not found"}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "database not found"}
    def getValue(db,feed_name,aio:Client):
        if db:
            try:
                #Check if sensor exists
                ref = db.reference('/sensors/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "sensor not found"}
                #Adafruit
                key = res["key"]
                if not key: return {"error": "sensor not found"}
                res = aio.receive(key)
                return {"value": res._asdict()["value"]}
            except FirebaseError as e:
                print(e)
                return {"error": e}
        else:
            return {"error": "database not found"}
    def editSensor(db,feed_name,feed_key):
        if db:
            try:
                #Check if sensor not exists
                ref = db.reference('/sensors/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "sensor not found"}
                #Add sensor by user
                data = {
                    "name": feed_name,
                    "key": feed_key
                }
                ref.set(data)
                return {"status": "edited" , "sensor": data}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}
    def deleteSensor(db,feed_name):
        if db:
            try:
                #Check if sensor not exists
                ref = db.reference('/sensors/' + feed_name)
                res = ref.get()
                if res == None:
                    return {"error": "sensor not found"}
                #Add sensor by user
                ref.delete()
                return {"status": "deleted"}
            except FirebaseError as e:
                return {"error": e}
        else:
            return {"error": "Database not found"}