import io
import pickle
import warnings

import pandas as pd
import requests


class Main:
    clf = None
    df = None

    def initModel(self) -> None:
        warnings.simplefilter('ignore', UserWarning)

        print("Loading model")
        modelAssetEndpoint = "https://api.github.com/repos/rakkyo150/PredictStarNumberHelper/releases/latest"
        modelAssetResponse = requests.get(url=modelAssetEndpoint)
        modelJson = modelAssetResponse.json()
        secondHeaders = {'Accept': 'application/octet-stream'}
        modelResponse = requests.get(url=modelJson["assets"][3]["browser_download_url"],
                                     headers=secondHeaders)

        Main.clf = pickle.load(io.BytesIO(modelResponse.content))

        # モデルのオープン
        # with open('model.pickle', mode='rb') as f:
        #   clf = pickle.load(f)

        print("loading meanStd")
        meanStdAssetEndpoint = "https://api.github.com/repos/rakkyo150/PredictStarNumberHelper/releases/latest"
        meanStdResponse = requests.get(url=meanStdAssetEndpoint)
        meanStdJson = meanStdResponse.json()
        secondHeaders = {'Accept': 'application/octet-stream'}
        meanStdResponse = requests.get(url=meanStdJson["assets"][2]["browser_download_url"],
                                       headers=secondHeaders)

        Main.df = pd.read_csv(io.BytesIO(meanStdResponse.content), sep=",", index_col=0)

        # df = pd.read_csv("meanStd.csv",index_col=0)

        '''
        print("Loading modelScore")
        modelScoreAssetEndpoint="https://api.github.com/repos/rakkyo150/PredictStarNumberHelper/releases/latest"
        modelScoreResponse=requests.get(url=modelScoreAssetEndpoint)
        modelScoreJson=modelScoreResponse.json()
        secondHeaders={'Accept': 'application/octet-stream' }
        modelScoreResponse=requests.get(url=modelScoreJson["assets"][3]["browser_download_url"],headers=secondHeaders)
        trainScore=modelScoreResponse.json()["trainScore"]
        testScore=modelScoreResponse.json()["testScore"]
        print(trainScore)
        print(testScore)
        '''

    def predict(self, mode: str, input: str, apiVersion: int) -> dict:
        print("Select input mode number")
        print("1:!bsr 2:hash")

        print(mode)

        if mode == "!bsr":
            print("Input !bsr")
            bsr = input
            response = requests.get(f'https://api.beatsaver.com/maps/id/{bsr}')
        elif mode =="leaderboardId":
            print("Input leaderboardId")
            leaderboardId = input
            scoreSaberResponse=requests.get(f'https://scoresaber.com/api/leaderboard/by-id/{leaderboardId}/info')
            sSResponseJson=scoreSaberResponse.json()
            hash=sSResponseJson["songHash"]
            response=requests.get(f'https://api.beatsaver.com/maps/hash/{hash}')
        else:
            print("Input hash")
            hash = input
            response = requests.get(f'https://api.beatsaver.com/maps/hash/{hash}')


        # result=""
        result = {}

        mapDetail = response.json()

        if response.status_code == 404:
            print(f"{response.status_code} Not Found: {mapDetail['id']}-{mapDetail['name']}")
            pass

        else:
            mapDifficulty = mapDetail["versions"][-1]["diffs"]

            for k in mapDifficulty:

                """
                if k["characteristic"] != "Standard":
                    pass
                else:
                """

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

                i = 0
                list = []
                for d in [bpm, duration, difficulty, sageScore, njs, offset, notes, bombs,
                          obstacles,
                          nps, events, chroma, errors, warns, resets]:
                    d = (d - Main.df.iloc[i, 0]) / Main.df.iloc[i, 1]
                    list.append(d)
                    i += 1

                data = [list]

                ans = Main.clf.predict(data)
                # type(ans) -> numpy.ndarray

                finishPredict = (ans[0] * Main.df.iloc[14, 1]) + Main.df.iloc[14, 0]
                floatStarNumber = float(finishPredict)
                roundStarNumber = round(floatStarNumber, 2)

                if apiVersion == 1:
                    # result+=f'<p>{k["difficulty"]} - {roundStarNumber}</p>\n'
                    result.setdefault(k["difficulty"], roundStarNumber)
                elif apiVersion == 2:
                    # result+=f'<p>{characteristic}-{k["difficulty"]} - {roundStarNumber}</p>\n'
                    result.setdefault(f'{characteristic}-{k["difficulty"]}', roundStarNumber)

        return result
