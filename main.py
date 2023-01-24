import io
import pickle
import warnings
from datetime import datetime
from typing import Tuple

import numpy as np
import requests


class FeatureValues:
    bpm: float = 0
    duration: float = 0
    difficulty: int = 0
    sageScore: int = 0
    njs: float = 0
    offset: float = 0
    notes: int = 0
    bombs: int = 0
    obstacles: int = 0
    nps: float = 0
    events: int = 0
    chroma: int = 0
    errors: int = 0
    warns: int = 0
    resets: int = 0

    def __init__(self, bpm: float, duration: int, difficulty: int, sageScore: int, njs: float,
                 offset: float, notes: int, bombs: int, obstacles: int, nps: float, events: int,
                 chroma: int, errors: int, warns: int, resets: int):
        self.bpm = bpm
        self.duration = duration
        self.difficulty = difficulty
        self.sageScore = sageScore
        self.njs = njs
        self.offset = offset
        self.notes = notes
        self.bombs = bombs
        self.obstacles = obstacles
        self.nps = nps
        self.events = events
        self.chroma = chroma
        self.errors = errors
        self.warns = warns
        self.resets = resets

    def array(self) -> np.ndarray:
        return np.array([self.bpm, self.duration, self.difficulty, self.sageScore, self.njs,
                         self.offset, self.notes, self.bombs, self.obstacles, self.nps, self.events,
                         self.chroma, self.errors, self.warns, self.resets])


class Main:
    model: object = None
    initModelHour: int = 0

    def initModel(self) -> None:
        try:
            warnings.simplefilter('ignore', UserWarning)

            self.initModelHour = datetime.now().hour

            print("Loading model")
            self.model = self.loadModel()

        except Exception as e:
            print(e)
            raise Exception(e)

    def predict(self, mode: str, input: str, apiVersion: int) -> dict:
        self.confirmModel()

        print("Select input mode")
        print("Selected : " + mode)

        try:
            mapDetail, response = self.getMapData(input, mode)
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

    def loadModel(self) -> object:
        # モデルのオープン
        # with open('model.pickle', mode='rb') as f:
        #   self.model = pickle.load(f)

        modelAssetEndpoint = "https://api.github.com/repos/rakkyo150/PredictStarNumberHelper/releases/latest"
        modelAssetResponse = requests.get(url=modelAssetEndpoint)
        modelJson = modelAssetResponse.json()
        secondHeaders = {'Accept': 'application/octet-stream'}
        modelResponse = requests.get(url=modelJson["assets"][3]["browser_download_url"],
                                     headers=secondHeaders)
        model = pickle.load(io.BytesIO(modelResponse.content))
        return model

    def confirmModel(self) -> None:
        if self.model is None or self.initModelHour != datetime.now().hour:
            self.initModel()

    def getMapData(self, input: str, mode: str) -> Tuple[dict, requests.Response]:
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
        return mapDetail, response

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

        featureValues = FeatureValues(bpm, duration, difficulty, sageScore, njs, offset, notes,
                                      bombs, obstacles, nps, events, chroma, errors, warns, resets)

        numpyList = []
        numpyList.append(featureValues.array())
        print(numpyList)

        return characteristic, numpyList
