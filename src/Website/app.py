from flask import Flask, render_template, send_from_directory, jsonify
import os
from flask import send_from_directory, request, redirect, flash, url_for
from uuid import uuid1
import json
from base64 import b64encode, b64decode, standard_b64encode
import requests
import folium
import pandas as pd
import networkx as nx
import random
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.secret_key = "secret key"
# run_with_ngrok(app)

TOKEN = b'dapica13e60df813d4b71e44cda8dda888a9'
headers = {"Authorization": b"Basic " + standard_b64encode(b"token:" + TOKEN)}
url = "https://eastus.azuredatabricks.net/api/2.0"
dbfs_dir = "dbfs:/FileStore/fben_itzik/Upload/"
ALLOWED_SCHEMA = ['_id', 'delay', 'congestion', 'lineId', 'vehicleId', 'timestamp', 'areaId', 'areaId1', 'areaId2',
                  'areaId3', 'gridID', 'actualDelay', 'longitude', 'latitude', 'currentHour', 'dateTypeEnum', 'angle',
                  'ellapsedTime', 'vehicleSpeed', 'distanceCovered', 'journeyPatternId', 'direction', 'busStop',
                  'poiId', 'poiId2', 'systemTimestamp', 'calendar', 'filteredActualDelay', 'atStop', 'dateType',
                  'justStopped', 'justLeftStop', 'probability', 'anomaly', 'loc']


stations = pd.read_csv("NTA_Public_Transport.csv")
station_ids = {}
station_graph: nx.Graph = None


@app.route('/')
def cows():
    return render_template('cows.html')


@app.route('/home')
def index():
    stations = pd.read_csv("NTA_Public_Transport.csv")
    station_list = list(stations['stop_name'])
    return render_template('index.html', stations=station_list)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def perform_query(path, data):
    session = requests.Session()
    resp = session.request('POST', url + path, data=json.dumps(data), verify=True, headers=headers)
    return resp.json()


def write_file(local_file, dbfs_path, overwrite):
    handle = perform_query('/dbfs/create', data={'path': dbfs_path, 'overwrite': overwrite})['handle']
    while True:
        contents = local_file.read(2**20)
        if len(contents) == 0:
            break
        perform_query('/dbfs/add-block', data={'handle': handle, 'data': b64encode(contents).decode()})
    perform_query('/dbfs/close', data={'handle': handle})


@app.route('/home', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            files = request.files['files']
            fileb = request.files['fileb']
            file = fileb if files.filename == '' else files
            print(file)
            row_dict = json.loads(file.readline())
            if file and all(key in row_dict.keys() for key in ALLOWED_SCHEMA):
                filename = str(uuid1())
                print('uploading')
                write_file(local_file=file, dbfs_path=dbfs_dir + filename, overwrite=True)
                flash("File successfully uploaded to DataBricks File System!", 'success')
                # else:
                #     flash("File failed to upload: " + resp, 'error')
                return redirect(url_for('index'))
            else:
                flash(f"Invalid schema. Please put it in this form: {ALLOWED_SCHEMA}", 'error')
                return redirect(request.url)
        except Exception as e:
            flash('Please try again', 'error')
            print(f"Error: {e}")
        return redirect(request.url)
    return redirect(url_for('index'))


@app.route('/map')
def create_map():
    print(request.args)
    loc_name = request.args.get('current_location')
    dest_name = request.args.get('destination')
    loc = stations[stations['stop_name'] == loc_name][['Y', 'X', 'stop_name']].head(1).to_numpy()[0]
    dest = stations[stations['stop_name'] == dest_name][['Y', 'X', 'stop_name']].head(1).to_numpy()[0]
    start_coords = (53.346392, -6.270854)
    folium_map = folium.Map(location=start_coords, zoom_start=9)
    for geo in [loc, dest]:
        folium.Marker(
            location=geo[:2].tolist(),
            popup=geo[2],
            tooltip=geo[2]
        ).add_to(folium_map)
    table = ''
    paths = nx.all_shortest_paths(station_graph, source=station_ids[loc_name], target=station_ids[dest_name])
    path_w = nx.shortest_path(station_graph, source=station_ids[loc_name], target=station_ids[dest_name],
                               weight='Distance')
    routes = set()
    for path in ([path_w] + list(paths))[:10]:
        pg = nx.path_graph(path)
        route = []
        for e in pg.edges():
            route.append(','.join(station_graph.edges[e[0], e[1]]['Routes'].split(', ')[:3]))
        routes.add(' -> '.join(route))
    for route in routes:
        table += f'<tr><td class="w3-center">{route}</td><td class="w3-center">' \
                 f'{int((random.random() - 0.2) * 300)} seconds</td></tr>'
    return jsonify({'map': folium_map._repr_html_(), 'table': table})


def make_station_graph():
    global station_graph
    station_routes = pd.read_csv('NTA_Public_Transport_Routes.csv',
                                 dtype={'Stop 1 Code': int, 'Stop 2 Code': int, 'Stop 1 Name': str,
                                        'Stop 2 Name': str, 'Distance': float})
    station_graph = nx.from_pandas_edgelist(station_routes, source='Stop 1 Code', target='Stop 2 Code',
                                            edge_attr=['Distance', 'Routes'])
    for _, row in stations.iterrows():
        station_ids[row['stop_name']] = int(row['stop_code'])


if __name__ == '__main__':
    make_station_graph()
    app.run()
