from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import time
import json
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_krabbypatty_sauce'
socketio = SocketIO(app)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# Webserver Routes


@app.route('/')
def intializeIndex():
    return render_template('index.html', async_mode=socketio.async_mode)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

# Socket Functions


@socketio.on('connect')
def client_connect():
    print('Client Successfully Connected')


@socketio.on('PROCESS_CHARTING_COMMAND')
def processChartingRequest(jsonPayload):
    print('Receive Charting Request : ' + str(jsonPayload))
    maxTime = jsonPayload['maxTime']
    print('Recieved Data : ' + str(jsonPayload))
    print('Transforming Data : ', type(jsonPayload))
    x = 0
    while x < int(maxTime):
        socketio.sleep(0)
        df = generateRandomHeat(10,10)
        print("Emitting Event")
        emit('RESPONSE_EVENT', str(df))
        time.sleep(0.5)
        x += 1
    print('Finished Processing Event Request: ' + str(jsonPayload))

def generateData(count):
    x = 0
    i = 0
    dataSeries = []
    while i != count:
        iterText = 'x'+str(i)
        myRanVal = np.random.randint(100)
        dataSeries.append({"x":iterText,"y":myRanVal})
        i+=1
    return dataSeries

def generateRandomHeat(count,dataValCount):
    i=0
    seriesData = []
    while i != count:
        heatVal = {"name":"S"+str(i),"data":generateData(dataValCount)}
        seriesData.append(heatVal)
        i+=1
    return {"payload":seriesData}
        

@socketio.on('disconnect')
def client_disconnect():
    print('Client Successfully Disconnected')


# Generate the Sever Initialization
if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=6984, host="127.0.0.1", debug=True)
