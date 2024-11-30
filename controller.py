import sys
import random
import time
from flask import Flask, jsonify, request
from auth.auth import checkUsingAuth
#pip install firebase-admin
import firebase_admin
from firebase_admin import db,credentials
from firebase_admin import firestore
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred, {"databaseURL":"https://dadn-241-default-rtdb.asia-southeast1.firebasedatabase.app/"})
from flask_cors import CORS   
app = Flask(__name__)
CORS(app)
from Adafruit_IO import Client,Feed
aio = Client("Binhphan1447", "aio_xCZH123V0tfRUaQps3s3Y5t1x7ZU")
import models.users as User
@app.route('/users', methods=['GET'])
def user_getUsers():#Done
    username = request.args.get('username')
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    if username == None:
        res = User.User.getAllUsers(db)
        if "error" in res.keys():
            return {"error": res["error"], "status": 404}
        return {"users": res["users"], "status": 200}
    else:
        res = User.User.getUserInfo(db,username)
        if "error" in res.keys():
            return {"error": res["error"], "status": 404}
        return {"user": res["user"], "status": 200}

@app.route('/users/register', methods=['POST'])
def user_createUser():#Done
    data = request.get_json()
    res = User.User.createUser(db,data["username"],data["password"],data["name"])
    print(res)
    if "error" in res.keys():
        return {"error": res["error"], "status": 400}
    else:
        return {"user": res["user"], "status": 201}

@app.route('/users/login', methods=['POST'])
def user_login():#Done
    data = request.get_json()
    res = User.User.login(db,data["username"],data["password"])
    print(res)
    if "error" in res.keys():
        return {"error": res["error"], "status": 400}
    else:
        return {"auth": res["auth"], "status": 200}
    
@app.route('/users/edit', methods=['PUT'])
def user_editUser():
    data = request.get_json()
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    if AuthenticatedUsername != data["username"]: return {"error": "Forbidden", "status": 403}
    res = User.User.editUser(db,data["username"],data["password"],data["name"])
    print(res)
    if "error" in res.keys():
        return {"error": res["error"], "status": 400}
    else:
        return {"user": res["user"], "status": 201}
@app.route('/users/delete', methods=['DELETE'])
def user_deleteUser():
    username = request.args.get('username')
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    if AuthenticatedUsername != username: return {"error": "Forbidden", "status": 403}
    res = User.User.deleteUser(db,username)
    print(res)
    if "error" in res.keys():
        return {"error": res["error"], "status": 400}
    else:
        return {"response": res["status"], "status": 201}

import models.sensors as Sensors
# @app.route('/sensors', methods=['GET'])
# def sensor_getSensors():
#     feedname = request.args.get('feedname')
#     auth = request.headers.get('Authorization')
#     AuthenticatedUsername = checkUsingAuth(db,auth)
#     if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
#     if feedname == None:
#         res = Sensors.Sensors.getAllSensors(db)
#         if "error" in res.keys():
#             return {"error": "No sensors found", "status": 404}
#         return {"sensor": res["sensors"], "status": 200}
#     else:
#         res = Sensors.Sensors.getValue(db,feedname,aio)
#         print(res)
#         if "error" in res.keys():
#             return {"error": "No sensors found", "status": 404}
#         else:
#             return {"value": res["value"], "status": 201}
@app.route('/sensors', methods=['GET'])
def sensor_getSensors():
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Sensors.Sensors.getAllSensors(db)
    if "error" in res.keys():
        return {"error": "No sensors found", "status": 404}
    return {"sensor": res["sensors"], "status": 200}
@app.route('/sensors', methods=['POST'])
def sensor_getSensorsWithFeedName():
    feedname = request.get_json()['feedname']
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Sensors.Sensors.getValue(db,feedname,aio)
    print(res)
    if "error" in res.keys():
        return {"error": "No sensors found", "status": 404}
    else:
        return {"value": res["value"], "status": 201}
@app.route('/sensors/add', methods=['POST'])
def sensor_addSensor():
    data = request.get_json()
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Sensors.Sensors.addSensor(db,data["name"],data["key"])
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 400}
    return {"sensor": res["sensor"], "status": 200}

@app.route('/sensors/edit', methods=['PUT'])
def sensor_editSensor():
    data = request.get_json()
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Sensors.Sensors.editSensor(db,data["name"],data["key"])
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 404}
    return {"sensor": res["sensor"], "status": 201}
    
@app.route('/sensors/delete', methods=['DELETE'])
def sensor_deleteSensor():
    feedname = request.args.get('feedname')
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Sensors.Sensors.deleteSensor(db,feedname)
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 404}
    return {"response": res["status"], "status": 200}


@app.route('/devices/set', methods=['POST'])
def device_setValue():
    data = request.get_json()
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    print(AuthenticatedUsername)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Devices.Devices.setValue(db,data["name"],data["value"],AuthenticatedUsername,aio)
    if "error" in res.keys():
        return {"error": "No devices found", "status": 404}
    return {"value": res["value"], "status": 200}

import models.devices as Devices
@app.route('/devices', methods=['GET'])
def device_getDevices():
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Devices.Devices.getAllDevices(db)
    if "error" in res.keys():
        return {"error": "No devices found", "status": 404}
    return {"device": res["devices"], "status": 200}
@app.route('/devices', methods=['POST'])
def device_getDevicesWithFeedName():
    feedname = request.get_json()['feedname']
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Devices.Devices.getValue(db,feedname,aio)
    print(res)
    if "error" in res.keys():
        return {"error": "No devices found", "status": 404}
    else:
        return {"value": res["value"], "status": 201}
@app.route('/devices/add', methods=['POST'])
def device_addDevice():
    data = request.get_json()
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    print(data)
    res = Devices.Devices.addDevice(db,data["name"],data["key"],data["type"],data["valrange"])
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 400}
    return {"device": res["device"], "status": 200}

@app.route('/devices/edit', methods=['PUT'])
def device_editDevice():
    data = request.get_json()
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    print(data)
    res = Devices.Devices.editDevice(db,data["name"],data["key"])
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 404}
    return {"device": res["device"], "status": 201}
    
@app.route('/devices/delete', methods=['DELETE'])
def device_deleteDevice():
    feedname = request.args.get('feedname')
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Devices.Devices.deleteDevice(db,feedname)
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 404}
    return {"response": res["status"], "status": 200}

@app.route('/devices/logs', methods=['GET'])
def device_getLogs():
    feedname = request.args.get('feedname')
    auth = request.headers.get('Authorization')
    AuthenticatedUsername = checkUsingAuth(db,auth)
    if not AuthenticatedUsername: return {"error": "Auth failed", "status": 401}
    res = Devices.Devices.getLogs(db,feedname)
    print(res)
    if "error" in res.keys():
            return {"error": res["error"], "status": 404}
    return {"response": res["logs"], "status": 200}
if __name__ == '__main__':
    app.run(debug=True)
    
