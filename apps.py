import os

from flask import Flask, abort, jsonify, make_response, render_template, request
from flask_cors import CORS

import main

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

instance = main.Main()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/init', methods=['POST'])
def test():
    if request.method == 'POST':
        instance.initModel()
        return "OK"


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        mode = request.form['mode']
        input = request.form['input']
        result = instance.predict(mode, input, 2)
        return result


@app.route('/api/id/<string:id>', methods=['GET'])
def apiPredictWithId(id):
    if request.method == 'GET':
        if instance.model is None or instance.standardScaler is None:
            instance.initModel()
        try:
            result = instance.predict("!bsr", id, 1)
        except:
            abort(404)
        return make_response(jsonify(result))


@app.route('/api/hash/<string:hash>', methods=['GET'])
def apiPredictWithHash(hash):
    if request.method == 'GET':
        if instance.model is None or instance.standardScaler is None:
            instance.initModel()
        try:
            result = instance.predict("hash", hash, 1)
        except:
            abort(404)
        return make_response(jsonify(result))


@app.route('/api/leaderboardId/<string:leaderboardId>', methods=['GET'])
def apiPredictWithLeaderboardId(leaderboardId):
    if request.method == 'GET':
        print(f"leaderboardId : {leaderboardId}")
        if instance.model is None or instance.standardScaler is None:
            instance.initModel()
        try:
            result = instance.predict("leaderboardId", leaderboardId, 1)
        except:
            abort(404)
        return make_response(jsonify(result))


@app.route('/api2/id/<string:id>', methods=['GET'])
def api2PredictWithId(id):
    if request.method == 'GET':
        if instance.model is None or instance.standardScaler is None:
            instance.initModel()
        try:
            result = instance.predict("!bsr", id, 2)
        except:
            abort(404)
        return make_response(jsonify(result))


@app.route('/api2/hash/<string:hash>', methods=['GET'])
def api2PredictWithHash(hash):
    if request.method == 'GET':
        if instance.model is None or instance.standardScaler is None:
            instance.initModel()
        try:
            result = instance.predict("hash", hash, 2)
        except:
            abort(404)
        return make_response(jsonify(result))


@app.route('/api2/leaderboardId/<string:leaderboardId>', methods=['GET'])
def api2PredictWithLeaderboardId(leaderboardId):
    if request.method == 'GET':
        print(f"leaderboardId : {leaderboardId}")
        if instance.model is None or instance.standardScaler is None:
            instance.initModel()
        try:
            result = instance.predict("leaderboardId", leaderboardId, 2)
        except:
            abort(404)
        return make_response(jsonify(result))


@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(port=port)
    app.run(host='0.0.0.0', port=port)
