import os

from flask import Blueprint, Flask, abort, jsonify, make_response, render_template, request
from flask_cors import CORS
from flask_restx import Api, Resource

import main

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)
api_bp = Blueprint("api2", __name__, url_prefix="/api2/")
api = Api(api_bp, version='1.2.0', doc='/doc', base_url='/')
app.register_blueprint(api_bp)

instance = main.Main()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/init', methods=['POST'])
def init():
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


@api.route('/id/<string:id>')
@api.doc(params={'id': 'map id(!bsr)'})
class Api2Id(Resource):
    def get(self, id):
        if request.method == 'GET':
            if instance.model is None or instance.standardScaler is None:
                instance.initModel()
            try:
                result = instance.predict("!bsr", id, 2)
            except:
                abort(404)
            return make_response(jsonify(result))


@api.route('/hash/<string:hash>')
@api.doc(params={'hash': 'map hash'})
class Api2Hash(Resource):
    def get(self, hash):
        if request.method == 'GET':
            if instance.model is None or instance.standardScaler is None:
                instance.initModel()
            try:
                result = instance.predict("hash", hash, 2)
            except:
                abort(404)
            return make_response(jsonify(result))


@api.route('/leaderboardId/<string:leaderboardId>')
@api.doc(params={'leaderboardId': 'score saber leaderboard id'})
class Api2LeaderboardId(Resource):
    def get(self, leaderboardId):
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
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(port=port)
    app.run(host='0.0.0.0', port=port)
