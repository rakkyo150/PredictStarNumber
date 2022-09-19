# PredictStarNumber
[RankedMapData](https://github.com/rakkyo150/RankedMapData)のデータをもとに、BeatSaverで公開されている譜面のScoreSaberのランク基準の星の数を予測するアプリ。<br>
[こちら](https://predictstarnumber.herokuapp.com/)から使えます。<br>
[PredictStarNumberHelper](https://github.com/rakkyo150/PredictStarNumberHelper)のモデルを使用。<br>
BeatSaverのAPIから取得できる情報のみで学習を行ったので、譜面にもよりますが、結構外れた値がでることもあります。<br>
~~なお、学習精度に関しては[PredictStarNumberHelper](https://github.com/rakkyo150/PredictStarNumberHelper)のmodelScore.jsonで確認できます。<br>
ちなみに、2022/1/3現在の精度は、trainScoreが0.9745135905035479、testScoreが0.9405029861621208です。~~
学習精度に決定係数を用いるのは不適当だったので、その点は今後改善する予定です。<br>
それに伴って、学習済みモデルの調整も行うかもです。

## API
### V2
|Method|URI|Models|
|:---|:---|:---|
|GET|https://predictstarnumber.herokuapp.com/api2/id/{id(!bsr)}|{ characteristic-difficulty : PredictedStarNumber(float) }|
|GET|https://predictstarnumber.herokuapp.com/api2/hash/{hash}|{ characteristic-difficulty : PredictedStarNumber(float) }|
|GET|https://predictstarnumber.herokuapp.com/api2/leaderboardId/{leaderboardId}|{ characteristic-difficulty : PredictedStarNumber(float) }|

### V1
後方互換性のために古いAPIを残しています<br>
characteristicがStandardの予測値しか取得できません

|Method|URI|Models|
|:---|:---|:---|
|GET|https://predictstarnumber.herokuapp.com/api/id/{id(!bsr)}|{ difficulty : PredictedStarNumber(float) }|
|GET|https://predictstarnumber.herokuapp.com/api/hash/{hash}|{ difficulty : PredictedStarNumber(float) }|
|GET|https://predictstarnumber.herokuapp.com/api/leaderboardId/{leaderboardId}|{ difficulty : PredictedStarNumber(float) }|