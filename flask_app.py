from flask import Flask,request, jsonify,render_template
from datetime import datetime,timezone,timedelta
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/',methods=["GET"])
def hello_world():
    return render_template("chart2.html")

@app.route('/api',methods=["POST"])
def api():
    data = request.get_json()
    if 'timestamp' in data and 'temperature' in data and 'humidity' in data and 'pressure' in data:
        #time = data['timestamp'
        tz = timezone(timedelta(hours=+5.5))
        utc = datetime.now(timezone.utc)
        lt = utc.astimezone(tz)
        time = lt.strftime("%Y-%m-%d %H:%M:%S")
        temp = data['temperature']
        humi = data['humidity']
        pres = data['pressure']
        with open('data.txt', 'a') as file:
            file.write(f'{time},{temp},{humi},{pres}\n')
        return jsonify({'message': 'Data stored successfully'})
    else:
        return jsonify({'error': 'Invalid request, missing key1 or key2'}), 400
@app.route('/realtime_api',methods=["POST"])
def realtime_api():
    data = request.get_json()
    if 'temperature' in data and 'humidity' in data and 'pressure' in data:
        temp = data['temperature']
        humi = data['humidity']
        pres = data['pressure']
        with open('realtime_data.txt', 'w') as file:
            file.write(f'{temp},{humi},{pres}')
        return jsonify({'message': 'Data stored successfully'})
    else:
        return jsonify({'error': 'Invalid request, missing key1 or key2'}), 400

@app.route('/get_realtime_data',methods=["GET"])
def get_realtime_data():
    f = open("realtime_data.txt","r")
    for line in f:
        r=line.strip().split(",")
    return jsonify(r)

@app.route('/get_time')
def get_time():
    tz = timezone(timedelta(hours=+5.5))
    utc = datetime.now(timezone.utc)
    lt = utc.astimezone(tz)
    ft = lt.strftime("%Y-%m-%d %H:%M:%S")
    return ft

@app.route('/get_data',methods=["GET"])
def get_data():
    f = open("data.txt","r")
    d=[]
    if not request.args:
        for line in f:
            r=line.strip().split(",")
            d.append(r)
    if 'date' in request.args:
        for line in f:
            row = line.strip().split(",")
            if(row[0][0:10]==request.args["date"]):
                d.append(row)
    return jsonify(d)