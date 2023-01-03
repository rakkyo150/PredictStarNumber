import io
import pickle
import warnings
from datetime import datetime
from typing import Tuple

import numpy as np
import requests


class Main:
    model = None
    standardScaler = None
    initModelHour: int = 0

    def initModel(self) -> None:
        try:
            warnings.simplefilter('ignore', UserWarning)

            self.initModelHour = datetime.now().hour

            print("Loading model")
            modelAssetEndpoint = "https://api.github.com/repos/rakkyo150/PredictStarNumberHelper/releases/latest"
            modelAssetResponse = requests.get(url=modelAssetEndpoint)
            modelJson = modelAssetResponse.json()
            secondHeaders = {'Accept': 'application/octet-stream'}
            modelResponse = requests.get(url=modelJson["assets"][2]["browser_download_url"],
                                         headers=secondHeaders)
            self.model = pickle.load(io.BytesIO(modelResponse.content))

            # モデルのオープン
            # with open('model.pickle', mode='rb') as f:
            #   self.model = pickle.load(f)

            print("Loading standardScaler")
            standardScalerAssetEndpoint = "https://api.github.com/repos/rakkyo150/PredictStarNumberHelper/releases/latest"
            standardScalerResponse = requests.get(url=standardScalerAssetEndpoint)
            standardScalerJson = standardScalerResponse.json()
            secondHeaders = {'Accept': 'application/octet-stream'}
            standardScalerResponse = requests.get(
                url=standardScalerJson["assets"][4]["browser_download_url"],
                headers=secondHeaders)

            self.standardScaler = pickle.load(io.BytesIO(standardScalerResponse.content))

            print(self.standardScaler)

            # モデルのオープン
            # with open('standardScaler.pickle', mode='rb') as f:
            #     self.standardScaler = pickle.load(f)

        except Exception as e:
            print(e)
            raise Exception(e)

    def predict(self, mode: str, input: str, apiVersion: int) -> dict:
        if self.model is None or self.standardScaler is None or \
                self.initModelHour != datetime.now().hour:
            self.initModel()

        print("Select input mode number")
        print("1:!bsr 2:hash")

        print(mode)

        try:
            if mode == "!bsr":
                print("Input !bsr")
                bsr = input
                response = requests.get(f'https://api.beatsaver.com/maps/id/{bsr}')
            elif mode == "leaderboardId":
                print("Input leaderboardId")
                leaderboardId = input
                scoreSaberResponse = requests.get(
                    f'https://scoresaber.com/api/leaderboard/by-id/{leaderboardId}/info')
                sSResponseJson = scoreSaberResponse.json()
                hash = sSResponseJson["songHash"]
                response = requests.get(f'https://api.beatsaver.com/maps/hash/{hash}')
            else:
                print("Input hash")
                hash = input
                response = requests.get(f'https://api.beatsaver.com/maps/hash/{hash}')

            mapDetail = response.json()
            result = {}

            if response.status_code == 404:
                print(f"{response.status_code} Not Found: {mapDetail['id']}-{mapDetail['name']}")
                pass

            else:
                result = self.UseModel(apiVersion, mapDetail)
            return result

        except Exception as e:
            print(e)
            raise Exception(e)

    def UseModel(self, apiVersion: int, mapDetail: dict) -> dict:
        predictResult = {}

        mapDifficulty = mapDetail["versions"][-1]["diffs"]
        for k in mapDifficulty:
            characteristic, numpyList = self.extractFeatureValues(k, mapDetail)

            ans = self.model.predict(numpyList)
            # type(ans) -> numpy.ndarray
            # []に予測値だけが入った形で返ってくる

            print(ans)
            floatStarNumber = float(ans[0])
            roundStarNumber = round(floatStarNumber, 2)

            if apiVersion == 1:
                predictResult.setdefault(k["difficulty"], roundStarNumber)
            elif apiVersion == 2:
                predictResult.setdefault(f'{characteristic}-{k["difficulty"]}', roundStarNumber)

        return predictResult

    def extractFeatureValues(self, k: dict, mapDetail: dict) -> Tuple[str, list]:
        bpm = mapDetail["metadata"]["bpm"]
        duration = mapDetail["metadata"]["duration"]
        if "sageScore" in mapDetail["versions"][-1]:
            sageScore = mapDetail["versions"][-1]["sageScore"]
        else:
            print("sageScore is null")
            sageScore = 0
        difficulty = k["difficulty"]
        if difficulty == "Easy":
            difficulty = 0
        elif difficulty == "Normal":
            difficulty = 1
        elif difficulty == "Hard":
            difficulty = 2
        elif difficulty == "Expert":
            difficulty = 3
        elif difficulty == "ExpertPlus":
            difficulty = 4
        njs = k["njs"]
        offset = k["offset"]
        notes = k["notes"]
        bombs = k["bombs"]
        obstacles = k["obstacles"]
        nps = k["nps"]
        characteristic = k["characteristic"]
        events = k["events"]
        chroma = k["chroma"]
        if chroma is True:
            chroma = 1
        else:
            chroma = 0
        errors = k["paritySummary"]["errors"]
        warns = k["paritySummary"]["warns"]
        resets = k["paritySummary"]["resets"]
        # predictに渡すときのnumpyArrayは[]で括っている必要あり
        numpyList = []
        numpyArray = np.array(
            [bpm, duration, difficulty, sageScore, njs, offset, notes, bombs,
             obstacles,
             nps, events, chroma, errors, warns, resets])
        standardizedNumpyArray = (numpyArray - self.standardScaler.mean_) / np.sqrt(
            self.standardScaler.var_)
        numpyList.append(standardizedNumpyArray)
        print(numpyList)
        return characteristic, numpyList
