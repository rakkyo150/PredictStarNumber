import os

from flask import Blueprint, Flask, abort, jsonify, make_response, render_template, request
from flask_cors import CORS
from flask_restx import Api, Resource
from markupsafe import escape

import main

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.json.sort_keys = False
CORS(app)
api_bp = Blueprint("api2", __name__, url_prefix="/api2/")
description = "PredictStarNumber API\n" \
              "GitHub : https://github.com/rakkyo150/PredictStarNumber\n" \
              "Training Data : https://github.com/rakkyo150/RankedMapData\n" \
              "Model : https://github.com/rakkyo150/PredictStarNumberHelper\n" \
              "Mod : https://github.com/rakkyo150/PredictStarNumberMod\n" \
              "Chrome Extension : https://github.com/rakkyo150/PredictStarNumberExtension"
api = Api(api_bp, version='1.2.1', title="PredictStarNumber", description=description, doc='/doc',
          default="Main", default_label="Main API", base_url='/',
          license_url="https://github.com/rakkyo150/PredictStarNumber/blob/master/LICENSE")
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
        result = instance.predict(escape(mode), escape(input), 2)
        return result


@api.route('/id/<string:id>')
@api.doc(params={'id': 'map id(!bsr)'})
class Api2Id(Resource):
    @api.doc(responses={200: "Success", 404: "Error"})
    def get(self, id):
        if request.method == 'GET':
            try:
                result = instance.predict("!bsr", id, 2)
                result_json = {item[0]: item[1] for item in result}
            except:
                abort(404)
            return make_response(jsonify(result_json))


@api.route('/hash/<string:hash>')
@api.doc(params={'hash': 'map hash'})
class Api2Hash(Resource):
    @api.doc(responses={200: "Success", 404: "Error"})
    def get(self, hash):
        if request.method == 'GET':
            try:
                result = instance.predict("hash", hash, 2)
                result_json = {item[0]: item[1] for item in result}
            except:
                abort(404)
            return make_response(jsonify(result_json))


@api.route('/leaderboardId/<string:leaderboardId>')
@api.doc(params={'leaderboardId': 'score saber leaderboard id'})
class Api2LeaderboardId(Resource):
    @api.doc(responses={200: "Success", 404: "Error"})
    def get(self, leaderboardId):
        if request.method == 'GET':
            try:
                result = instance.predict("leaderboardId", leaderboardId, 2)
                result_json = {item[0]: item[1] for item in result}
            except:
                abort(404)
            return make_response(jsonify(result_json))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # For local run, comment out above code and uncomment below code
    # app.run(port=port)
